from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from activity.utils import create_action
from activity.models import Action
from .forms import LoginForm, RegisterForm, EditUserForm, EditProfileForm
from .models import Profile, Follow

User = get_user_model()

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

    return render(request, 'user/login.html', {'form': form})

@login_required
def user_list(request):
    # TODO change filter to order by author
    users = User.objects.filter(
        is_active=True
    ).exclude(username=request.user.username)

    return render(
        request,
        'user/dashboard/list.html',
        {
            'section': 'authors',
            'users': users
        }
    )

@login_required
def user_detail(request, username):
    user = get_object_or_404(
        User,
        username=username,
        is_active=True
    )
    
    return render(
        request,
        'user/dashboard/detail.html',
        {
            'section': 'profile',
            'user': user,
        }

    )

"""
    TODO: change the user_dashboard when making mods to 
    the dashboard section. switch dashboard with the activity
    tab
"""
@login_required
def user_dashboard(request):
    # display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list(
        id, flat=True
    )

    if following_ids:
        # if user is following other retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related(
            'user', 'user__profile'
        ).prefetch_related('target')[:10]
    return render(
        request,
        'user/dashboard/base.html',
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
            create_action(request.user, 'created an account')
            Profile.objects.create(user=new_user)
            return render(
                request,
                'user/register_done.html',
                {'new_user': new_user}
            )
    else:
        form = RegisterForm()

    return render(
        request,
        'user/register.html',
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
            messages.success(
                request,
                'Profile changed successfully'
            )
        else:
            messages.error(
                request,
                'Error updating your profile'
            )

    else:
        user_edit_form = EditUserForm(instance=request.user)
        profile_edit_form = EditProfileForm(instance=request.user.profile)
    
    return render(
        request,
        'user/user_edit.html',
        {
            'user_form': user_edit_form,
            'profile_form': profile_edit_form
        }
    )

@login_required
def user_follow(request, username):
    user_to = get_object_or_404(
        User,
        username=username,
    )
    follow_exists = Follow.objects.filter(
        user_from=request.user,
        user_to=user_to
    ).exists()
    
    if user_to != request.user:
        if not follow_exists:
            Follow.objects.get_or_create(
                user_from=request.user,
                user_to=user_to
            )
            create_action(request.user, 'is following', user_to)
        else:
            Follow.objects.filter(
                user_from=request.user,
                user_to=user_to
            ).delete()

    # TODO:Add render response for only the profile card
    # to update the follow count and follow button
    return render(request, 'snippets/follow.html', {'user': user_to})