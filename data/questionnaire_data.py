def get_questionnaire_data(current_time):
    return [
        {
            "type": "beck_depression_inventory",
            "description": "The Beck Depression Inventory (BDI-II) is a questionnaire designed to assess the severity of depressive symptoms. Please choose the option that best describes your feelings over the past two weeks, including today.",
            "content": {
                "questions": [
                    {
                        "id": 1,
                        "type": "single_choice",
                        "question": "Sadness",
                        "options": [
                            {"value": "0", "text": "I do not feel sad."},
                            {"value": "1", "text": "I feel sad much of the time."},
                            {"value": "2", "text": "I am sad all the time."},
                            {"value": "3", "text": "I am so sad or unhappy that I can't stand it."}
                        ]
                    },
                    {
                        "id": 2,
                        "type": "single_choice",
                        "question": "Pessimism about the future",
                        "options": [
                            {"value": "0", "text": "I am not pessimistic about the future."},
                            {"value": "1", "text": "I feel more pessimistic than I used to."},
                            {"value": "2", "text": "I don’t expect things to get better."},
                            {"value": "3", "text": "I feel hopeless about the future."}
                        ]
                    },
                    {
                        "id": 3,
                        "type": "single_choice",
                        "question": "Feelings of failure",
                        "options": [
                            {"value": "0", "text": "I do not feel like a failure."},
                            {"value": "1", "text": "I feel I have failed more than I should have."},
                            {"value": "2", "text": "When I look back, I see a lot of failures."},
                            {"value": "3", "text": "I feel like a complete failure."}
                        ]
                    },
                    {
                        "id": 4,
                        "type": "single_choice",
                        "question": "Loss of pleasure",
                        "options": [
                            {"value": "0", "text": "I still get pleasure from things."},
                            {"value": "1", "text": "I don’t enjoy things as much as I used to."},
                            {"value": "2", "text": "I get very little pleasure from the things I used to enjoy."},
                            {"value": "3", "text": "I can't get any pleasure from the things I used to enjoy."}
                        ]
                    },
                    {
                        "id": 5,
                        "type": "single_choice",
                        "question": "Guilt feelings",
                        "options": [
                            {"value": "0", "text": "I do not feel particularly guilty."},
                            {"value": "1", "text": "I feel guilty over things I have done or should have done."},
                            {"value": "2", "text": "I feel guilty most of the time."},
                            {"value": "3", "text": "I feel guilty all of the time."}
                        ]
                    },
                    {
                        "id": 6,
                        "type": "single_choice",
                        "question": "Feelings of punishment",
                        "options": [
                            {"value": "0", "text": "I do not feel I am being punished."},
                            {"value": "1", "text": "I feel I may be punished."},
                            {"value": "2", "text": "I expect to be punished."},
                            {"value": "3", "text": "I feel I am being punished."}
                        ]
                    },
                    {
                        "id": 7,
                        "type": "single_choice",
                        "question": "Self-dislike",
                        "options": [
                            {"value": "0", "text": "I feel the same about myself as ever."},
                            {"value": "1", "text": "I have lost confidence in myself."},
                            {"value": "2", "text": "I am disappointed in myself."},
                            {"value": "3", "text": "I dislike myself."}
                        ]
                    },
                    {
                        "id": 8,
                        "type": "single_choice",
                        "question": "Self-criticalness",
                        "options": [
                            {"value": "0", "text": "I don’t criticize or blame myself more than usual."},
                            {"value": "1", "text": "I am more critical of myself than I used to be."},
                            {"value": "2", "text": "I blame myself for all of my faults."},
                            {"value": "3", "text": "I blame myself for everything bad that happens."}
                        ]
                    },
                    {
                        "id": 9,
                        "type": "single_choice",
                        "question": "Suicidal thoughts or wishes",
                        "options": [
                            {"value": "0", "text": "I don’t have any thoughts of killing myself."},
                            {"value": "1",
                             "text": "I have thoughts of killing myself, but I would not carry them out."},
                            {"value": "2", "text": "I would like to kill myself."},
                            {"value": "3", "text": "I would kill myself if I had the chance."}
                        ]
                    },
                    {
                        "id": 10,
                        "type": "single_choice",
                        "question": "Crying",
                        "options": [
                            {"value": "0", "text": "I don’t cry any more than I used to."},
                            {"value": "1", "text": "I cry more than I used to."},
                            {"value": "2", "text": "I cry over every little thing."},
                            {"value": "3", "text": "I feel like crying, but I can’t."}
                        ]
                    },
                    {
                        "id": 11,
                        "type": "single_choice",
                        "question": "Agitation",
                        "options": [
                            {"value": "0", "text": "I am no more restless or wound up than usual."},
                            {"value": "1", "text": "I feel more restless or wound up than usual."},
                            {"value": "2", "text": "I am so restless or agitated that it’s hard to stay still."},
                            {"value": "3",
                             "text": "I am so restless or agitated that I have to keep moving or doing something."}
                        ]
                    },
                    {
                        "id": 12,
                        "type": "single_choice",
                        "question": "Loss of interest",
                        "options": [
                            {"value": "0", "text": "I have not lost interest in other people or activities."},
                            {"value": "1", "text": "I am less interested in other people or things than before."},
                            {"value": "2", "text": "I have lost most of my interest in other people or things."},
                            {"value": "3", "text": "It’s hard to get interested in anything."}
                        ]
                    },
                    {
                        "id": 13,
                        "type": "single_choice",
                        "question": "Indecisiveness",
                        "options": [
                            {"value": "0", "text": "I make decisions about as well as ever."},
                            {"value": "1", "text": "I find it more difficult to make decisions than usual."},
                            {"value": "2",
                             "text": "I have much greater difficulty in making decisions than I used to."},
                            {"value": "3", "text": "I have trouble making any decisions."}
                        ]
                    },
                    {
                        "id": 14,
                        "type": "single_choice",
                        "question": "Worthlessness",
                        "options": [
                            {"value": "0", "text": "I do not feel I am worthless."},
                            {"value": "1", "text": "I don’t consider myself as worthwhile and useful as I used to."},
                            {"value": "2", "text": "I feel more worthless as compared to others."},
                            {"value": "3", "text": "I feel utterly worthless."}
                        ]
                    },
                    {
                        "id": 15,
                        "type": "single_choice",
                        "question": "Loss of energy",
                        "options": [
                            {"value": "0", "text": "I have as much energy as ever."},
                            {"value": "1", "text": "I have less energy than I used to have."},
                            {"value": "2", "text": "I don’t have enough energy to do very much."},
                            {"value": "3", "text": "I don’t have enough energy to do anything."}
                        ]
                    },
                    {
                        "id": 16,
                        "type": "single_choice",
                        "question": "Changes in sleeping pattern",
                        "options": [
                            {"value": "0", "text": "I have not experienced any change in my sleeping pattern."},
                            {"value": "1", "text": "My sleep is somewhat more or less than usual."},
                            {"value": "2", "text": "I sleep a lot more or a lot less than usual."},
                            {"value": "3",
                             "text": "I sleep most of the day / I wake up too early and can't get back to sleep."}
                        ]
                    },
                    {
                        "id": 17,
                        "type": "single_choice",
                        "question": "Irritability",
                        "options": [
                            {"value": "0", "text": "I am no more irritable than usual."},
                            {"value": "1", "text": "I am more irritable than usual."},
                            {"value": "2", "text": "I am much more irritable than usual."},
                            {"value": "3", "text": "I am irritable all the time."}
                        ]
                    },
                    {
                        "id": 18,
                        "type": "single_choice",
                        "question": "Changes in appetite",
                        "options": [
                            {"value": "0", "text": "My appetite has not changed."},
                            {"value": "1", "text": "My appetite is somewhat less or more than usual."},
                            {"value": "2", "text": "My appetite is much less or much greater than usual."},
                            {"value": "3", "text": "I have no appetite at all / I crave food all the time."}
                        ]
                    },
                    {
                        "id": 19,
                        "type": "single_choice",
                        "question": "Difficulty concentrating",
                        "options": [
                            {"value": "0", "text": "I can concentrate as well as ever."},
                            {"value": "1", "text": "I can’t concentrate as well as usual."},
                            {"value": "2", "text": "It’s hard to keep my mind on anything for very long."},
                            {"value": "3", "text": "I find I can’t concentrate on anything."}
                        ]
                    },
                    {
                        "id": 20,
                        "type": "single_choice",
                        "question": "Tiredness or fatigue",
                        "options": [
                            {"value": "0", "text": "I am no more tired or fatigued than usual."},
                            {"value": "1", "text": "I get tired or fatigued more easily than usual."},
                            {"value": "2",
                             "text": "I am too tired or fatigued to do a lot of the things I used to do."},
                            {"value": "3", "text": "I am too tired or fatigued to do most of the things I used to do."}
                        ]
                    },
                    {
                        "id": 21,
                        "type": "single_choice",
                        "question": "Loss of interest in sex",
                        "options": [
                            {"value": "0", "text": "I have not noticed any recent change in my interest in sex."},
                            {"value": "1", "text": "I am less interested in sex than I used to be."},
                            {"value": "2", "text": "I have much less interest in sex now."},
                            {"value": "3", "text": "I have lost interest in sex completely."}
                        ]
                    }
                ],
                "scoring": {
                    "ranges": [
                        {"min": 0, "max": 13, "level": "minimal", "description": "Minimal depression"},
                        {"min": 14, "max": 19, "level": "mild", "description": "Mild depression"},
                        {"min": 20, "max": 28, "level": "moderate", "description": "Moderate depression"},
                        {"min": 29, "max": 63, "level": "severe", "description": "Severe depression"}
                    ]
                }
            },
            "created_at": current_time,
            "updated_at": current_time
        },
        {
            "type": "study_status_assessment",
            "description": "This questionnaire is designed to assess your study status over the past month. Please select the option that best reflects your actual experience.",
            "content": {
                "questions": [
                    {
                        "id": 1,
                        "type": "single_choice",
                        "question": "Do you procrastinate or fail to complete study tasks on time?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 2,
                        "type": "single_choice",
                        "question": "Do you get distracted easily during study?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 3,
                        "type": "single_choice",
                        "question": "Do you compress your study time due to procrastination?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 4,
                        "type": "single_choice",
                        "question": "Do you feel overwhelmed or stressed by course content?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 5,
                        "type": "single_choice",
                        "question": "Do you lack a study plan or schedule?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 6,
                        "type": "single_choice",
                        "question": "Do you find it hard to stay focused in class?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 7,
                        "type": "single_choice",
                        "question": "Do you often stay up late to finish assignments or study?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 8,
                        "type": "single_choice",
                        "question": "Do you feel anxious before exams or quizzes?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 9,
                        "type": "single_choice",
                        "question": "Do you avoid discussing problems with teachers or classmates?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 10,
                        "type": "single_choice",
                        "question": "Do you experience mood swings because of study tasks?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 11,
                        "type": "single_choice",
                        "question": "Do you feel a lack of sense of accomplishment in learning?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 12,
                        "type": "single_choice",
                        "question": "Do you lack motivation to start studying?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 13,
                        "type": "single_choice",
                        "question": "Do you easily give up when facing difficult study materials?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 14,
                        "type": "single_choice",
                        "question": "Do you struggle to balance study and rest time?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 15,
                        "type": "single_choice",
                        "question": "Do you feel that your study efficiency is low?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 16,
                        "type": "single_choice",
                        "question": "Do you often use your phone or watch short videos while studying?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 17,
                        "type": "single_choice",
                        "question": "Do you feel that you're falling behind your classmates?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 18,
                        "type": "single_choice",
                        "question": "Are you unwilling to actively review or reinforce learned content?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 19,
                        "type": "single_choice",
                        "question": "Do you feel confused about your future academic or career direction?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    },
                    {
                        "id": 20,
                        "type": "single_choice",
                        "question": "Do you feel resistant to studying or unable to focus on learning?",
                        "options": [
                            {"value": "0", "text": "Never"},
                            {"value": "1", "text": "Rarely"},
                            {"value": "2", "text": "Sometimes"},
                            {"value": "3", "text": "Often"},
                            {"value": "4", "text": "Always"}
                        ]
                    }
                ],
                "scoring": {
                    "ranges": [
                        {
                            "min": 0,
                            "max": 19,
                            "level": "good",
                            "description": "Good status",
                            "detail": "Your study state is stable, showing strong self-discipline and adaptability.",
                            "suggestions": [
                                "Maintain your good habits and gradually improve efficiency based on your goals.",
                                "Continue to keep a positive learning attitude.",
                                "Consider helping peers to make collective progress."
                            ]
                        },
                        {
                            "min": 20,
                            "max": 39,
                            "level": "mild",
                            "description": "Mild fluctuation",
                            "detail": "There are some fluctuations in your study state, possibly affected by emotions or habits.",
                            "suggestions": [
                                "Try creating a study plan to reduce distractions.",
                                "Maintain positive reinforcement.",
                                "Establish a regular daily routine.",
                                "Find learning methods that work for you."
                            ]
                        },
                        {
                            "min": 40,
                            "max": 59,
                            "level": "moderate",
                            "description": "Declining state",
                            "detail": "You may feel a lack of motivation or efficiency, which limits your learning outcome.",
                            "suggestions": [
                                "Adjust your routine and avoid distractions.",
                                "Seek help from advisors or study partners.",
                                "Set concrete plans for improvement.",
                                "Relax appropriately and adjust your mindset."
                            ]
                        },
                        {
                            "min": 60,
                            "max": 80,
                            "level": "severe",
                            "description": "Severely ineffective",
                            "detail": "Your study state is poor and may involve procrastination, anxiety, or burnout.",
                            "suggestions": [
                                "Consider structured time management training.",
                                "Seek psychological counseling or support.",
                                "Contact your school’s support center if needed.",
                                "Adjust your study rhythm and proceed gradually."
                            ]
                        }
                    ]
                }
            },
            "created_at": current_time,
            "updated_at": current_time
        }
    ] 