from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm,PwdResetForm,PwdResetConfirmForm, PwdChangeForm

app_name= 'accounts'


urlpatterns=[
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html",
                                                                   form_class=PwdChangeForm), name='pwdforgot'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html',authentication_form=UserLoginForm), name='login'),
     path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html",
                                                                 form_class=PwdResetForm), name='pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html', form_class=PwdResetConfirmForm), name="pwdresetconfirm"),  
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'), 
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),     
    path('profile/edit/', views.edit, name='edit'),                                                
    path('profile/', views.profile, name='profile'),
   
    path('profile/delete/', views.delete_user, name='deleteuser'),
    path('register/', views.accounts_register, name='register'),
    path('like/', views.like, name='like'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
     
     



]    






 






if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)