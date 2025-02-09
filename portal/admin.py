from django.contrib import admin
from .import models



@admin.register(models.Post)
class Authoradmin(admin.ModelAdmin):
    list_display=('user','title')
    


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('post','user','publish')
    search_fields=('user','content')


admin.site.register(models.Category)

admin.site.register(models.Notification)


# Register your models here.
