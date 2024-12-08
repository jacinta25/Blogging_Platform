#Blogging Platform API
1. create a Repository on github- Blogging_Platform
2. clone the repository - git clone https://github.com/jacinta25/Blogging_Platform.git
3. create a virtual environment - python -m venv venv
4. access the virtual environment - source vern/Scripts/activate
5. install Django - pip install django
6. create the project - django-admin startproject blogging_platform
7. create the app - python manage.py startapp blog
8. add 'blog' app to setting.py INSTALLED APPS of the main project blogging_platform
9. run python manage.py migrate to save the changes