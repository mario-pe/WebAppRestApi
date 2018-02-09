from django.conf.urls import url,include
from . import views, api_views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from django.conf.urls import include

router = routers.DefaultRouter()
# router.register(r'/api', api_views.Url.as_view())


app_name = 'zad'

urlpatterns = [
    # index /zad
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'zad/logged_out.html'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', views.signup, name='signup'),

    url(r'^add_file/$', views.AddFile.as_view(), name='add_file'),
    url(r'^action_file/(?P<id>\d+)/$', views.ActionFile.as_view(), name='action_file'),
    url(r'^add_url/$', views.AddUrl.as_view(), name='add_url'),
    url(r'^action_url/(?P<id>\d+)/$', views.ActionUrl.as_view(), name='action_url'),

    url(r'^details_url/(?P<id>\d+)/$', views.ActionUrl.as_view(), name='customer_url_details'),
    url(r'^details_file/(?P<id>\d+)/$', views.ActionFile.as_view(), name='customer_file_details'),


    url(r'^upload_info/(?P<id>d+)/$', views.upload_info, name='upload_info'),                    #poprawic i zrobic poludzku
    url(r'^upload_info_file/(?P<id>\d+)/$', views.upload_info_file, name='upload_info_file'),

    url(r'^urls/$', api_views.Url.as_view()),
    url(r'^files/$', api_views.File.as_view()),
    url(r'^get_file`/$', api_views.GetFile.as_view()),
    url(r'^archive/(?P<date_from>.+)/(?P<date_to>.+)/$', api_views.ActivityArchiveApi.as_view()),
    #url(r'^urls/(?P<pk>[0-9]+)/(?P<password>.+)/$', api_views.get_url),
    # url(r'^urls/$', api_views.url_add),


    url(r'^api-auth/', include('rest_framework.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

