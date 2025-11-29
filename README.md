# 🩸 LifeLink - Blood Bank Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.1-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**A modern, feature-rich blood bank management system connecting donors with patients in need.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API Documentation](#-api-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Database Models](#-database-models)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

---

## 🌟 Overview

**LifeLink** is a comprehensive blood bank management system built with Flask that facilitates the critical connection between blood donors and patients in need. The platform provides an intuitive interface for managing donor registrations, blood requests, emergency alerts, and real-time communication between donors and patients.

### Why LifeLink?

- 🚨 **Emergency Response**: Quick matching of donors with urgent blood requests
- 💬 **Real-time Chat**: Direct communication between donors and patients via WebSocket
- 📊 **Analytics Dashboard**: Comprehensive statistics and insights for administrators
- 🔒 **Secure**: CSRF protection, secure session management, and data validation
- 📱 **Responsive**: Mobile-friendly interface built with Tailwind CSS
- 🌐 **Scalable**: Modular architecture supporting easy expansion

---

## ✨ Features

### For Donors
- ✅ **Registration & Profile Management**: Complete donor profile with medical history
- 📅 **Availability Management**: Set and update blood donation availability
- 🔔 **Emergency Notifications**: Receive alerts for urgent blood requests
- 📊 **Donation History**: Track personal donation history and achievements
- 💬 **Direct Messaging**: Communicate with patients securely
- 🎖️ **Achievements & Badges**: Gamification to encourage donations

### For Patients
- 🩸 **Blood Request System**: Submit blood requirements with urgency levels
- 🔍 **Donor Search**: Find compatible donors by blood type and location
- ⚡ **Emergency Requests**: Mark critical requests for priority attention
- 💬 **Contact Donors**: Direct communication with potential donors
- 📍 **Location-based Search**: Find nearby donors

### For Administrators
- 📈 **Analytics Dashboard**: System-wide statistics and metrics
- 👥 **User Management**: Manage donor and patient accounts
- 🚨 **Emergency Management**: Monitor and prioritize critical requests
- 📊 **Reports Generation**: Generate detailed reports on donations and requests
- ⚙️ **System Configuration**: Platform settings and customization
- 🔍 **Activity Monitoring**: Track platform usage and engagement

### Technical Features
- 🔐 **Authentication System**: Secure login/registration with session management
- 🛡️ **CSRF Protection**: Flask-WTF integration for form security
- 🗄️ **Database Management**: SQLAlchemy ORM with migration support
- 🔄 **Real-time Updates**: WebSocket implementation with Flask-SocketIO
- 📧 **Email Validation**: Comprehensive form validation
- 🎨 **Modern UI/UX**: Responsive design with Tailwind CSS and Lucide icons
- 🌐 **RESTful API**: Structured routing system for API endpoints

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.1.1
- **ORM**: Flask-SQLAlchemy 3.1.1
- **Migration**: Flask-Migrate 4.1.0
- **Authentication**: Flask-Login 0.6.3
- **Forms**: Flask-WTF 1.2.2, WTForms 3.2.1
- **Real-time**: Flask-SocketIO 5.3.6
- **Validation**: email-validator 2.1.0
- **Environment**: python-dotenv 1.0.0

### Frontend
- **Styling**: Tailwind CSS (CDN)
- **Icons**: Lucide Icons
- **UI Components**: Custom HTML/CSS/JavaScript
- **Animations**: CSS animations and transitions

