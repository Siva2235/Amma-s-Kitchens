from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Profile

# Create your views here.
def register(request):
    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        Username = request.POST['Username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if password == confirmPassword:
            if User.objects.filter(username=Username).exists():
                messages.error(request,'username  already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'email  already exists')
                return redirect('register')
            elif Profile.objects.filter(phone=phone).exists():
                messages.error(request, 'Mobile number already exists')
                return redirect('register')
            else:    
                user = User.objects.create_user(username=Username, first_name=firstName, last_name=lastName, email=email,password=password)
                user.save();

                profile = Profile.objects.create(user=user, phone=phone)
                profile.save()

                auth.login(request, user)
                messages.success(request, 'Account Created Successfully')
                return redirect('user_login')

        else:
            print('password is not matching')
            return redirect('register')    
    else:    
        return render(request,'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request, 'Login Successful')
            return redirect('user_login')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('user_login')
    else:      
     return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')