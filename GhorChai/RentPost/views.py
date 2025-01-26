from django.shortcuts import render
from .models import Post
from .forms import PostForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


# Create your views here.
def index(request):
    return render(request, 'index.html')

def post_list(request):
    my_posts = request.GET.get('my_posts') == 'on'
    
    price_range = request.GET.get('price_range', '')
    min_price = None
    max_price = None

    if price_range:
        try:
            min_price, max_price = map(int, price_range.split('-'))
        except ValueError:
            pass

    posts = Post.objects.all()

    if my_posts:
        posts = posts.filter(owner=request.user)

    if min_price is not None and max_price is not None:
        posts = posts.filter(price__gte=min_price, price__lte=max_price)
    elif min_price is not None:
        posts = posts.filter(price__gte=min_price)
    elif max_price is not None:
        posts = posts.filter(price__lte=max_price)

    posts = posts.order_by('-created_at')

    return render(request, 'post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id, owner=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save(commit=False)
            form.owner = request.user
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)

    return render(request, 'post_form.html', {'form': form})

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id, owner=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'post_confirm_delete.html', {'post': post})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})