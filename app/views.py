from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from .models import Customer
from random import randint

# Create your views here.




def index(request):
    return render(request,"app/index.html")


def user_login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            a1 = Customer.objects.get(username=username)
        except:
            messages.add_message(request,messages.INFO,f"Invalid username!!!")
            return redirect("user_login")



        if not check_password(password,a1.password):
            messages.add_message(request,messages.INFO,f"Invalid Password for {username}!!!")
            return redirect("user_login")

        request.session["logged_in"] = True
        request.session["username"] = username 
        return redirect("dashboard")
    return render(request,"app/login.html")

def user_register(request):
    if request.method == "POST":
        name = request.POST["name"]
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        gender = request.POST["gender"]
        password = make_password(request.POST["password"])


        request.session["name"] = name
        request.session["username"] = username
        request.session["email"] = email
        request.session["phone"] = phone
        request.session["address"] = address
        request.session["gender"] = gender
        request.session["password"] = password
        
        otp = verify(request)
        request.session["user_otp"] = otp

        return render(request,"app/verify.html",{"email":email})  
    elif request.method == "GET":
        return render(request,"app/register.html")


def verify(request):
    otp = randint(111111,999999)
    username = request.session["username"]
    email = request.session["email"]
    subject = "Email verification"
    body = f"OTP for username:{username} is\n {otp}"
    send_mail(subject,body,'forworkdewas@gmail.com',[email],fail_silently=False)
    return otp



def user_verify(request):
    if request.method=="POST":
        name = request.session["name"] 
        username = request.session["username"]
        email = request.session["email"] 
        phone = request.session["phone"] 
        address = request.session["address"]
        gender = request.session["gender"]
        password = request.session["password"]
        otp = request.POST["entered_otp"]
    

        if int(otp) == request.session["user_otp"]:
            try:
                Customer.objects.create(name=name,username=username,email=email,phone=phone,address=address,gender=gender,password=password)
            except Exception as e:
                messages.add_message(request,messages.INFO,"User Cannot be created invalid field!!!!")
                return redirect("user_register")
            else:
                send_mail("Account created successfully",f"Welcome {(name.title())},\n An account with username {username} is created.","forworkdewas@gmail.com",[email],fail_silently=False)
                request.session.flush()
            messages.add_message(request,messages.INFO,"User Created")
            return render(request,"app/login.html")
        else:
            messages.add_message(request,messages.INFO,"Wrong OTP Entered!!!!")
            return render(request,"app/verify.html",{"email":email}) 
        

def dashboard(request):
    if request.session.get("logged_in",False):
        username = request.session["username"]
        return render(request,"app/dashboard.html",{"username":username})
    return redirect("user_login")

def logout(request):
    request.session.flush()
    return redirect("user_login")
