from django.urls import path
from django.contrib import admin
import usermgmt
from usermgmt import views

admin.autodiscover()
urlpatterns = [
    # Examples:
    # url(r'^$', 'task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    path(r'admin/', admin.site.urls),
    path(r'', views.home, name='home'),
    path(r'index', views.index, name='home'),
    path(r'home', views.index, name='home'),
    path(r'addsuccess', views.addsuccess, name='addsuccess'),
    path(r'usermod', views.usermod, name='usermod'),
    path(r'modifyuser', views.modifyuser, name='modifyuser'),
    path(r'userdel', views.userdel, name='userdel'),
    path(r'deleteduser', views.deleteduser, name='deleteduser'),
    path(r'usergrant', views.usergrant, name='usergrant'),
    path(r'grantusersucc', views.grantusersucc, name='grantusersucc'),
    path(r'register', views.register, name='register'),
    path(r'login', views.user_login, name='login'),
    path(r'logout', views.user_logout, name='logout'),

]
