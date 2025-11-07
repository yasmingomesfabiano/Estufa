from django.contrib import admin
from django.urls import path
from estufa.views import LeituraViewSet, AlertaViewSet
from rest_framework import routers

router= routers.DefaultRouter()
router.register(r'leituras', LeituraViewSet) #r:rotas
router.regiter(r'alerta', AlertaViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
]