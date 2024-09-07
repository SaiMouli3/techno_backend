
## Step 1: Clone the Repository

First, clone the project repository to your local machine:
git clone <repository-url>
Replace `<repository-url>` with the actual repository URL.

## Step 2: Navigate to the Project Directory

Change your working directory to the project folder:
cd <project-directory>
Replace `<project-directory>` with the name of your project folder.

## Step 3: Set Up the Virtual Environment

Create a virtual environment to manage project dependencies:
python3 -m venv venv


Activate the virtual environment:

- **For Linux/macOS:**
source venv/bin/activate

- **For Windows:**
venv\Scripts\activate
---

## Step 4: Install Dependencies

If a `requirements.txt` file exists in the project directory, install the necessary dependencies by running:
pip install -r requirements.txt

## Step 5: Configure the Database

The project is set up to use a MySQL database. The required configuration for the database is as follows:

```python
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
```

Make sure the database configuration is added to your `settings.py` file.

### Install MySQL Client

To interact with the MySQL database, you'll need to install the `mysqlclient` package:
pip install mysqlclient


## Step 6: Install Additional Dependencies

Ensure the following Django packages are installed for proper functionality:

1. **Django CORS Headers:**

 
   pip install django-cors-headers
  

2. **Django Import Export:**
pip install django-import-export
  

3. **Django REST Framework:**
pip install djangorestframework


## Step 7: Add Installed Apps

Add the following apps to the `INSTALLED_APPS` section of your `settings.py` file:

```python
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
```

---

## Step 8: Apply Migrations

To set up your database schema, apply migrations:
python manage.py migrate
---

## Step 9: Start the Development Server

Once everything is set up, you can run the Django development server:
python manage.py runserver

