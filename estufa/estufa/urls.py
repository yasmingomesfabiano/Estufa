from django.contrib import admin
from django.urls import include, path
from estufa.views import LeituraViewSet, AlertaViewSet
from rest_framework import routers

router= routers.DefaultRouter()
router.register(r'leituras', LeituraViewSet, basename='leitura')
router.register(r'alerta', AlertaViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
