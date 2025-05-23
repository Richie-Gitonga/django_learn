from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='users'


urlpatterns = [
#   prev login view
#    path('login', views.user_login, name='login')
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.user_register, name='user_register'),
    path('edit/', views.user_edit, name="user_edit"),
    path('', views.user_dashboard, name='dashboard'),
    path('users/all/', views.user_list, name='user_list'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('users/follow/<username>/', views.user_follow, name='user_follow'),
    # change password
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),
    # password resets
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done"
    ),
    path(
        'password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'password-reset/complete',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    )
]