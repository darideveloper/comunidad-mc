from django.contrib import admin
from django.urls import include, path

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('', include('app.urls')),
    path('botviews/', include('botviews.urls')),
    path('botcheers/', include('botcheers.urls')),
    path('admin/', admin.site.urls),
]

handler404 = 'app.views.error404'