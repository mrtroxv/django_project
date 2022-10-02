from django.urls import path
from . import views

urlpatterns = [
    path('', views.SongRoute.as_view(), name="without_args"),
    path("file", views.FileInsert.as_view(), name='file'),
    path('<int:id>', views.SongArgumentRoute.as_view(), name="print"),
    path('selct_by_filter', views.SelectByFilter.as_view(), name='filter')
]
