from django.contrib import messages
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from . import models
from django.views import generic
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



def index(request):
    # print(models.BlogPost.objects.get_random_post().author)
    all_posts = models.BlogPost.objects.get_posts_in_desc_order()

    context ={
        'random_post':models.BlogPost.objects.get_random_post(),
        '5popular_posts':models.BlogPost.objects.all().filter(is_popular=True)[0:5],
        '5trending_posts':models.BlogPost.objects.get_all_trending(5),
        '5recent_posts':models.BlogPost.objects.get_range_of_post(5),
        'latest_posts':models.BlogPost.objects.get_posts_in_desc_order(),
        # 'about_site':models.AboutSite.objects.get_site_about(),
        'count_registered_emails':models.SavedNewsletterEmails.objects.count()
      }
    try:context.update({'random_post':models.BlogPost.objects.get_random_post(),'about_site':models.AboutSite.objects.get_site_about(),})
    except:context.update({'about_site':'',})
    return render(request,'index.html',context)


def filter_view(request,searchKeyword=None,categories=None):
    if searchKeyword != "None":
        print(searchKeyword)
        queryset = models.BlogPost.objects.filter(title__icontains=searchKeyword)
        print(queryset)
    elif categories != "None":
        category= models.Categories.objects.filter(slug__icontains=categories).first()
        queryset = models.BlogPost.objects.filter(categories=category)
    return render(request,'filter.html',{"results":queryset,
        'about_site':models.AboutSite.objects.get_site_about()
    
    })
def contactPage(request):
    "this renders the contact html"
    if request.method == 'POST':
        InputName = request.POST['InputName']
        InputEmail = request.POST['InputEmail']
        InputSubject = request.POST['InputSubject']
        InputMessage = request.POST['InputMessage']

        contact = models.ContactUs.objects.create(
            name=InputName,
            email= InputEmail,
            subject = InputSubject,
            message = InputMessage
        )
        contact.save()
        messages.success(request,f'Hey  {InputName} your Request Has Been Sent We will Get Back To you Soon')
    return render(request,'contact.html')

def create_comment(request,pk=None):
    name = request.POST['name']
    comment_text = request.POST['comment_text']
    post = models.BlogPost.objects.get(id=pk)
    new_comment = models.Comment.objects.create(post=post,name = name,comment_text=comment_text)
    new_comment.save()
    # print(reverse)
    return redirect(reverse('post-detail',kwargs={'pk':pk}))

def save_email_for_newsletter(request):
    if request.method == 'POST':
        email = request.POST['email']
        instance = models.SavedNewsletterEmails.objects.create(email=email)
        instance.save()
        messages.success(request,'Your Email Addresse Has Been saved successfully!!')
        
    return redirect(reverse('home'))


class PostDetail(generic.DetailView):
    model = models.BlogPost
    template_name='blog-single.html'
    context_object_name ='blogpost'
    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paragraphs'] = self.get_object().blogparagraph_set.all()
        context['5popular_posts'] = models.BlogPost.objects.all().filter(is_popular=True)[0:5]
        # context['about_site'] = models.AboutSite.objects.get_site_about()
        context['all_comment']= models.Comment.objects.filter(post=self.kwargs.get('pk'))
        context['num_of_comment'] = models.Comment.objects.count()
        context['postid'] = self.kwargs.get('pk')
        context['like_dislike_obj'] = self.get_object().bloglikes_set.all()
        context['count_registered_emails'] = models.SavedNewsletterEmails.objects.count()
        
        try:context.update({'random_post':models.BlogPost.objects.get_random_post(),'about_site':models.AboutSite.objects.get_site_about(),})
        except:context.update({'about_site':'',})
        return context



@api_view(['POST'])
def increment_BlogLikes(request,pk=None):
    post =models.BlogPost.objects.get(id=pk)
    postlikes,created = models.BlogLikes.objects.get_or_create(blogpost=post)
    print(created)

    DATA= request.data
    print(DATA)
    def save_likes_or_dislikes(data,likemodel):
        if data['like'] == True:
            print("likes",likemodel.likes)
            likemodel.likes +=1

        if data['dislike'] == True:
            likemodel.dislikes +=1
        likemodel.save()

    if created:
        "this works if the instance is just created"
        save_likes_or_dislikes(DATA,postlikes)         
    else:
        "this runs we want to update the insance"
        save_likes_or_dislikes(DATA,postlikes) 

        


    return Response(data={"likes":postlikes.likes,"dislikes":postlikes.dislikes},status=status.HTTP_200_OK)