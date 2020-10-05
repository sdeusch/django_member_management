from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.details, name='detail'),
    path('delete/<int:id>/', views.details_delete, name='detail_delete'),
    path('', views.Members, name='home-page' ),
    path('members/', views.memberList.as_view()),
    path('upload/', views.upload_list, name='upload-list'),
    path('uploads/upload',views.upload_csv, name='upload-csv')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
