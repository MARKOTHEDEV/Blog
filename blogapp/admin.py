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
        ('Personal info', {'fields': ('image','first_name','surname_name','last_login')}),
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

class  Blog_Imagesinline(admin.TabularInline):
    model= models.BlogImages
    extra=1
    max_num =2


class BlogpostAdmin(admin.ModelAdmin):
    fieldsets=[(None,{'fields':['is_popular','is_trending','title','main_image','author','categories']})]
    inlines=[BlogPost_Paragraphinline,Blog_Imagesinline]



admin.site.register(models.myUser,UserAdmin)
admin.site.register(models.BlogPost,BlogpostAdmin)
admin.site.register(models.Categories)
