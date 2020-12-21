from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("job/", views.job, name="job"),
    path("detail/<int:job_id>", views.detail, name="detail"),
    path("next/<int:job_id>", views.next, name="next"),
    path("before/<int:job_id>", views.before, name="before"),
    path("write/", views.write, name="write"),
    path("rewrite/<int:job_id>", views.rewrite, name="rewrite"),
    path("remove/<int:job_id>", views.remove, name="remove"),
    path('search', views.search, name='search'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)