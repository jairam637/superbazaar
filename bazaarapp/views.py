from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm, UserForm
import json
import urllib
from django.shortcuts import render, redirect
from django.urls import reverse

# from accounts.forms import RegistrationForm, EditProfileForm
from django.http import JsonResponse

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout
from django.shortcuts import redirect
from . import models as mod
# -------------------------------------------------------------------

from . import models
from django.contrib.auth.models import Group


def index(request):
    return HttpResponse("output got")


def login1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            s = list(user.groups.all())
            if list(user.groups.all())[0].name == "cashier":
                return redirect('cashier1')
            elif list(user.groups.all())[0].name == "customer":
                print("Fund a customer")
            else:
                return render(request, 'register.html', {})
        else:
            form = UserForm()
            return render(request, 'login.html', {'form': form})
    form = UserForm()
    return render(request, 'login.html', {'form': form})


# ------------------------------------------------------------------------

def logout_view(request):
    logout(request)
    return redirect('login')

def cashier_group_check(request):
    user = User.objects.get(id=request.id)
    if list(user.groups.all())[0].name == "cashier":
        return True
    else:
        return False

def manager_group_check(request):
    user = User.objects.get(id=request.id)
    if list(user.groups.all())[0].name == "manager":
        return True
    else:
        return False


@login_required(login_url="/bazaarapp/login")
@user_passes_test(manager_group_check, login_url="bazaarapp/login")
def register(request):
    
    if request.method == 'POST':
        form = models.MyRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            user_id = list(User.objects.filter(username=username)
                          .values('id'))[0]['id']
            usertable = models.UserTable()
            usertable.user_id = request.POST.get(request.user.id)
            usertable.mobile = request.POST.get('mobile')
            usertable.address = request.POST.get('address')
            usertable.state = request.POST.get('state')
            usertable.pincode = request.POST.get('pincode')
            usertable.country = request.POST.get('country')
            usertable.user_id_id = user_id
            # if list(user.groups.all())[0].name == "manager":
            my_group = Group.objects.get(name='cashier')
            client = list(User.objects.filter(username=username))[0]
            client.groups.add(my_group)
            # elif list(user.groups.all())[0].name == "cashier":
            #     my_group = Group.objects.get(name='customer')
            #     client = list(User.objects.filter(username=username))[0]
            #     client.groups.add(my_group)
            usertable.save()
            return HttpResponse("User is registered as cashier")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {})
    
@login_required(login_url="/bazaarapp/login")
@user_passes_test(cashier_group_check, login_url="/bazaarapp/login")
def cashier1(request):
    # if request.session.keys():
    user_id = request.session["_auth_user_id"]
    # else:
        # return redirect('login')
    row = list(User.objects.filter(id=user_id))
    # if list(row[0].groups.all())[0].name != "cashier":
    #     raise HttpResponse("not accesable")
    return render(request, 'cashier.html', {})


def get_catagories(request):
    dictionary = mod.get_catagories()
    # print(dictionary.items())
    return JsonResponse(dictionary)


def get_brands(request, catagory):
    dictionary = mod.get_brands(catagory)
    return JsonResponse(dictionary)


def get_item(request, catagory, brand):
    dictionary = mod.get_item(catagory, brand)
    return JsonResponse(dictionary)


def store_data(request):
    x = request.POST
    post_data = dict(request.POST.lists())
    print(post_data)
    myDict = request.POST.dict()
    dictionary = mod.store_transaction(post_data)
    return JsonResponse(dictionary)
# def item_sold(request):
#     catagory_dictionary = mod.get_catagories()
#     catagories = catagory_dictionary['item_category']
#     dictionary = get_item_sold()
#     return dictionary
