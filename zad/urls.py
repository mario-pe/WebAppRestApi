from django.conf.urls import url,include
from django.contrib.auth.decorators import login_required

from . import views, api_views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from django.conf.urls import include

router = routers.DefaultRouter()


app_name = 'zad'

urlpatterns = [
    # index /zad
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'zad/logged_out.html'}, name='logout'),
    url(r'^logout-then-login/$', auth_views.logout_then_login, name='logout_then_login'),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', views.signup, name='signup'),

    url(r'^add_file/$', login_required(views.AddFile.as_view()), name='add_file'),
    url(r'^action_file/(?P<id>\d+)/$', login_required(views.ActionFile.as_view()), name='action_file'),
    url(r'^add_url/$', login_required(views.AddUrl.as_view()), name='add_url'),
    url(r'^action_url/(?P<id>\d+)/$', login_required(views.ActionUrl.as_view()), name='action_url'),
    url(r'^details_url/(?P<id>\d+)/$', login_required(views.ActionUrl.as_view()), name='customer_url_details'),
    url(r'^details_file/(?P<id>\d+)/$', login_required(views.ActionFile.as_view()), name='customer_file_details'),
    url(r'^upload_info/(?P<id>\d+)/$', views.upload_info, name='upload_info'),
    url(r'^upload_info_file/(?P<id>\d+)/$', views.upload_info_file, name='upload_info_file'),

    url(r'^urls/$', api_views.Url.as_view()),
    url(r'^files/$', api_views.File.as_view()),
    url(r'^get_file/$', api_views.GetFile.as_view()),
    url(r'^get_url/$', api_views.GetUrl.as_view()),
    url(r'^archive/(?P<date_from>.+)/(?P<date_to>.+)/$', api_views.ActivityArchiveApi.as_view()),

    url(r'^api-auth/', include('rest_framework.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

