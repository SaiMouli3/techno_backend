
1. Clone the repository:
**git clone <repository-url>**
2. Navigate to the project directory:
**cd <project-directory>**
3. Create a virtual environment and activate it:
**python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate  # For Windows**
4. Install the required dependencies:(If file exsists)
**pip install -r requirements.txt**

**python manage.py migrate**
Start the development server:
**python manage.py runserver**



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'techno$final_db1',
        'USER': 'techno',
        'PASSWORD': 'Mm@u7Sn)M3!quJL',
        'HOST': 'techno.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}

MYSQL DATABASE

**pip install mysqlclient**


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webapp.apps.WebappConfig',
    'corsheaders',
    'import_export',
    'rest_framework',
]
command to install these
**pip install django-cors-headers
pip install django-import-export
pip install djangorestframework**


After Installing these go to manage.py where it exsists
Run server
**python manage.py migrate**
**python manage.py runserver**


