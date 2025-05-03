from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.questionnaire import QuestionnaireService, QuestionnaireProcessor, QuestionnaireResultGenerator
from repo.questionnaireRepo import QuestionnaireRepository
from repo.userRepo import UserRepository
from model.db_base import session
from data.questionnaire_data import get_questionnaire_data
from datetime import datetime


class QuestionnaireController:
    bp = Blueprint('questionnaire', __name__,
                   template_folder='../templates',
                   static_folder='../static')

    def __init__(self):
        self.db_session = session
        self.questionnaire_repo = QuestionnaireRepository(session)
        self.user_repo = UserRepository(session)
        self.questionnaire_service = QuestionnaireService(self.questionnaire_repo)
        self.questionnaire_processor = QuestionnaireProcessor()
        self.register_routes()

    def register_routes(self):
        # 页面路由
        self.bp.add_url_rule('/questionnaires', 'list_page', self.list_page, methods=['GET'])
        self.bp.add_url_rule('/questionnaire/<int:questionnaire_id>', 'detail_page', self.detail_page, methods=['GET'])
        self.bp.add_url_rule('/questionnaire/take/<questionnaire_type>', 'take_questionnaire', self.take_questionnaire,
                             methods=['GET'])
        self.bp.add_url_rule('/questionnaire/submit/<questionnaire_type>', 'submit_new_questionnaire',
                             self.submit_new_questionnaire, methods=['POST'])
        self.bp.add_url_rule('/questionnaire/result', 'result_page', self.result_page, methods=['GET'])
        self.bp.add_url_rule('/questionnaire/history', 'history_page', self.history_page, methods=['GET'])
        self.bp.add_url_rule('/questionnaire/shared', 'shared_page', self.shared_page, methods=['GET'])

        # API 路由
        self.bp.add_url_rule('/api/questionnaires', 'list', self.list_questionnaires, methods=['GET'])
        self.bp.add_url_rule('/api/questionnaire/<int:questionnaire_id>/submit', 'submit', self.submit_questionnaire,
                             methods=['POST'])
        self.bp.add_url_rule('/api/questionnaire/delete/<int:record_id>', 'delete_record',
                             self.delete_record, methods=['POST'])
        self.bp.add_url_rule('/api/questionnaire/calculate-result', 'calculate_result',
                             self.calculate_result, methods=['POST'])

    @jwt_required(optional=True)  # 允许未登录访问
    def list_page(self):
        """问卷列表页面"""
        # 获取当前用户（可能为None）
        current_user = None
        try:
            user_id = get_jwt_identity()
            if user_id:
                current_user = self.user_repo.get_user_by_id(int(user_id))
        except:
            pass

        # 如果未登录，重定向到登录页面
        if not current_user:
            return redirect(url_for('auth.login_page'))

        # 如果是管理员，重定向到共享问卷页面
        if current_user.is_stuff:
            return redirect(url_for('questionnaire.shared_page'))

        # 获取新问卷类型
        questionnaires = []
        for q_type in self.questionnaire_processor.get_all_questionnaire_types():
            details = self.questionnaire_processor.get_questionnaire_details(q_type)
            if details:
                questionnaires.append({
                    'type': q_type,
                    'title': q_type.replace('_', ' ').title(),
                    'description': details.get('description', '')
                })

        return render_template('questionnaire/list_new.html', questionnaires=questionnaires)

    @jwt_required()
    def detail_page(self, questionnaire_id):
        """问卷详情页面"""
        user_id = int(get_jwt_identity())
        user = self.user_repo.get_user_by_id(user_id)

        if user.is_stuff:
            flash('管理员不能填写问卷', 'warning')
            return redirect(url_for('questionnaire.shared_page'))

        questionnaire = self.questionnaire_service.get_questionnaire(questionnaire_id)
        if not questionnaire:
            return "问卷不存在", 404
        return render_template('questionnaire/detail.html', questionnaire=questionnaire)

    @jwt_required()
    def take_questionnaire(self, questionnaire_type):
        """填写新类型的问卷"""
        user_id = int(get_jwt_identity())
        user = self.user_repo.get_user_by_id(user_id)

        if user.is_stuff:
            flash('管理员不能填写问卷', 'warning')
            return redirect(url_for('questionnaire.shared_page'))

        questionnaire = self.questionnaire_processor.get_questionnaire_details(questionnaire_type)
        if not questionnaire:
            flash('问卷类型不存在', 'danger')
            return redirect(url_for('questionnaire.list_page'))

        return render_template('questionnaire/form_new.html', questionnaire=questionnaire)

    @jwt_required()
    def submit_new_questionnaire(self, questionnaire_type):
        """提交新类型问卷的答案并计算结果"""
        user_id = int(get_jwt_identity())

        # 收集回答
        answers = {}
        for key, value in request.form.items():
            if key.startswith('question_'):
                question_id = int(key.replace('question_', ''))
                answers[question_id] = value

        # 用户是否选择分享
        is_shared = request.form.get('is_shared') == 'on'

        try:
            # 计算问卷结果
            result = self.questionnaire_processor.calculate_score(questionnaire_type, answers)

            # 根据问卷类型和得分判断是否符合条件共享
            should_share = False
            if is_shared:  # 只有用户选择分享时才考虑条件
                total_score = result.get('total_score', 0)
                if questionnaire_type == 'beck_depression_inventory' and total_score >= 14:
                    # 贝克抑郁量表 >= 轻度抑郁
                    should_share = True
                elif questionnaire_type == 'study_status_assessment' and total_score >= 40:
                    # 学习状态评估 >= 状态下滑
                    should_share = True

            # 生成结果页面内容
            result_content = QuestionnaireResultGenerator.generate_result_content(result)

            # 保存问卷记录到数据库
            # 注意: 保存记录时使用实际的共享条件判断结果
            questionnaire_id = 0  # 临时问卷ID，需要在数据库中创建对应记录
            success, message = self.questionnaire_service.submit_questionnaire(
                user_id=user_id,
                questionnaire_id=questionnaire_id,
                answers=answers,
                is_shared=should_share,  # 使用条件判断后的共享结果
                questionnaire_type=questionnaire_type  # 添加问卷类型
            )

            if not success:
                flash(f'保存问卷记录失败: {message}', 'danger')

            # 将结果保存到会话中
            from flask import session
            session['questionnaire_result'] = result_content

            return redirect(url_for('questionnaire.result_page'))

        except Exception as e:
            flash(f'处理问卷失败: {str(e)}', 'danger')
            return redirect(url_for('questionnaire.list_page'))

    @jwt_required()
    def result_page(self):
        """显示问卷结果"""
        from flask import session

        result = session.get('questionnaire_result')
        if not result:
            flash('没有问卷结果可显示', 'warning')
            return redirect(url_for('questionnaire.list_page'))

        # 清除会话中的结果，防止重复访问
        session.pop('questionnaire_result', None)

        return render_template('questionnaire/result.html', result=result)

    @jwt_required()
    def history_page(self):
        """用户的问卷历史记录"""
        user_id = int(get_jwt_identity())
        questionnaires = self.questionnaire_service.get_user_questionnaires(user_id)
        return render_template('questionnaire/history.html', questionnaires=questionnaires)

    @jwt_required()
    def shared_page(self):
        """查看共享的问卷结果（仅管理员可见）"""
        user_id = int(get_jwt_identity())
        user = self.user_repo.get_user_by_id(user_id)

        if not user.is_stuff:
            flash('权限不足', 'danger')
            return redirect(url_for('questionnaire.list_page'))

        questionnaires = self.questionnaire_service.get_shared_questionnaires()
        return render_template('questionnaire/shared.html', questionnaires=questionnaires)

    @jwt_required()
    def list_questionnaires(self):
        """获取问卷列表(API)"""
        user_id = int(get_jwt_identity())
        user = self.user_repo.get_user_by_id(user_id)

        if user.is_stuff:
            return jsonify({
                'success': False,
                'message': '管理员不能填写问卷'
            }), 403

        # 获取新问卷类型和旧问卷类型
        questionnaires_data = []

        # 新问卷类型
        for q_type in self.questionnaire_processor.get_all_questionnaire_types():
            details = self.questionnaire_processor.get_questionnaire_details(q_type)
            if details:
                questionnaires_data.append({
                    'id': 0,  # 使用临时ID，前端需要区分处理
                    'type': q_type,
                    'description': details.get('description', ''),
                    'created_at': datetime.now().isoformat(),
                    'is_new_type': True  # 标记为新类型问卷
                })

        # 旧问卷类型
        old_questionnaires = self.questionnaire_service.get_questionnaires()
        for q in old_questionnaires:
            questionnaires_data.append({
                'id': q.id,
                'type': q.type,
                'description': q.description,
                'created_at': q.created_at.isoformat(),
                'is_new_type': False
            })

        return jsonify({
            'success': True,
            'data': questionnaires_data
        })

    @jwt_required()
    def submit_questionnaire(self, questionnaire_id):
        """提交问卷答案(旧API)"""
        user_id = int(get_jwt_identity())
        data = request.get_json()

        success, message = self.questionnaire_service.submit_questionnaire(
            user_id=user_id,
            questionnaire_id=questionnaire_id,
            answers=data['answers'],
            is_shared=data.get('is_shared', False)
        )

        return jsonify({
            'success': success,
            'message': message
        }), 200 if success else 500

    @jwt_required()
    def delete_record(self, record_id):
        """删除问卷记录"""
        user_id = int(get_jwt_identity())
        success, message = self.questionnaire_service.delete_questionnaire_record(record_id, user_id)

        return jsonify({
            'success': success,
            'message': message
        }), 200 if success else (404 if message == "记录不存在" else 403)

    @jwt_required()
    def calculate_result(self):
        """计算问卷结果API"""
        data = request.get_json()
        questionnaire_type = data.get('questionnaire_type')
        answers = data.get('answers', {})

        try:
            # 确保答案格式正确
            processed_answers = {}
            for question_id, answer in answers.items():
                # 将问题ID转为整数
                q_id = int(question_id) if isinstance(question_id, str) else question_id

                # 将答案转为整数(如果可能)
                if isinstance(answer, str) and answer.isdigit():
                    processed_answers[q_id] = int(answer)
                else:
                    processed_answers[q_id] = answer

            # 计算问卷结果
            if questionnaire_type and processed_answers:
                # 对于新类型问卷，使用问卷处理器
                if questionnaire_type in ['beck_depression_inventory', 'study_status_assessment']:
                    result = self.questionnaire_processor.calculate_score(questionnaire_type, processed_answers)
                    result_content = QuestionnaireResultGenerator.generate_result_content(result)

                    # 调试信息 - 打印完整结果内容
                    print(f"计算结果: {result}")
                    print(f"生成的结果内容: {result_content}")

                    return jsonify({
                        'success': True,
                        'result': result_content
                    })
                # 对于旧类型问卷，返回错误
                else:
                    return jsonify({
                        'success': False,
                        'message': '暂不支持此类型问卷的结果计算'
                    })
            else:
                return jsonify({
                    'success': False,
                    'message': '参数缺失'
                })
        except Exception as e:
            import traceback
            print(f"计算结果错误: {str(e)}")
            print(traceback.format_exc())  # 打印详细错误信息

            return jsonify({
                'success': False,
                'message': f'计算结果失败: {str(e)}'
            })