from django.urls import path 
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    path('', views.indexView, name='home'),
    path('feed/', views.feedView, name='feed'),
    path('notifications/', views.notificationsView, name='notifications'),
    path('create_post/', PostCreate.as_view(), name='create_post_url'),
    path('recomend/', views.recomendView, name='recomend'),
    path('like/', views.like_post, name='like_url'),
    path('profile/<usname>', views.profileView, name='profile'),

    path('publication/<pub_id>', views.publicationView, name='publication'),
    path('publication_delete/<pub_id>', views.publicationDeleteView, name='pub_delete'),
    path('delete_ready/<pub_id>', views.publicationDeleteReadyView, name='delete_ready'),
    path('delete_cancel/<pub_id>', views.publicationDeleteCancelView, name='delete_cancel'),

    path('profile/profile_edit/', ProfileEdit.as_view(), name='profile_edit'),
    path('profile/<int:other_user>/subscribe', views.subscription_process, name='subscription'),
    path('login/', views.loginView, name='login_url'),
    path('register/', views.registerView, name='register_url'),
    path('logout/', LogoutView.as_view(next_page='/login'), name='logout'),
]
