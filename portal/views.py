from django.shortcuts import render, get_object_or_404 , HttpResponseRedirect,redirect
from.models import Post,Category
from .forms import NewCommentForm, PostForm ,PostSearchForm

from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q
from .models import Notification







@login_required
def home(request):
    posts=Post.objects.all()
    return render(request,'portal/index.html',{'post':posts})

def post_single(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    user_comment = None

    # Check if the request is AJAX by looking for the "X-Requested-With" header
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Handle form submission
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.user = request.user
            user_comment.save()

            # Return a JSON response with the new comment data
            return JsonResponse({
                'status': 'success',
                'comment': {
                    'username': user_comment.user.username,
                    'content': user_comment.content,
                    'publish': user_comment.publish.strftime('%Y-%m-%d %H:%M:%S')  # Format date as needed
                }
            })
        else:
            # If the form is invalid, send an error response
            return JsonResponse({'status': 'error', 'message': 'Invalid comment form.'})

    else:
        # Handle GET request (for displaying the post and comments)
        comment_form = NewCommentForm()

    return render(request, 'portal/single.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form=PostForm(request.POST, request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('index')
    else:
        form=PostForm()

    return render (request, 'portal/create_post.html', {'form':form})





class CatListView(LoginRequiredMixin,ListView):
    template_name= 'portal/category.html'
    context_object_name='catlist'

    def get_queryset(self):
        content ={
               'cat': self.kwargs['category'],
               'posts': Post.objects.filter(category__name=self.kwargs['category'])
            
        }
        return content
    

def category_list(request):
    category_list=Category.objects.exclude(name='default')
    context ={
        "category_list": category_list

}
    return context


def landing_page(request):
    return render(request,'portal/landing_page.html')




    



def post_search(request):
    form = PostSearchForm()
    q = ''
    c = ''
    results = []
    query = Q()

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']

            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__contains=q)

            results = Post.objects.filter(query)
    return render(request, 'portal/search.html',{'form': form, 'q': q, 'results':results})




def notifications_view(request):
    """Display notifications for the logged-in user."""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    
    # Mark notifications as read when user accesses the notifications page
    notifications.update(is_read=True)

    return render(request, 'portal/notifications.html', {
        'notifications': notifications,
        'unread_notifications': unread_notifications
    })

def mark_as_read(request, notification_id):
    """Mark a notification as read."""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')  # Redirect to notifications page