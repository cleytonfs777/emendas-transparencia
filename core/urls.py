from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from cadastrar.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('auth/', include('usuarios.urls')),
    path('disparo/', include('disparo.urls')),
    path('cadastrar/', include('cadastrar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
