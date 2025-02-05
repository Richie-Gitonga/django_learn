from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from .models import Post
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import EmailPostForm

# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    #paginator with 5 posts per page
    # TODO: change to 12 for future semantic viewing

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        #if page number is not an integer, get the first page
        posts = paginator.page(1)
    except EmptyPage:
        #if page number is out of range, get last page of results
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )

def post_share(request, post_id):
    #retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False

    if request.method == "POST":
        #form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']})"
                f"recommends you read {post.title}"
            )
            message = (
                f"read {post.title} at {post_url} \n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent=True
        else:
            form = EmailPostForm()

        return render(
            request,
            'blog/post/share.html',
            {
                'post': post,
                'form': form,
                'sent': sent
            }
        )