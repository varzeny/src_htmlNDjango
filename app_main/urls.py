from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.showPage, name='show'),
    path('dbRead_forever',views.dbRead_forever,name="dbRead_forever"),
    path('dbRead/',views.dbRead,name='dbRead'),
    path('connect/',views.connect,name='connect'),
    path('moveUnit/',views.moveUnit,name='moveUnit'),
    path('sendMsg2Unit',views.sendMsg2Unit,name='sendMsg2Unit'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)