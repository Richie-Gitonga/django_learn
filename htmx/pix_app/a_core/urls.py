from django.contrib import admin
from django.urls import path
from a_posts.views import home_view, post_create_view, post_delete_view, post_update_view, post_page_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('post/create/', post_create_view, name='post-create'),
    path('post/delete/<pk>/', post_delete_view, name='post-delete'),
    path('post/edit/<pk>/', post_update_view, name='post-edit'),
    path('post/<pk>/', post_page_view, name='post'),
    path('category/<tag>/', home_view, name='category')
]
