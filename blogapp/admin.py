from django.contrib import admin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from . import models


class UserAdmin(BaseUserAdmin):
    ordering = ('id',)
    list_display = ('id','email','first_name')
    list_display_links = ('first_name','email')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('image','first_name','surname_name','last_login','about_writer')}),
        ('Permissions', {'fields': ('is_staff','is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'password1', 'password2'),
        }),
    )




class  BlogPost_Paragraphinline(admin.TabularInline):
    model= models.BlogParagraph
    extra=1
    # fieldsets

# class  Blog_Imagesinline(admin.TabularInline):
#     model= models.BlogImages
#     extra=1
#     max_num =2


class BlogpostAdmin(admin.ModelAdmin):
    fieldsets=[(None,{'fields':['is_popular','is_trending','title','main_image','author','categories']})]
    inlines=[BlogPost_Paragraphinline]



admin.site.register(models.myUser,UserAdmin)
admin.site.register(models.BlogPost,BlogpostAdmin)
admin.site.register(models.Categories)
admin.site.register(models.AboutSite)
admin.site.register(models.SavedNewsletterEmails)
admin.site.register(models.ContactUs)
# admin.site.register(models.Comment)



"the settings below has to do with the Admin Designs"
admin.site.site_header= "MyBlog Admin"
admin.site.site_title = "myBlog Portal"
admin.site.index_title  = "Welcome to  myBlog Portal"
