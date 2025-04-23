# ResearchHub

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

A multi-purpose Django web application combining research documentation, e-commerce functionality, and learning management.

## 🌟 Features

- **User Accounts System** - Authentication and profile management
- **E-Commerce Module** - Product listings and shopping functionality
- **Learning Management** - Educational content tracking system
- **Resource Hub** - Centralized research materials repository

## 📂 Project Structure
ResearchHub/
├── accounts/ # User authentication app
│ ├── migrations/ # Database migrations
│ ├── templates/ # HTML templates
│ ├── admin.py # Admin configuration
│ ├── models.py # Data models
│ └── views.py # Business logic
│
├── ecommerce_app/ # Online store functionality
│ ├── migrations/
│ ├── templates/
│ ├── models.py # Product/category models
│ └── views.py # Store logic
│
├── learning_logs/ # Educational tracking
│ ├── migrations/
│ ├── templates/
│ ├── forms.py # User input forms
│ ├── models.py # Learning content models
│ └── views.py # Learning interface
│
├── resources/ # Research materials
│ ├── migrations/
│ ├── templates/
│ ├── models.py # Resource models
│ └── views.py # Research interface
│
├── ll_project/ # Main project config
│ ├── settings.py # Django settings
│ └── urls.py # URL routing
│
├── manage.py # Django CLI tool
└── requirements.txt # Python dependencies
