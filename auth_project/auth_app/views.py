from django.shortcuts import render
from auth_app.forms import UserForm,UserProfileInfoForm

#imports for creating log in Page
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'auth_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are now logged in!!")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered=False

    if request.method=="POST":
            user_form = UserForm(data=request.POST)
            profile_info_form = UserProfileInfoForm(data=request.POST)

            if user_form.is_valid() and profile_info_form.is_valid():

                user = user_form.save()
                user.set_password(user.password)
                user.save()

                profile=profile_info_form.save(commit=False)
                profile.user=user

                if 'picture' in request.FILES:
                    profile.picture=request.FILES['picture']

                profile.save()
                registered=True
            else:
                    print(user_form.errors,profile_info_form.errors)

    else:
            user_form =UserForm()
            profile_info_form=UserProfileInfoForm()

    return render(request,'auth_app/registration.html',{'user_form':user_form,
                    'profile_info_form': profile_info_form,
                    'registered':registered})


def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        #authenticate returns the user object that we store in "user"
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account not active,please log in.")

        else:
            print('Someone tried to login and failed')
            print('Username:{} and password : {}'.format(username,password))
            return HttpResponse("Invalid Login,please ensure the details are correct.")
    else:
        return render(request,'auth_app/login.html',{})
