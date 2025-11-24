from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request,"home.html")


def SignUp(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        password= request.POST.get("password")
        phone = request.POST.get("phone")
        #Basic Validations 
        if not name or not email or not password:
            messages.error(request,"Please Fill all Required Fields.")
            return redirect('sign_up')
        if len(password) < 6 :
            messages.error(request,"min. 6 character is required.")
            return redirect("sign_up")
        if User.objects.filter(username = email):
            messages.error(request,"User Already Exits!")
            return redirect("sign_up")
        
        user = User.objects.create_user(username=email,password=password)
        if " " in name: 
            first, last = name.split(" ",1)
        else:
            first, last = name, ""

        user.first_name, user.last_name = first, last
        user.save()

        #User Created
        UserProfile.objects.create(user = user , phone = phone )
        login(request,user)
        messages.success(request,"Account Created Sucessfully, Welcome!")
        return redirect("predict")
    return render(request,"signup.html")

from .ml.loader import prediction , load_bundle
@login_required
def PredictView(request):
    feature_order = load_bundle()["feature_cols"]
    result = None
    last_data = None

    if request.method == 'POST':
        data = {}
        try:
            for c in feature_order:
                data[c] = float(request.POST.get(c))
        except ValueError:
            messages.error(request,"Please enter valid value")
            return redirect('predict')
        label = prediction(data)
        
        Prediction.objects.create(user = request.user ,**data, predicted_label = label)
        result = label
        last_data =data
        messages.success(request,f"Recommended Crop: {label}")

    return render(request,"predict.html",locals())

@login_required
def LogoutView(request):
    logout(request)
    messages.success(request,"You have Logout Sucessfully")
    return redirect("login")


def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if not user:
            messages.error(request,"Invalid Login Credentials")
            return redirect("login")
        else:
            login(request,user)
            messages.success(request,"Logged in successfully")
            return redirect("predict")
    return render(request,"login.html")

@login_required
def UserHistoryView(request):
    predictions = Prediction.objects.filter(user=request.user)
    return render(request,"history.html",locals())

from django.shortcuts import get_object_or_404
@login_required
def UserHistoryDelete(request,id):
    p = get_object_or_404(Prediction,id=id,user=request.user)
    p.delete()
    messages.success(request,"Deleted Successfully")
    return redirect('user_history')

@login_required
def UserPro(request):
    profile = UserProfile.objects.get(user = request.user)
    full_name = request.user.get_full_name()
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        if name:
            parts = name.split(" ",1)
            request.user.first_name = parts[0]
            request.user.last_name = parts[1] if len(parts) > 1 else ""
        profile.phone = phone
        request.user.save()
        profile.save()
        messages.success(request,"Profile Updated!")
        
    return render(request,"profile.html",locals())

@login_required
def ChangePassword(request):
    if request.method == 'POST':
        old_pass = request.POST.get("current_password")
        new_pass = request.POST.get("new_password")
        con_pass = request.POST.get("con_password")
        if not request.user.check_password(old_pass):
            messages.error(request,"Current Password is Incorrect")
            return redirect('change_pass')
        if len(new_pass) < 6:
            messages.error(request,"New password must have atleast 6 characters ")
            return redirect('change_pass')
        if new_pass != con_pass:
            messages.error(request,"Passwords not Match")
            return redirect('change_pass')
        
        request.user.set_password(con_pass)
        request.user.save()
        user = authenticate(request,username=request.user.username,password=new_pass)
        if  user:
            login(request,user)
            messages.success(request,"Password Changed Sucessfully")
            return redirect("change_pass")
            
    return render(request,"change_pass.html")