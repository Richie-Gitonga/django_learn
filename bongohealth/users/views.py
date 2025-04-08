from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm, EditUserForm, EditProfileForm
from .models import Profile

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

@login_required
def user_dashboard(request):
    return render(
        request,
        'users/dashboard.html',
        {'section': 'dashboard'}
    )

def user_register(request):
    form = None

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            # create new user object
            new_user = form.save(commit=False)
            # save the password
            new_user.set_password(
                form.cleaned_data['password']
            )
            # save the user object
            new_user.save()
            # create user profile
            Profile.objects.create(user=new_user)
            return render(
                request,
                'users/register_done.html',
                {'new_user': new_user}
            )
    else:
        form = RegisterForm()

    return render(
        request,
        'users/register.html',
        {'form': form}
    )

def user_edit(request):
    user_edit_form = None
    profile_edit_form = None

    if request.method == 'POST':
        user_edit_form = EditUserForm(
            instance=request.user ,
            data=request.POST
        )
        profile_edit_form = EditProfileForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )

        if user_edit_form.is_valid and profile_edit_form.is_valid:
            user_edit_form.save()
            profile_edit_form.save()

    else:
        user_edit_form = EditUserForm(instance=request.user)
        profile_edit_form = EditProfileForm(instance=request.user.profile)
    
    return render(
        request,
        'users/user_edit.html',
        {
            'user_form': user_edit_form,
            'profile_form': profile_edit_form
        }
    )