from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from taggit.models import Tag
from django.db.models import Count 
from .models import Post
from .forms import EmailPostForm, CommentForm

# Create your views here.
# функция пагинатора для отображения статей
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags=tag)

    items_per_page = int(request.GET.get('items_per_page', 2))
    paginator = Paginator(object_list.order_by('id'), items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not page_obj.object_list:
        messages.info(request, 'No posts available')

    context = {
        'posts': page_obj.object_list,  # Передаем только объекты текущей страницы
        'page_obj': page_obj,                # Передаем сам объект страницы
        'request': request,
        'tag': tag
    }
    
    return render(request, 'spaceposts/list.html', context)



# отображение деталей поста
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm(initial={
        'name': request.user.username,  
        'email': request.user.email     
    }) 
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('spaceposts:post_detail', year=year, month=month, day=day, post=post.slug)

    post_tags_ibs = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ibs).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    context = {
        'post': post,
        'comments': comments, 
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts  
    }

    return render(request, 'spaceposts/detail.html', context)


# функция отправки постов
def post_share(request, post_id):
    # получение статьи по id
    post = get_object_or_404(Post, id=post_id, status='published')
    form = EmailPostForm(initial={
        'name': request.user.username,  
        'email': request.user.email     
    })
    sent = False
    context = {
            'post': post,
            'form': form,
            'sent': sent
        }

    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            # отправка поста
            post_url = request.build_absolute_uri(post.get_absolute_url())  
            subject = f"{cd['name']} ({cd['email']}) recommends you reading '{post.title}'"
            message = f'Read "{post.title}" at {post_url}\n\n{cd["name"]}\'s comments:\n{cd["comments"]}' 
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
        else:
            form = EmailPostForm()
        
    return render(request, 'spaceposts/share.html', context)
