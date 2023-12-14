# PocketTracker

The Pocket Tracker App is a simple tool designed to help you manage and monitor your expenses efficiently

## Features
- Add, edit and delete expenses
* Categorize expenses
+ Simple visual graphs for expense categories
* Filter and view specific expenses based on criteria such as date, category, or amount
- User registration and authentication
+ Password reset

## Technologies Used
**Frontend:**
- HTML
+ CSS
* JavaScript
- Bootstrap

**Backend:**
- Django(Python Web Framework)

**Database:**
- PostgreSQL

## Getting Started

1. Clone the repository
 
```
git clone https://github.com/babafemiolatona/pocket-tracker.git
```

3. Navigate to the project directory

```
cd pocket-tracker
```
   
4. Create a virtual environment and activate it

```
python -m venv venv
   
venv\scripts\activate(Windows)

source venv/bin/activate(Linux/Ubuntu)
```
5. Install Dependencies

```
pip install -r requirements.txt
```

6. Create a PostgreSQL database and add the database credentials to the .env.example file

7. Copy the environment variables template to create your configuration file
```
cp .env.example .env
```

8. Run database migrations

```
python manage.py makemigrations
python manage.py migrate
```

9. Start the development server
```
python manage.py runserver
```

10. Access the application through http://localhost:8000/
