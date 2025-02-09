from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static





urlpatterns=[
     path('', views.home, name='index'),
     path('search/', views.post_search, name='post_search'),
     path('post/<int:post_id>/', views.post_single, name='post_single'),
     path('create/', views.create_post, name='create_post'),
     path('category/<str:category>/', views.CatListView.as_view(), name='category'),
     path('account/', include('django.contrib.auth.urls')),
     path('notifications/', views.notifications_view, name='notifications'),
     path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    
     
     



]    


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



 




