from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages.views import flatpage
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from foodgram import views

handler404 = views.error404
handler500 = views.error500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('django.contrib.flatpages.urls')),
    path('author/', flatpage, {'url': '/author/'}, name='about_author'),
    path('tech/', flatpage, {'url': '/tech/'}, name='about_tech'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += staticfiles_urlpatterns()
