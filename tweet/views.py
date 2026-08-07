from django.shortcuts import render
from .models import Tweet, Profile, Follow, Like
from .form import TweetForm, UserRegistrationForm, ProfileForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request, 'index.html')


def tweet_list(request):
    tweets = Tweet.objects.all().order_by("-created_at")

    tweet_data = []

    for tweet in tweets:

        liked = False

        if request.user.is_authenticated:
            liked = Like.objects.filter(
                user=request.user,
                tweet=tweet
            ).exists()

        tweet_data.append(
            {
                "tweet": tweet,
                "liked": liked,
                "likes": tweet.likes.count(),
            }
        )

    return render(
        request,
        "tweet_list.html",
        {
            "tweet_data": tweet_data,
        },
    )

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form':form})


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk = tweet_id, user = request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form':form})



@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk= tweet_id, user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet':tweet})
    
    
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form':form})

@login_required
def profile(request):
    return redirect(
        "user_profile",
        username=request.user.username
    )

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    profile = Profile.objects.get(user=user)

    tweets = Tweet.objects.filter(
        user=user
    ).order_by("-created_at")

    tweet_data = []

    for tweet in tweets:

        liked = False

        if request.user.is_authenticated:
            liked = Like.objects.filter(
                user=request.user,
                tweet=tweet
            ).exists()

        tweet_data.append(
            {
                "tweet": tweet,
                "liked": liked,
                "likes": tweet.likes.count(),
            }
        )

    is_following = Follow.objects.filter(
        follower=request.user,
        following=user
    ).exists()

    followers = Follow.objects.filter(
        following=user
    ).count()

    following = Follow.objects.filter(
        follower=user
    ).count()

    return render(
        request,
        "profile.html",
        {
            "profile": profile,
            "tweet_data": tweet_data,
            "is_following": is_following,
            "followers": followers,
            "following": following,
        },
    )

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        "edit_profile.html",
        {
            "form": form
        }
    )

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if request.user != user_to_follow:
        Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

    return redirect("user_profile", username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)

    Follow.objects.filter(
        follower=request.user,
        following=user_to_unfollow
    ).delete()

    return redirect("user_profile", username=username)

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    Like.objects.get_or_create(
        user=request.user,
        tweet=tweet
    )

    return redirect("tweet_list")

@login_required
def unlike_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    Like.objects.filter(
        user=request.user,
        tweet=tweet
    ).delete()

    return redirect("tweet_list")