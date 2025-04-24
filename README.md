# 🎟️ Ticket Booking System

A web-based ticket booking system for managing shows, seat selections, and user bookings. Built with Django, Dockerized for easy deployment, and integrated with Jenkins for CI/CD automation.

---

## 📌 Project Overview

This application allows users to:
- Register and log in to their account
- View available shows and details
- Select showtimes and reserve seats
- Manage their bookings
- Admins can manage shows, showtimes, and bookings from a custom admin panel

---

## 🛠️ Tech Stack Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (Bootstrap)
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **CI/CD**: Jenkins
- **Authentication**: Django’s built-in auth system
- **Others**: Gunicorn (for production), Whitenoise (for static files)

---

## ⚙️ Setup & Run Instructions

### 🔧 Prerequisites
- Docker
- Docker Compose
- Git

### 🚀 Quickstart

```bash
# Clone the repository
git clone https://github.com/tailormst/SL-3-Ticket_Booking_APP
cd ticket_booking_system

# Build and run the containers
docker-compose up --build

# Create superuser (optional)
docker-compose exec web python manage.py createsuperuser

# Access the app
Visit http://localhost:8000
```

# 🐳 Running Without Docker
## Create virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

## Install dependencies
pip install -r requirements.txt

## Run migrations
python manage.py migrate

## Create superuser
python manage.py createsuperuser

## Run the server
python manage.py runserver

```

# 📸 Screenshots

![Screenshot (523)](https://github.com/user-attachments/assets/57d868e6-f6e4-42ac-bf99-4a2c22019d0a)
![Screenshot (525)](https://github.com/user-attachments/assets/54e63686-2c1c-4494-816f-350003816b61)
![Screenshot (526)](https://github.com/user-attachments/assets/b1ba5c74-6c31-455e-862c-58bc802a4ebb)
![Screenshot (527)](https://github.com/user-attachments/assets/04fb2d24-4ead-4f4f-888b-9e8c6b6a7051)
![Screenshot (528)](https://github.com/user-attachments/assets/a837bcbb-bc85-4c9b-b612-736a060cd4e9)
![Screenshot (529)](https://github.com/user-attachments/assets/f8e79a0d-349c-4774-a29a-96f11bae610e)

# 🐳 Docker Usage
Dockerfile and docker-compose.yml are configured to:

Run the Django app with Gunicorn

Use a separate PostgreSQL container

Automatically collect static files

To restart the service:

docker-compose down
docker-compose up --build

# ⚙️ Jenkins Usage
Jenkinsfile included for automating the build and test process.

Example stages:

Pull latest code

Build Docker image

Run tests

Deploy to Docker container

Ensure Jenkins is set up to trigger on push to the repository and Docker is installed on the Jenkins host.

# 📂 Project Structure
```

ticket_booking_system/
├── bookings/              
├── shows/                 
├── users/                 
├── admin_panel/           
├── templates/             
├── static/                
├── ticket_booking/        
├── Dockerfile             
├── docker-compose.yml     
├── Jenkinsfile            
├── requirements.txt       
└── manage.py

```

# 📄 License
This project is licensed under the MIT License.
