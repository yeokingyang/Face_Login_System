from django.shortcuts import render, redirect
from django.conf import settings
from .models import *
from FaceLogin.Face_Recognition.face_reco import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            userAccount = UserAccount.objects.get(username=username, password=password)
            if userAccount.username == 'admin' and userAccount.password == 'admin':
                return redirect("/show")
            else:
                FRmodel = ini_model()
                user_db = ini_user_database()
                name = username
                verified = do_face_recognition_webcam(user_db, FRmodel, name)
            if verified:
                return redirect("/succeed")
            else:
                return redirect("/failed")
        except UserAccount.DoesNotExist:
            return redirect("/failed")
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            userAccount = UserAccount.objects.get(username=username)
            return redirect("/failed")
        except:
            FRmodel = ini_model()
            user_db = ini_user_database()
            if add_user_webcam(user_db, FRmodel, username, password):
                return redirect("/succeed")
            else:
                 return redirect("/failed")
    return render(request, 'register.html')

def succeed(request):
    return render(request, "succeed.html")

def failed(request):
    return render(request, "failed.html")

def show(request):
    userAccounts = UserAccount.objects.all()
    return render(request, 'show.html', { 'userAccounts' : userAccounts })

def delete(request, id):  
    userAccount = UserAccount.objects.get(id=id)  
    userAccount.delete()
    user_db = ini_user_database()
    delete_user(user_db, userAccount.username)
    return redirect("/show")  
