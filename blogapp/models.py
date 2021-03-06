from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin,BaseUserManager)
import random
import datetime

from django.db.models.expressions import F




class myUserManager(BaseUserManager):
    
    def create_user(self,email,password=None):
        "this helps create our custom myUser instance"

        if password is None:
            raise ValidationError("You Need a Password To create an Account ")
        "all we need to fill is the email for now"
        user = self.model(email = email)
        "then we set the password set_password() helps to hash our password"
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        "this method helps create a superuser easily"
        superuser = self.create_user(email,password)
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save(using=self._db)

        return superuser


class myUser(PermissionsMixin,AbstractBaseUser):
    email= models.EmailField(unique=True)
    first_name= models.CharField(max_length=100)
    surname_name= models.CharField(max_length=100)
    is_active  = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(upload_to='userimage/%m/%d/',null=True)
    about_writer = models.TextField(default="")

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = []
    "this  represent the manager of the user"
    objects = myUserManager()

    def __str__(self):
        return f'{self.surname_name} {self.first_name}'



"# a BlogPost Must Have"
"""
blogpost Title
as many paragraph it wants -- (many paragraph to one post)
one picture
isPopular
(many comment to one post)
foren kye of tag
"""
class BlogPostManager(models.Manager):
    "this is what manages our Blog Post"
    def get_random_post(self):
        "this returns a random post every time it called"
        queryset = super().get_queryset()
        number_of_post = queryset.count()
        "this code get random post using the choices method"
        if number_of_post == 0:
            return ''
        else:
            # print(queryset.first().id,number_of_post)
            return random.choices([post for post in queryset.all()])[0]
            # return queryset.get(id=random.randint(queryset.first().id,number_of_post))
    def get_all_trending(self,num=None):
        "this function gets all the posts that are marked as 'is_trending=True' "
        if num is None:
            return super().get_queryset().filter(is_trending=True)
        return super().get_queryset().all().filter(is_trending=True)[0:num]
    
    def get_range_of_post(self,num):
        "this method get the amount of post specified"
        return super().get_queryset().all().order_by('-id')[0:num]

    def is_there_post(self):
        return super().get_queryset().count() != 0
    def get_posts_in_desc_order(self):
        return super().get_queryset().all().order_by('-id')
    
class Categories(models.Model):

    class NameChoices(models.TextChoices):
        Lifestyle ='Lifestyle'
        Inspiration = 'Inspiration'
        Fashion = 'Fashion'
        Politic = 'Politic'
        Trending = 'Trending'
        Culture = 'Culture'
    names = models.CharField(max_length=50,choices=NameChoices.choices)
    slug = models.SlugField(default="")
    
    def __str__(self):
        return self.slug


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    main_image= models.ImageField(upload_to='blogpost/main_image/%m/%d/')
    author = models.ForeignKey(myUser,on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories,on_delete=models.CASCADE,blank=True,default='')
    is_trending = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def get_paragraph_intro(self):
        'this method get the post intro and extract 100 charachters'
        #input_text is where the text lives check BlogParagraph for more details
        try:
            return f'{self.blogparagraph_set.all()[0].input_text[0:100]}.....'
        except:
            return ''


    "Custom manager"
    objects = BlogPostManager()
    def __str__(self) -> str:
        return f'{self.title} By {self.author}'


class Comment(models.Model):
    name = models.CharField(max_length=200)
    comment_text = models.TextField()
    post = models.ForeignKey(BlogPost,on_delete=models.CASCADE,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'Comment By {self.name}'

class BlogParagraph(models.Model):
    "one BlogPost has many BlogParagraph"
    blogpost = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
    input_text = models.TextField()
    image = models.ImageField(upload_to='blogParagraphImage/%m/%d/',blank=True)

class BlogLikes(models.Model):
    likes = models.IntegerField(blank=True,default=0)
    dislikes = models.IntegerField(blank=True,default=0)
    blogpost = models.ForeignKey(BlogPost,on_delete=models.CASCADE)

    def __str__(self):
        return f'Likes: {self.likes} || Dislikes: {self.dislikes}'

class AboutSite_Manager(models.Manager):

    def get_site_about(self):
        return super().get_queryset().all()[0]

class AboutSite(models.Model):
    body= models.TextField()
    
    objects = AboutSite_Manager()

    def __str__(self):
        return f'{self.id}) { self.body[0:10]}..'

class SavedNewsletterEmails(models.Model):
    email = models.EmailField()

    def __str__(self):
        return f'{self.email}'


class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f'{self.name} Ask About {self.subject}'