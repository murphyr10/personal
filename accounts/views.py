from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login
from .forms import RegistrationForm, UserEditForm ,UserProfileForm
from .token import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,  force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.models import User
from .models import Profile
from django.http import JsonResponse
from portal.models import Post,Notification
from django.urls import reverse


# Create your views here.


@login_required
def like(request):
    if request.method == 'POST':  # Ensure we're handling only POST requests
        post_id = int(request.POST.get('postid'))  # Get the post ID from the request
        post = get_object_or_404(Post, id=post_id)

        # Check if the user has already liked the post
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)  # Un-like the post
            post.like_count -= 1
            is_liked = False  # User has unliked the post
        else:
            post.likes.add(request.user)  # Like the post
            post.like_count += 1
            is_liked = True  # User has liked the post

            # Send notification after the post has been liked
            post_author = post.user  # The author of the post
            if post_author != request.user:  # Avoid notifying the post author
                message = f"Your post '{post.title}' has been liked."
                post_url = reverse('post_single', args=[post.id])  # URL for the post
                Notification.objects.create(user=post_author, message=message, url=post_url)

        post.save()  # Save the updated post with the new like count

        # Return the updated like count and the like status (is_liked)
        return JsonResponse({
            'result': post.like_count,
            'is_liked': is_liked  # Return if the post is liked by the current user
        })
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)



def avatar(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        avatar = Profile.objects.filter(user=user)
        context = {
            "avatar": avatar,
        }
        return context
      
      
    else:
        return {
            'NotLoggedIn': True  # Return a boolean flag or a string to indicate the user is not logged in
        }



@login_required
def profile(request):
    return render(request, 'accounts/profile.html',{'section':'profile'})





def accounts_register(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('registration/email_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = RegistrationForm()
    return render(request, 'registration/register.html', {'form': registerForm})






def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')
    

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)

        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    return render(request,
                  'accounts/update.html',
                  {'user_form': user_form, 'profile_form': profile_form})






@login_required
def delete_user(request):

    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        return redirect('accounts:login')

    return render(request, 'accounts/delete.html')
