from django.views import generic
from .models import Post, Images, FAQ
from django.forms import modelformset_factory
from django.contrib import messages
from .forms import CommentForm, PostForm, ImageForm, FAQForm, AnswerForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse,Http404

def PdfsView(request,name):
    try:
        return FileResponse(open(f'pdf/{name}.docx', 'rb'), content_type='application/docx')
    except FileNotFoundError:
        raise Http404()


def PostList(request):
    posts = Post.objects.all()  # fetching all post objects from database
    p = Paginator(posts, 5)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    
    return render(request, 'blogs/blog_home.html', {'page_obj': page_obj})

def FAQList(request):
    posts = FAQ.objects.all()  # fetching all post objects from database
    p = Paginator(posts, 5)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    
    return render(request, 'blogs/FAQ_list.html', {'page_obj': page_obj})
'''
class PostList(generic.ListView):
    
    queryset = Post.objects.filter(status=1).order_by('-created_at')
    
    template_name = 'blogs/blog_home.html'
'''

def faq_detail(request, slug):
    template_name = 'blogs/faq_detail.html'
    post = get_object_or_404(FAQ, slug=slug)
    comments = post.answers.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = AnswerForm(data=request.POST)
        if comment_form.is_valid():

            new_comment = comment_form.save(commit=False)
            
            # if request.user.is_authenticated:
            new_comment.created_by = request.user
            new_comment.active = True
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'faq': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})



def post_detail(request, slug):
    template_name = 'post_details.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    images = Images.objects.filter(post=post)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            new_comment = comment_form.save(commit=False)
            
            # if request.user.is_authenticated:
            new_comment.created_by = request.user
            new_comment.active = True
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'images': images,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

@login_required
def faq_create(request):
    if request.method == 'POST':
        creation_from = FAQForm(data=request.POST)
        #formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())
        if creation_from.is_valid():
            new_form = creation_from.save(commit=False)
            new_form.author = request.user
            new_form.save()
            return redirect('list-faq')
    else:
        creation_from = FAQForm()
    return render(request, 'blogs/FAQ.html',{'form' : creation_from})


@login_required
def post_create(request):
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)
    if request.method == 'POST':
        creation_from = PostForm(data=request.POST)
        files = request.FILES.getlist('images')
        #formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())
        if creation_from.is_valid():
            new_form = creation_from.save(commit=False)
            new_form.author = request.user
            if 'Publish' in request.POST:
                new_form.status = 1
            elif 'Draft' in request.POST:
                new_form.status = 0
            new_form.save()
            print("--",files,"--")
            for f in files:
                Images.objects.create(post = new_form, image=f)
            '''for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Image(post=new_form, image=image)
                    photo.save()
                else:
                    print("Upload faild\n\n\n\n")
                    '''
            messages.success(request, f"Post created successfully")
            return redirect('blog-home')
    else:
        creation_from = PostForm()
        #formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'blogs/post_create.html', {'postForm' : creation_from})


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_details.html'