from django.urls import path
from . import views

urlpatterns = [
    path('',views.first, name='first'),
    path('home',views.home,name='home'),
    path('signup/',views.signup_view,name='signup'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('create_post',views.create_post,name='create_post'),
    path('like/<int:post_id>/',views.like_post, name='like_post'),
    path('comment/<int:post_id>/',views.comment_post, name='comment_post'),
    path('profile/<str:username>/',views.user_profile, name='user_profile'),
    path('profile/<str:username>/follow',views.follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow',views.unfollow_user, name='unfollow_user'),
    path('followers/<str:username>/', views.followers_list, name='followers_list'),
    path('following/<str:username>/', views.following_list, name='following_list'),
    path('post/<int:post_id>/delete/',views.delete_post, name='delete_post'),
    path('add_story/',views.add_story, name='add_story'),
    path('forgot_pass',views.forgot_pass, name='forgot_pass'),
    path('change_pass/<str:token>/',views.change_pass, name='change_pass'), 
]
