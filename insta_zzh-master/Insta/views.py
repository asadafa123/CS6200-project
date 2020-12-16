from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render
from Insta.models import Post, Like, InstaUser, UserConnection, Comment
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from Insta.forms import CustomUserCreationForm
from annoying.decorators import ajax_request
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, query
from elasticsearch_dsl.query import FunctionScore
from elasticsearch_dsl.function import ScoreFunction as SF
#from imagekit.models.fields.files import ProcessedImageFieldFIle
from django.db.models.fields.files import ImageFieldFile
import os
from django.core.files import File  
from django.core.files.base import ContentFile
from django.utils import timezone
#from search import esCRUD
#es
#from elasticsearch import Elasticsearch, RequestsHttpConnection
#from rest_framework_elasticsearch import es_views, es_pagination, es_filters
#from .search_indexes import BlogIndex


# Create your views here.
class helloworld(TemplateView):
    template_name = 'test.html'

class PostsView(ListView):
    model = Post
    template_name = 'index.html'
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title',
            'article',
            'description',
            'image'
    ]
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

class PostUpdateView(UpdateView):
    model = Post 
    template_name = 'post_update.html'
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy("posts")

class UserDetailView(DetailView):
    model = InstaUser
    template_name = 'user_detail.html'

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")


class ExploreView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'explore.html'
    login_url = 'login'

    def get_queryset(self):
        return Post.objects.all().order_by('-posted_on')[:20]

class SearchView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'search_result.html'
    login_url = 'login'

    def get_queryset(self):
        return Post.objects.all().order_by('-posted_on')[:20]

def init_dataset(request):
    csvFile = open(os.path.join(os.getcwd(),"static\\flickr_dataset\\flickr30k_images\\results.csv"), "r", encoding = "utf-8")
    result = {}
    uuid = 0
    for line in csvFile:    
        if line.startswith('image_name'):
            continue
        item = [x.strip() for x in line.split('|')]
        if item[0] not in result:
            result[item[0]] = item[2]
        else:
            result[item[0]] += " " + item[2]
    csvFile.close()
    dataset = []
    random_doc =  open(os.path.join(os.getcwd(),"static\\flickr_dataset\\flickr30k_images\\WarAndPeace.txt"), "r", encoding = "utf-8")
    lines = random_doc.readlines()
    list_to_add = []
    #print(result.keys())
    for key in result:
        cur_user = InstaUser.objects.get(username = "test"+str(uuid % 10))
        #print("here")
        cur_pic_path = os.path.join(os.getcwd(), os.path.join("static\\flickr_dataset\\flickr30k_images\\flickr30k_images", key))
        f = open(cur_pic_path, "rb")
        cur_pic_content = f.read()
        f.close()
        cur_post = Post()
        cur_post.id = uuid
        cur_post.author = cur_user
        cur_post.description = result[key]
        cur_post.title = " ".join(lines[uuid].split(" ")[0:3])
        cur_post.article = lines[uuid+1]
        cur_post.posted_on = timezone.now()
        #print("here3")
        cur_post.image.save(key, ContentFile(cur_pic_content))
        #print("here4")
        #list_to_add.append(cur_post)
        uuid += 1
        print(str(uuid)," image added")
        #if uuid % 5000 == 2500:
        #    try:
        #        Post.objects.bulk_create(list_to_add)
        #        list_to_add = []
        #    except Exception:
        #        print(Exception)
        #   break
        
    return  render(request, "index.html")

def init_reset(request):
    Post.objects.all().delete()
    return render(request, "index.html")

def search(request):

    q = request.GET.get('q')
    choice = request.GET.get('choice')
    #client = Elasticsearch()
    #s = None
    #query = None
    if choice == "article-only":
        query = Q("function_score", score_mode = "sum"\
                ,query = Q({"multi_match": {"query": q, "fields": ["title", "article"], "fuzziness": "AUTO", "operator" : "or" }}))     
            
        pass
    if choice == "description-only":
        query = Q("function_score", score_mode = "sum"\
                ,query = Q({"multi_match": {"query": q, "fields": ["description"], "fuzziness": "AUTO", "operator" : "or"}}))
        pass
    if choice == "combine1":
        query = Q("function_score", score_mode = "sum",\
             query = Q({"multi_match": {"query": q, "fields": ["title", "article", "description"], "fuzziness": "AUTO", "operator" : "or"}}))
    if choice == "combine2":
        query = Q("function_score", score_mode = "sum",\
             query = Q({"multi_match": {"query": q, "fields": ["title", "article", "description^2"], "fuzziness": "AUTO", "operator" : "or"}}))
        pass
    if choice == "combine3":
        query = Q("function_score", score_mode = "sum",\
             query = Q({"multi_match": {"query": q, "fields": ["title^2", "article^2", "description"], "fuzziness": "AUTO", "operator" : "or"}}))
        pass
    #
    #if len(s) > 20:
    #    s = s[:20]
    s = Search().query(query).extra(min_score = -1)
    post_list = []
    print(s.to_dict())
    for hit in s:
        #print(hit.to_dict())
        if 'id' in hit.to_dict():
            post_list.append(Post.objects.get(pk = hit.to_dict()['id']))
    return render(request, 'search_result.html',{'object_list': post_list, 'choice' : choice})



@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }

@ajax_request
def toggleFollow(request):
    current_user = InstaUser.objects.get(pk = request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstaUser.objects.get(pk = follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator = current_user, following = follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator = current_user, follow_user_pk = follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result' : result,
        'type' : request.POST.get('type'),
        'follow_user_pk' : follow_user_pk
    }

@ajax_request
def addComment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk = post_pk)
    commenter_info = {}
    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username

        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }
        post.description += " " + comment_text
        post.save()
        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }

'''
class BlogView(es_views.ListElasticAPIView):
    es_client = Elasticsearch(hosts=['elasticsearch:9200/'],
                              connection_class=RequestsHttpConnection)
    es_model = BlogIndex
    es_filter_backends = (
        es_filters.ElasticFieldsFilter,
        es_filters.ElasticSearchFilter
    )
    es_filter_fields = (
        es_filters.ESFieldFilter('tag', 'tags'),
    )
    es_search_fields = (
        'tags',
        'title',
    )
    '''