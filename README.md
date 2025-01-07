# Blogging Platform API

This project is a Blogging Platform API built with Django and Django REST Framework. It allows users to create, read, update, and delete blog posts, and includes user management features such as authentication. The platform also supports filtering blog posts by categories, tags, and authors.

## Project Setup

Follow these steps to set up the project locally:

1. Create a Repository on GitHub
Create a new repository on GitHub called `Blogging_Platform` and clone it to your local machine:
git clone https://github.com/jacinta25/Blogging_Platform.git

2. Create and Activate a Virtual Environment
To create a virtual environment and install the required dependencies:
python -m venv venv
source venv/Scripts/activate

3. Install Dependencies
Install Django and other required packages:

4. Create the Project
Create the Django project and necessary apps:

django-admin startproject blogging_platform
cd blogging_platform
python manage.py startapp blog
python manage.py startapp users
python manage.py startapp api

5. Migrate Database
Apply the initial migrations to set up the database:
python manage.py migrate

6. Run the Development Server
Run the server to check if everything is working:
python manage.py runserver
Visit http://127.0.0.1:8000/ to see your project running.

7. Project Structure
1. Blog App
The blog app handles everything related to blog posts, categories, and tags. The core logic of this app is implemented in the models.py file where we define the structures of the blog-related data. This app provides the models necessary for the blog posts to be stored and managed in the database.

2. Users App
The users app handles user authentication and management. It is primarily responsible for:
User: Manages user-related information (username, email, password).
Usage: This app helps manage user registration, login, and profiles. It works closely with the authentication system (JWT) to ensure secure access to the platform.

3. API App
The api app is the most critical part of the application, as it exposes all the API endpoints that allow the front-end to interact with the blog posts and users. This app contains various files that handle different aspects of the API logic:

serializers.py: Converts the models.py data into JSON format so that it can be easily consumed by API clients (such as frontend apps or external services).
views.py: Contains the logic for handling the HTTP requests (e.g., GET, POST, PUT, DELETE) for creating, retrieving, updating, and deleting blog posts. These views are connected to the URL routing system.
filters.py: Implements custom filtering for API queries, allowing users to filter blog posts based on categories, tags, and authors.
signals.py: Manages signals that trigger certain actions in response to events, like when a new blog post is created or updated.
urls.py: Defines the API endpoint routes that map to views, allowing users to access and perform actions on blog posts and user data.
permissions.py: Custom permission classes that enforce access control, ensuring that only authorized users can perform actions like creating, editing, or deleting posts.

8. Technologies Used
Django: A high-level Python web framework for building the backend and handling all logic for the application.
Django REST Framework (DRF): A powerful toolkit used to expose the API and handle the serialization of the models into JSON format.
SQLite: The default database for local development (could be swapped out with PostgreSQL for production).
JWT (JSON Web Token): Used for token-based user authentication and authorization.
Python: The programming language used for the project.
Dependencies
To install the required dependencies:
pip install -r requirements.txt
-Dependencies in requirements.txt:

asgiref==3.8.1
cffi==1.17.1
cryptography==44.0.0
Django==5.1.4
django-filter==24.3
django-markdownx==4.0.7
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.1
Markdown==3.7
mysqlclient==2.2.6
pillow==11.1.0
pycparser==2.22
PyJWT==2.10.1
sqlparse==0.5.2
tzdata==2024.2


9. Features
1. Blog Post Management (CRUD)
Create, Read, Update, and Delete blog posts.
Each blog post includes attributes like title, content, author, category, and tags.
Validation for required fields like title and content.
2. User Management (CRUD)
Implement CRUD operations for users.
Only authenticated users can create, update, or delete their blog posts.
3. Search and Filter Blog Posts
Users can search blog posts by title, content, author, and tags.
Posts can be filtered by category and published date.
4. Authentication
Users must authenticate with JWT tokens to create, update, or delete posts.

