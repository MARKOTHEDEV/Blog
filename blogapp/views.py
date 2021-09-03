from django.shortcuts import render
from . import models
from django.views import generic




def index(request):
    # print(models.BlogPost.objects.get_random_post().author)
    all_posts = models.BlogPost.objects.get_posts_in_desc_order()

    context ={
        'random_post':models.BlogPost.objects.get_random_post(),
        '5popular_posts':models.BlogPost.objects.all().filter(is_popular=True)[0:5],
        '5trending_posts':models.BlogPost.objects.get_all_trending(5),
        '5recent_posts':models.BlogPost.objects.get_range_of_post(5),
        'latest_posts':models.BlogPost.objects.get_posts_in_desc_order(),
        'about_site':models.AboutSite.objects.get_site_about()
      }
    return render(request,'index.html',context)

# def create_comment(request):


class PostDetail(generic.DetailView):
    model = models.BlogPost
    template_name='blog-single.html'
    context_object_name ='blogpost'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paragraphs'] = self.get_object().blogparagraph_set.all()
        context['5popular_posts'] = models.BlogPost.objects.all().filter(is_popular=True)[0:5]
        context['about_site'] = models.AboutSite.objects.get_site_about()
        context['all_comment']= models.Comment.objects.filter(post=self.kwargs.get('pk'))
        return context