def get_online_courses(current_time):
    return [
        {
            "name": "Data Structures and Algorithms",
            "description": "Covers fundamental data structures and algorithm design techniques, including sorting, searching, and graph algorithms.",
            "instructor": "Professor Zhang",
            "duration": "48 hours",
            "url": "https://course.example.com/dsa",
            "created_at": current_time,
            "updated_at": current_time,
            "keywords": "computer science, algorithms, data structures, programming, study method"
        },
        {
            "name": "Introduction to Software Engineering",
            "description": "Introduces software development processes and project management, including requirements analysis and design patterns.",
            "instructor": "Professor Li",
            "duration": "32 hours",
            "url": "https://course.example.com/se-intro",
            "created_at": current_time,
            "updated_at": current_time,
            "keywords": "software engineering, development, study method"
        },
        {
            "name": "Foundations of Machine Learning",
            "description": "Explains the basic concepts and algorithms in machine learning, including supervised and unsupervised learning.",
            "instructor": "Professor Wang",
            "duration": "56 hours",
            "url": "https://course.example.com/ml-basic",
            "created_at": current_time,
            "updated_at": current_time
        },
        {
            "name": "Web Development Practice",
            "description": "Covers full-stack development using modern web technologies, including frontend frameworks and backend architectures.",
            "instructor": "Professor Chen",
            "duration": "40 hours",
            "url": "https://course.example.com/web-dev",
            "created_at": current_time,
            "updated_at": current_time
        },
        {
            "name": "Database Systems Principles",
            "description": "Deep dive into database system design and implementation, including transactions, concurrency control, and indexing.",
            "instructor": "Professor Liu",
            "duration": "44 hours",
            "url": "https://course.example.com/database",
            "created_at": current_time,
            "updated_at": current_time
        }
    ]


def get_papers(current_time):
    return [
        {
            "title": "Application of Artificial Intelligence in Software Testing",
            "authors": "Researcher Wang, Researcher Zhang",
            "publication": "Journal of Software Engineering",
            "publish_date": current_time,
            "abstract": "This paper explores recent AI applications in software testing and proposes a deep learning-based automated testing approach...",
            "keywords": "Artificial Intelligence, Software Testing, Automation, study method, mental health",
            "created_at": current_time,
            "updated_at": current_time
        },
        {
            "title": "Research on Consensus Algorithms in Distributed Systems",
            "authors": "Researcher Li",
            "publication": "Journal of Computer Science",
            "publish_date": current_time,
            "abstract": "This paper analyzes common consensus algorithms in distributed systems, comparing Paxos and Raft...",
            "keywords": "Distributed Systems, Consensus Algorithms, Paxos",
            "created_at": current_time,
            "updated_at": current_time
        },
        {
            "title": "Code Generation Based on Deep Learning",
            "authors": "Researcher Chen, Researcher Huang",
            "publication": "Journal of Computer Research and Development",
            "publish_date": current_time,
            "abstract": "This research proposes a Transformer-based method for code generation from natural language descriptions...",
            "keywords": "Deep Learning, Code Generation, Transformer",
            "created_at": current_time,
            "updated_at": current_time
        },
        {
            "title": "Performance Optimization Strategies in Microservice Architecture",
            "authors": "Researcher Zhao, Researcher Qian",
            "publication": "Journal of Software",
            "publish_date": current_time,
            "abstract": "This paper proposes a set of performance optimization strategies for microservices, including service splitting and caching...",
            "keywords": "Microservices, Performance Optimization, Distributed Systems",
            "created_at": current_time,
            "updated_at": current_time
        },
        {
            "title": "Application of Blockchain in Supply Chain Management",
            "authors": "Researcher Sun",
            "publication": "Journal of Information Security",
            "publish_date": current_time,
            "abstract": "This paper discusses how blockchain improves transparency and traceability in supply chains and proposes implementation strategies...",
            "keywords": "Blockchain, Supply Chain Management, Traceability",
            "created_at": current_time,
            "updated_at": current_time
        }
    ]


def get_seminars(current_time):
    return [
        {
            "title": "AI Development Trends in 2025",
            "organizer": "School of Computer Science",
            "date": current_time,
            "location": "Main Building Auditorium",
            "description": "Discusses the latest trends and prospects in AI, including deep learning and reinforcement learning.",
            "created_at": current_time,
            "updated_at": current_time,
            "keywords": "artificial intelligence, trends, study efficiency, mental health"
        },
        {
            "title": "Best Practices in Software Engineering",
            "organizer": "School of Software",
            "date": current_time,
            "location": "Library Auditorium",
            "description": "Shares best practices and lessons learned in software development, covering agile, DevOps, and more.",
            "created_at": current_time,
            "updated_at": current_time
        },
        {
            "title": "Cloud-Native Technologies and Microservice Architecture",
            "organizer": "School of Information Engineering",
            "date": current_time,
            "location": "Tech Building Conference Room",
            "description": "Covers trends and practices in cloud-native development, including containerization and service mesh.",
            "created_at": current_time,
            "updated_at": current_time
        },
        {
            "title": "Data Science and Big Data Analytics",
            "organizer": "Center for Data Science",
            "date": current_time,
            "location": "Innovation Building Auditorium",
            "description": "Explores techniques and applications in data mining, machine learning, and big data analysis.",
            "created_at": current_time,
            "updated_at": current_time
        },
        {
            "title": "Cybersecurity Technology Innovation Forum",
            "organizer": "School of Cyberspace Security",
            "date": current_time,
            "location": "Security Building Conference Room",
            "description": "Covers new technologies and protection methods in cybersecurity, including vulnerability detection and prevention.",
            "created_at": current_time,
            "updated_at": current_time
        }
    ]


def get_majors(current_time):
    return [
        {
            "name": "Computer Science and Technology",
            "description": "This major prepares students with skills in hardware and software design, development, and application.",
            "created_at": current_time,
            "updated_at": current_time
        },
        {
            "name": "Software Engineering",
            "description": "This major focuses on software design, development, testing, and maintenance skills.",
            "created_at": current_time,
            "updated_at": current_time
        }
    ]


def get_major_resource_mappings():
    return {
        "Computer Science and Technology": {
            "online_courses": [0, 2],  # DSA, Machine Learning
            "papers": [1, 2],          # Distributed Systems, Code Generation
            "seminars": [0, 3]         # AI Trends, Data Science
        },
        "Software Engineering": {
            "online_courses": [1, 3],  # Software Engineering, Web Dev
            "papers": [0, 3],          # AI in Testing, Microservices
            "seminars": [1, 2]         # SE Best Practices, Cloud Native
        }
    }
