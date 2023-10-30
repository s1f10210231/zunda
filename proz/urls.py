from django.urls import path
from proz import views
from django.conf import settings
from django.conf.urls.static import static

app_name ='proz'

urlpatterns = [
    path('',views.index,name='index'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)