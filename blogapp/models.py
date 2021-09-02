from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin,BaseUserManager)





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


    USERNAME_FIELD='email'
    REQUIRED_FIELDS = []
    "this  represent the manager of the user"
    objects = myUserManager()

    def __str__(self):
        return self.email



"# a BlogPost Must Have"
"""
blogpost Title
as many paragraph it wants -- (many paragraph to one post)
one picture
isPopular
(many comment to one post)
foren kye of tag
"""
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    main_image= models.ImageField(upload_to='blogpost/main_image/%m/%d/')
    author = models.ForeignKey(myUser,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.title} By {self.author}'


class BlogParagraph(models.Model):
    "one BlogPost has many BlogParagraph"
    blogpost = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
    input_text = models.TextField()

class BlogImages(models.Model):
    blogpost = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
    secondary_image= models.ImageField(upload_to='blogpost/secondary_image/%m/%d/')


# class Comment

"""
class Tag
"""