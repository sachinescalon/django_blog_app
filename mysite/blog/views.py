from django.shortcuts import render,get_object_or_404
from django.http import  Http404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

# Create your views here.
def post_list(request):
    # posts=Post.published.all()
    post_list=Post.published.all()

    paginator=Paginator(post_list,2)
    page_number=request.GET.get('page',1)
    # posts=paginator.page(page_number)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    context={
        'posts':posts
    }
    return render(request,template_name='blog/post/list.html',context=context)


# def post_detail(request, id):
#     # try:
#     #     post = Post.published.get(id=id)
#     # except Post.DoesNotExist:
#     #     raise Http404("No Post found.")
#     post = get_object_or_404(Post,id=id,status=Post.Status.PUBLISHED)
#     context={'post': post}
#     return render(request,'blog/post/detail.html',context=context)

#SEO Friendly URL Genration in form of  /blog/2022/1/1/who-was-django-reinhardt/
def post_detail(request, year, month, day,post ):
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,slug=post,publish__year=year,publish__month=month,publish__day=day)
    context={'post': post}
    return render(request,'blog/post/detail.html',context=context)

#class Based View for post_list view function written above
class PostListView(ListView):
    """
    Alternative post list view
    """

    # model=Post
    queryset = Post.published.all()
    #We use queryset to use a custom QuerySet instead of retrieving all objects. Instead of defining a queryset attribute, we could have specified model = Post and Django would have built the generic Post.objects.all() QuerySet for us.
    
    
    #We use the context variable posts for the query results. The default variable is object_list if you don’t specify any context_object_name.
    context_object_name = 'posts'

    #We define the pagination of results with paginate_by, returning three objects per page.
    paginate_by = 2

    #We use a custom template to render the page with template_name. If you don’t set a default template, ListView will use blog/post_list.html by default.
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = EmailPostForm()
    # print(f'form_{form}')
    sent=False
    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
        # Form fields passed validation
            cleaned_data = form.cleaned_data
            print(f'cleaned_data_{cleaned_data}')
            post_url = request.build_absolute_uri(
            post.get_absolute_url())
            print(f'absolute_url_{post.get_absolute_url()}')
            print(f'post_url_{post_url}')

            subject = f"{cleaned_data['name']} recommends you read " \
            f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cleaned_data['name']}\'s comments: {cleaned_data['comments']}"
            mail_output=send_mail(subject, message, 'sachindahda.escalon@gmail.com',
            [cleaned_data['to']])
            print(f'mail_output_{mail_output}')
            sent = True
        # ... send email
    return render(request, 'blog/post/share.html', {'post': post,
    'form': form,'sent': sent})