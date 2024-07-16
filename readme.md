# Inventory
This is an inventory management system which helps businesses track and issue out products.
The system extends the django authentication system to separate the roles of each user in the system.

## Installation instructions
Create a virtual 

```python3 -m venv env```

Activate the virtual env

```source env/bin/activate```

Install the required packages

```pip install -r requirements.txt```

Start the server

```python manage.py runserver```

## Screenshots
![Login Screen!](sys/login.PNG "System login screen")

Login Screen

![User View!](sys/user_view.PNG "Normal user view")

User view

![Admin View!](sys/admin_view.PNG "Admin user view")

Admin user view


Here is a step-by-step guide to creating a simple Django application with login and signup pages using the command line interface (CLI).

Step 1: Set Up Your Environment
First, ensure you have Python and Django installed. If not, you can install them using:

sh
Copy code
pip install django
Step 2: Create a Django Project
Start by creating a new Django project. Open your terminal and run:

sh
Copy code
django-admin startproject myproject
cd myproject
Step 3: Create a Django App
Next, create a new Django app within your project. Run:

sh
Copy code
python manage.py startapp myapp
Step 4: Set Up Your App in the Project
Add the new app to your project’s settings. Open myproject/settings.py and add 'myapp' to the INSTALLED_APPS list:

python
Copy code
INSTALLED_APPS = [
    ...
    'myapp',
]
Step 5: Create User Model and Forms
We will use Django's built-in user model for authentication. Create forms for user registration and login.

In myapp/forms.py, add:

python
Copy code
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
Step 6: Create Views
In myapp/views.py, create views for signup and login:

python
Copy code
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, LoginForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
Step 7: Create URL Patterns
In myapp/urls.py, define the URL patterns for the views:

python
Copy code
from django.urls import path
from .views import signup_view, login_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
]
Include these URLs in your project’s main URL configuration. Edit myproject/urls.py to include myapp URLs:

python
Copy code
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
Step 8: Create Templates
Create templates for signup and login pages. In myapp/templates/, create signup.html and login.html.

signup.html:

html
Copy code
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
</head>
<body>
    <h2>Signup</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Signup</button>
    </form>
</body>
</html>
login.html:

html
Copy code
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Login</button>
    </form>
</body>
</html>
Step 9: Migrate the Database
Run the migrations to create the necessary database tables:

sh
Copy code
python manage.py migrate
Step 10: Run the Development Server
Finally, run the development server to see your application in action:

sh
Copy code
python manage.py runserver
Now, you should be able to visit http://127.0.0.1:8000/signup/ and http://127.0.0.1:8000/login/ to access your signup and login pages.