### Database
- **Development**: SQLite (default)
- **Production**: PostgreSQL/MySQL (configurable)

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/lifelink-blood-bank.git
   cd lifelink-blood-bank
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv myenv
   ```

3. **Activate the virtual environment**
   
   **Linux/macOS:**
   ```bash
   source myenv/bin/activate
   ```
   
   **Windows:**
   ```bash
   myenv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and configure your settings (see [Configuration](#-configuration))

6. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

---

## ⚙️ Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///lifelink.db
# For PostgreSQL: DATABASE_URL=postgresql://username:password@localhost/dbname
# For MySQL: DATABASE_URL=mysql://username:password@localhost/dbname

# Application Settings
APP_NAME=LifeLink Blood Bank
APP_VERSION=1.0.0

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Socket.IO Configuration
SOCKETIO_MESSAGE_QUEUE=redis://localhost:6379/0  # Optional for production
```

### Configuration Classes

The application supports multiple configuration environments:
- `DevelopmentConfig`: Development settings with debug mode
- `ProductionConfig`: Production-ready settings
- `TestingConfig`: Testing environment configuration

Set the environment via the `FLASK_ENV` variable in `.env`.

---

## 🚀 Usage

### Running in Development Mode

```bash
python app.py
```

The application will run on `http://localhost:5000` with debug mode enabled.

### Running in Production

1. **Install production server**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 --worker-class eventlet -w 1 app:app
   ```
   Note: Flask-SocketIO requires eventlet or gevent worker class

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

---

## 📁 Project Structure

```
lifelink-blood-bank/
├── app.py                     # Main application entry point
├── config.py                  # Configuration settings
├── models.py                  # Database models
├── forms.py                   # WTForms form definitions
├── database.py                # Database utilities
├── utils.py                   # Helper functions
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── README.md                 # Project documentation
│
├── routes/                   # Route blueprints
│   ├── __init__.py          # Routes initialization
│   ├── auth.py              # Authentication routes
│   ├── donor.py             # Donor-specific routes
│   ├── patient.py           # Patient-specific routes
│   ├── admin.py             # Admin routes
│   ├── emergency.py         # Emergency request routes
│   └── chat.py              # Chat/messaging routes
│
├── templates/               # Jinja2 HTML templates
│   ├── base.html           # Base template with navigation
│   ├── index.html          # Homepage
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── emergency.html      # Emergency requests page
│   ├── donors.html         # Donors listing
│   ├── dashboard/          # Dashboard templates
│   │   ├── donor.html      # Donor dashboard
│   │   ├── patient.html    # Patient dashboard
│   │   └── admin.html      # Admin dashboard
│   └── errors/             # Error pages
│       ├── 404.html        # Not found
│       ├── 403.html        # Forbidden
│       └── 500.html        # Server error
│
├── static/                 # Static assets
│   ├── css/               # Custom stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Image assets
│
├── migrations/            # Database migrations
│   └── versions/          # Migration versions
│
└── instance/             # Instance-specific files
    └── lifelink.db       # SQLite database (development)
```

---

## 💾 Database Models

### Donor
- Personal information (name, email, phone)
- Blood type and Rh factor
- Medical history and eligibility
- Availability status
- Location (city, state, country)
- Donation history

### Patient
- Personal information
- Blood type requirements
- Medical condition details
- Urgency level
- Hospital/location information

### BloodRequest
- Request details and urgency
- Required blood type and quantity
- Patient information
- Status tracking
- Expiration date

### ChatMessage
- Sender and receiver information
- Message content
- Timestamps
- Read status

### Emergency
- Emergency alert details
- Priority level
- Location
- Contact information
- Response tracking

---

## 📡 API Documentation

### Authentication Endpoints

```
POST   /api/auth/register    - Register new user
POST   /api/auth/login       - User login
POST   /api/auth/logout      - User logout
GET    /api/auth/verify      - Verify authentication status
```

### Donor Endpoints

```
GET    /api/donors           - Get all donors (with filters)
GET    /api/donors/:id       - Get specific donor
PUT    /api/donors/:id       - Update donor profile
DELETE /api/donors/:id       - Delete donor account
POST   /api/donors/availability - Update availability
```

### Patient Endpoints

```
GET    /api/patients         - Get all patients
GET    /api/patients/:id     - Get specific patient
PUT    /api/patients/:id     - Update patient profile
POST   /api/patients/request - Create blood request
```

### Emergency Endpoints

```
GET    /api/emergency        - Get emergency requests
POST   /api/emergency        - Create emergency request
PUT    /api/emergency/:id    - Update emergency status
DELETE /api/emergency/:id    - Cancel emergency request
```

### Chat Endpoints (WebSocket)

```
SOCKET join_room             - Join a chat room
SOCKET send_message          - Send a message
SOCKET receive_message       - Receive messages
```

---

## 🖼️ Screenshots

### Homepage
Modern landing page with statistics, features, and call-to-action sections.

### Donor Dashboard
Personalized dashboard showing donation history, emergency alerts, and availability status.

### Emergency Requests
Real-time emergency blood request listing with urgency indicators.

### Admin Panel
Comprehensive analytics and system management interface.

---

## 🚀 Deployment

### Heroku Deployment

1. **Create Procfile**
   ```
   web: gunicorn --worker-class eventlet -w 1 app:app
   ```

2. **Deploy**
   ```bash
   heroku create your-app-name
   heroku addons:create heroku-postgresql:hobby-dev
   git push heroku main
   heroku run flask db upgrade
   ```

### AWS Deployment

1. **Using Elastic Beanstalk**
   - Create EB application
   - Configure environment variables
   - Deploy with EB CLI

2. **Using EC2**
   - Set up EC2 instance
   - Install dependencies
   - Configure Nginx/Apache
   - Run with Gunicorn

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add: description of your feature"
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request**

### Coding Standards
- Follow PEP 8 style guide for Python code
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Comment complex logic

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 LifeLink Blood Bank

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🆘 Support

### Getting Help

- **Documentation**: Check this README and code comments
- **Issues**: [GitHub Issues](https://github.com/yourusername/lifelink-blood-bank/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/lifelink-blood-bank/discussions)

### Reporting Bugs

Please include:
- Detailed description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, etc.)

---

## 🙏 Acknowledgments

- **Flask Community**: For the excellent framework and extensions
- **Contributors**: Thanks to all who have contributed to this project
- **Blood Donors**: For their life-saving contributions worldwide

---

## 📊 Project Stats

- **Language**: Python
- **Framework**: Flask
- **Database**: SQLAlchemy
- **Version**: 1.0.0
- **Status**: Active Development

---

<div align="center">

**Made with ❤️ for saving lives**

[⬆ Back to Top](#-lifelink---blood-bank-management-system)

</div>