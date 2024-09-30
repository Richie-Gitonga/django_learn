from django.contrib import admin
from django.urls import path, include
from a_posts.views import home_view, post_create_view, post_delete_view, post_update_view, post_page_view
from a_users.views import profile_view, profile_edit_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('allauth.urls')),
    path('post/create/', post_create_view, name='post-create'),
    path('post/delete/<pk>/', post_delete_view, name='post-delete'),
    path('post/edit/<pk>/', post_update_view, name='post-edit'),
    path('post/<pk>/', post_page_view, name='post'),
    path('category/<tag>/', home_view, name='category'),
    path('profile', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile-edit')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)