from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile,Post,Like,Comment,Follow,Story,Notification
from .forms import ProfileForm,PostForm,CommentForm,StoryForm
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from .helpers import send_forget_pass_mail
import uuid
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def first(request):
       return render(request,'core/first.html')

@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    now=timezone.now()
    stories=Story.objects.filter(created_at__gte=now-timedelta(hours=24))
    for post in posts:
        post.is_liked = post.like_set.filter(user=request.user).exists()

    followers_count = 0
    following_count = 0

    if request.user.is_authenticated:
        followers_count = Follow.objects.filter(following=request.user).count()
        following_count = Follow.objects.filter(follower=request.user).count()

    return render(request, 'core/home.html', {
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'active_stories':stories
    })

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email=request.POST.get('email')
        if User.objects.filter(username=username).exists():
            return render(request, 'core/signup.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.get_or_create(user=user)
        login(request, user)
        return redirect('home')
    return render(request, 'core/signup.html')

def login_view(request):
          if request.method=='POST':
                username=request.POST['username']
                password=request.POST['password']
                user=authenticate(request,username=username,password=password)
                if user is not None:
                        login(request,user)
                        return redirect('home')
                else:
                        return render(request,'core/login.html',{'error':'Invalid Credentionals'}) 
          return render(request,'core/login.html')

def logout_view(request):
        logout(request)
        return redirect('login')

@login_required
def edit_profile(request):
          profile=request.user.profile
          if  request.method=='POST':
                form=ProfileForm(request.POST, request.FILES, instance=profile)
                if form.is_valid():
                        form.save()
                        return redirect('home')
          else:
                form=ProfileForm(instance=profile)    
          return render(request,'core/edit.html',{'form':form}) 
 
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'core/create_post.html', {'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()
    elif post.user != request.user:
        Notification.objects.create(
            sender=request.user,
            recipient=post.user,
            post=post,
            type='like',
            text=f"{request.user.username} liked your post"
        )
        notify_via_ws(
            post.user.id,
            {
                'text': f"{request.user.username} liked your post",
                'type': 'like'
            }
        )
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

            if post.user != request.user:
                Notification.objects.create(
                    sender=request.user,
                    recipient=post.user,
                    post=post,
                    comment=comment,
                    type='comment',
                    text=f"{request.user.username} commented on your post"
                )
                # WebSocket real-time notification
                notify_via_ws(post.user.id, {
                    'text': f"{request.user.username} commented on your post",
                    'type': 'comment'
                })
        return redirect('home')
    
@login_required
def user_profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user_obj)
    
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user_obj).exists()

    followers_count = Follow.objects.filter(following=user_obj).count()
    following_count = Follow.objects.filter(follower=user_obj).count()

    context = {
        'user_obj': user_obj,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'core/user_profile.html', context)

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        follow,created=Follow.objects.get_or_create(follower=request.user, following=user_to_follow)  
    return redirect('user_profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('user_profile', username=username)


def followers_list(request, username):
    user_obj = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(following=user_obj).select_related('follower')
    return render(request, 'core/followers_list.html', {
        'user_obj': user_obj,
        'followers': followers
    })

def following_list(request, username):
    user_obj = get_object_or_404(User, username=username)
    following = Follow.objects.filter(follower=user_obj).select_related('following')
    return render(request, 'core/following_list.html', {
        'user_obj': user_obj,
        'following': following
    })

@login_required
def delete_post(request, post_id):
     post=get_object_or_404(Post,id=post_id)
     if request.method=='POST':
          post.delete()
          return redirect('home')
     return render(request,'core/delete_post.html',{'post':post})

@login_required
def add_story(request):
    if request.method=='POST':
        form=StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story=form.save(commit=False)
            story.user=request.user
            story.save()
            return redirect('home')
    else:
         form=StoryForm()
    return render(request,'core/add_story.html',{'form':form})

def active_stories():
    now=timezone.now()
    return Story.objects.filter(created_at__gte=now-timedelta(hours=24))

def forgot_pass(request):
     try:
          if request.method=='POST':
               username=request.POST.get('username')

               if not User.objects.filter(username=username).exists():
                    messages.error(request,'No user found')
                    return redirect('forgot_pass/')
               user_obj=User.objects.get(username=username)
               token=str(uuid.uuid4())
               profile_obj=Profile.objects.get(user=user_obj)
               profile_obj.forget_pass_token=token
               profile_obj.save()
               send_forget_pass_mail(user_obj.email, token)
               messages.success(request,'An email is sent')
               return redirect('change_pass', token=token)
     except Exception as e:
          print(e)
     return render(request,'core/forgot_pass.html')

def change_pass(request, token):
    try:
        profile_obj = Profile.objects.get(forget_pass_token=token)
        user_obj = profile_obj.user 

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('change_pass', token=token)

            user_obj.set_password(new_password)
            user_obj.save()
            profile_obj.forget_pass_token = ''
            profile_obj.save()

            messages.success(request, 'Password reset successfully! You can now log in.')
            return redirect('login')

        return render(request, 'core/change_pass.html')

    except Profile.DoesNotExist:
        messages.error(request, 'Invalid or expired link.')
        return redirect('forgot_pass')

def notify_via_ws(user_id, message_dict):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",  
        {
            "type": "send_notification",
            "content": message_dict
        }
    )


