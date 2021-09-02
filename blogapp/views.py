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
      }
    return render(request,'index.html',context)



class PostDetail(generic.DetailView):
    model = models.BlogPost
    template_name='blog-single.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context