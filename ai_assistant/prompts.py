# Specialized prompts and reference knowledge for AI Placement Assistant

SYSTEM_PROMPT = """You are an expert AI College Placement Officer and Career Mentor for engineering and management students.
Your mission is to provide encouraging, realistic, accurate, and actionable guidance for campus placement preparation.
You help students find relevant campus jobs, master interview questions, optimize their resumes, and understand placement eligibility.
Always respond in concise, friendly, and structured Markdown with clear bullet points.
"""

CAREER_ROADMAPS = {
    'python_developer': {
        'title': 'Python Developer Career Roadmap',
        'steps': [
            {'step': 1, 'title': 'Master Python Fundamentals', 'desc': 'Data types, loops, OOP (Classes, Inheritance, Polymorphism), generators, decorators, and exception handling.'},
            {'step': 2, 'title': 'Databases & SQL Mastery', 'desc': 'Relational DB concepts, PostgreSQL/MySQL, writing efficient queries, indexing, joins, and normal forms.'},
            {'step': 3, 'title': 'Master Web Frameworks (Django / FastAPI)', 'desc': 'Django MVT architecture, ORM queries, authentication, middlewares, forms, and admin customization.'},
            {'step': 4, 'title': 'Build RESTful APIs', 'desc': 'Django REST Framework, serialization, JWT authentication, CRUD endpoints, status codes, and Swagger/OpenAPI.'},
            {'step': 5, 'title': 'Version Control & Development Tools', 'desc': 'Git branching, GitHub pull requests, virtualenv/Pipenv, unit testing with PyTest, and code quality (flake8).'},
            {'step': 6, 'title': 'Cloud & Deployment Basics', 'desc': 'Docker containerization, Gunicorn/Nginx, hosting on AWS EC2 or Render, and environment variable security.'},
            {'step': 7, 'title': 'Build Capstone Placement Project', 'desc': 'Develop a full-featured web application (e.g. AI Placement Portal or E-commerce) and publish live demo with GitHub repo.'},
            {'step': 8, 'title': 'Campus Interview Preparation', 'desc': 'Practice data structures in Python (lists, dicts, trees), solve LeetCode easy/medium, and rehearse HR STAR method questions.'}
        ]
    },
    'data_analyst': {
        'title': 'Data Analyst Career Roadmap',
        'steps': [
            {'step': 1, 'title': 'Advanced SQL & Data Querying', 'desc': 'Window functions, CTEs, subqueries, group by rollups, aggregations, and data extraction.'},
            {'step': 2, 'title': 'Data Manipulation with Python', 'desc': 'Pandas dataframes, NumPy arrays, data cleaning, handling missing values, and type conversions.'},
            {'step': 3, 'title': 'Data Visualization & Storytelling', 'desc': 'Matplotlib, Seaborn, designing intuitive charts, and communicating findings to non-technical stakeholders.'},
            {'step': 4, 'title': 'Business Intelligence (Power BI / Tableau)', 'desc': 'Creating interactive dashboards, DAX formulas, calculated measures, and scheduled refreshes.'},
            {'step': 5, 'title': 'Applied Business Statistics', 'desc': 'Mean, median, standard deviation, probability distributions, hypothesis testing (p-value, t-test), and A/B testing.'},
            {'step': 6, 'title': 'Excel for Business Analysis', 'desc': 'Pivot tables, VLOOKUP/XLOOKUP, conditional formatting, and financial modelling.'},
            {'step': 7, 'title': 'Real-World Case Studies', 'desc': 'Perform exploratory data analysis on sales, churn, or healthcare datasets and publish findings on Kaggle/GitHub.'},
            {'step': 8, 'title': 'Placement Interview Preparation', 'desc': 'Solve live SQL interview queries, practice product metrics questions, and explain business trade-offs.'}
        ]
    },
    'data_engineer': {
        'title': 'Data Engineer Career Roadmap',
        'steps': [
            {'step': 1, 'title': 'Python & Advanced SQL', 'desc': 'Data structures in Python, writing complex analytical SQL queries, database indexing, and query execution plans.'},
            {'step': 2, 'title': 'Data Modeling & Warehousing', 'desc': 'Star schema, snowflake schema, dimensional modeling, OLTP vs OLAP, Snowflake, Google BigQuery, or Amazon Redshift.'},
            {'step': 3, 'title': 'ETL / ELT Pipeline Engineering', 'desc': 'Building reliable ingestion pipelines, batch processing, data validation, and idempotency.'},
            {'step': 4, 'title': 'Workflow Orchestration (Apache Airflow)', 'desc': 'Writing DAGs in Python, scheduling tasks, handling dependencies, retries, and monitoring alerts.'},
            {'step': 5, 'title': 'Big Data Processing (Apache Spark / PySpark)', 'desc': 'Distributed computing concepts, Spark DataFrames, transformations vs actions, and optimizing partitioning.'},
            {'step': 6, 'title': 'Streaming & Messaging (Kafka)', 'desc': 'Publish-subscribe messaging, topics, partitions, consumer groups, and real-time streaming ingestion.'},
            {'step': 7, 'title': 'Cloud Data Architecture (AWS / GCP / Azure)', 'desc': 'S3 data lakes, IAM security, AWS Glue, and infrastructure as code basics.'},
            {'step': 8, 'title': 'Campus Interview Prep', 'desc': 'System design for data pipelines, SQL window problem solving, and explaining data warehousing architecture.'}
        ]
    },
    'fullstack_developer': {
        'title': 'Full Stack Web Developer Roadmap',
        'steps': [
            {'step': 1, 'title': 'Frontend Foundations', 'desc': 'Semantic HTML5, CSS3 (Flexbox, Grid), JavaScript ES6+ (Async/Await, Promises, DOM manipulation).'},
            {'step': 2, 'title': 'Modern Frontend Framework (React / Next.js)', 'desc': 'Components, props, state, hooks (useState, useEffect), routing, and state management.'},
            {'step': 3, 'title': 'Backend Foundations (Django or Node.js)', 'desc': 'Server-side routing, controllers/views, authentication, and database connections.'},
            {'step': 4, 'title': 'Database Design (SQL & NoSQL)', 'desc': 'Schema normalization, indexing, relationships, and queries using ORMs.'},
            {'step': 5, 'title': 'API Design & Integration', 'desc': 'RESTful API standards, JSON data transfer, handling CORS, error handling, and API security.'},
            {'step': 6, 'title': 'Authentication & Authorization', 'desc': 'Session auth, JWT tokens, password hashing, role-based access control (RBAC).'},
            {'step': 7, 'title': 'Deployment & CI/CD', 'desc': 'Deploying frontend and backend to cloud providers, setting up automated GitHub Actions.'},
            {'step': 8, 'title': 'Technical Interviews & Portfolios', 'desc': 'Building responsive portfolio with 3 full-stack projects, solving DSA problems on arrays and graphs.'}
        ]
    },
    'ai_ml_engineer': {
        'title': 'AI / Machine Learning Engineer Roadmap',
        'steps': [
            {'step': 1, 'title': 'Mathematics for Machine Learning', 'desc': 'Linear algebra (matrices, eigenvalues), calculus (gradients), probability and statistics.'},
            {'step': 2, 'title': 'Python & Data Stack', 'desc': 'NumPy, Pandas, Matplotlib, Scikit-Learn for preprocessing, feature scaling, and train-test splits.'},
            {'step': 3, 'title': 'Classical Machine Learning', 'desc': 'Supervised learning (Regression, Trees, Random Forests, XGBoost), Unsupervised (K-Means, PCA).'},
            {'step': 4, 'title': 'Deep Learning Foundations', 'desc': 'Neural networks, activation functions, backpropagation, PyTorch or TensorFlow, CNNs for vision, RNNs/Transformers.'},
            {'step': 5, 'title': 'Natural Language Processing & LLMs', 'desc': 'Tokenization, embeddings, attention mechanisms, fine-tuning LLMs, and prompt engineering with LangChain.'},
            {'step': 6, 'title': 'MLOps & Model Serving', 'desc': 'FastAPI model endpoints, ONNX runtime, Docker containerization, and model monitoring.'},
            {'step': 7, 'title': 'Capstone AI Application', 'desc': 'Deploy a live AI application (e.g. document Q&A, recommendation engine, or computer vision detector).'},
            {'step': 8, 'title': 'Technical Coding & AI Interviews', 'desc': 'Explaining bias-variance tradeoff, regularization, model evaluation metrics (F1-score, ROC-AUC), and LeetCode.'}
        ]
    }
}
