from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from inqueries.models import Inquery

def register(request):
    if request.method =='POST':
        # Get form values -for every form submitted, we want to put it into variables 
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match -we want to do some validation 
        if password == password2:
            """if the passwords match, we do more validation"""
            #Check username, this means we have to bring in the user model. We check if the username exists in the database, if it does we return an error message and redirect the user to the register page.  
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect(register)
            else: 
                #if the username does not exist we check if email exists
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect(register)
                else: 
                    #looks good, create the user in the database
                    user = User.objects.create_user(username=username, password =password, email=email, first_name=first_name, last_name=last_name)
                    # Option 1 We can then login the user automatically to the dashboard. In this case, you have to bring in the auth  model which is part of django contrib
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect ('dashboard')
                    # Option 2 save the user and redirect them to the login page 
                    user.save()
                    messages.success(request, 'You are now logistered and can log in')
                    return redirect('register')
        else: 
            """if the passwords do not match, return an error message the redirect"""
            messages.error(request, 'Password Mismatch') 
            return redirect ('register')

    else:
        return render(request, 'accounts/register.html')

def login(request):

    if request.method =='POST':
       username = request.POST['username'] 
       password = request.POST['password'] 

       user = auth.authenticate(username = username, password = password)

       if user is not None:
           auth.login(request, user)
           messages.success(request, 'You are now logged in')
           return redirect ('dashboard')
       else:
           messages.error(request, 'Invalid Credentials')
    else:
        return render(request, 'accounts/login.html') 

def logout(request):
    if request.method =='POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')  

def dashboard(request):
    #you have to bring in the model 
    user_inqueries = Inquery.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'inqueries':user_inqueries
    }

    return render(request, 'accounts/dashboard.html',context)