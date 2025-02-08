from django.shortcuts import render
from .models import Post, PostReaction
from .forms import PostForm, UserRegistrationForm, CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q, Count
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')

def post_list(request):
    search_query = request.GET.get('search', '')

    my_posts = request.GET.get('my_posts') == 'on'
    
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)

    posts = Post.objects.all()

    if my_posts:
        posts = posts.filter(owner=request.user)

    if search_query:
        posts = Post.objects.filter(title__icontains=search_query)

    if min_price is not None and max_price is not None:
        posts = posts.filter(price__gte=min_price, price__lte=max_price)

    posts = posts.annotate(
        upvotes_count=Count('reactions', filter=Q(reactions__reaction_type=1)),
        downvotes_count=Count('reactions', filter=Q(reactions__reaction_type=0))
    ).order_by('-created_at')

    # posts = posts.order_by('-created_at')

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

def post_view(request, post_id):
    post = Post.objects.filter(pk=post_id).annotate(
        upvotes_count=Count('reactions', filter=Q(reactions__reaction_type=1)),
        downvotes_count=Count('reactions', filter=Q(reactions__reaction_type=0))
    ).first()

    if request.method == 'POST' and 'comment' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_view', post_id=post.id)
    else:
        form = CommentForm()

    comments = post.comments.all()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

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

@login_required
def post_reaction(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    reaction_type = int(request.POST.get("reaction_type"))

    reaction, created = PostReaction.objects.get_or_create(post=post, user=user)

    if reaction.reaction_type == reaction_type:
        reaction.reaction_type = -1
    else:
        reaction.reaction_type = reaction_type

    reaction.save()

    upvotes = PostReaction.objects.filter(post=post, reaction_type=1).count()
    downvotes = PostReaction.objects.filter(post=post, reaction_type=0).count()

    return JsonResponse({"upvotes": upvotes, "downvotes": downvotes, "user_reaction": reaction.reaction_type})
