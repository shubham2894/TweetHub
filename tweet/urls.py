from . import views
from django.urls import path

urlpatterns = [

    path('home/', views.index, name='index'),

    path('', views.tweet_list, name='tweet_list'),

    path('create/', views.tweet_create, name='tweet_create'),

    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),

    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),

    path('register/', views.register, name='register'),

    # Profile
    path('profile/', views.profile, name='profile'),

    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('profile/<str:username>/', views.user_profile, name='user_profile'),

    # Follow
    path('follow/<str:username>/', views.follow_user, name='follow_user'),

    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),

    # Like
    path('like/<int:tweet_id>/', views.like_tweet, name='like_tweet'),

    path('unlike/<int:tweet_id>/', views.unlike_tweet, name='unlike_tweet'),

]