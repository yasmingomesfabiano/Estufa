from django.shortcuts import render

from rest_framework import viewsets #viewsets: classes que agrupam visualizações , como CROD em uma unica classe
from rest_framework.decorators import action #actions: ações personalizadas para criar rotas em viewsets
from rest_framework.response import Response #response: restorna respostas HTTP formatadas
from .models import Leitura, Alerta
from .serializers import LeituraSerializer, AlertaSerializer


class LeituraViewSet(viewsets.ModelViewSet):
    query= Leitura.objects.all() #pegue todos os objetos contidos em Leitura
    serializer_class= LeituraSerializer
    
    @action(detail=False, methods=['get'])
    def ultima(self, request):
        """rertona a ultima leitura"""
        leitura= Leitura.objects.first()
        
        if Leitura:
            serializer= self.get_serializer(leitura)
            return Response(serializer.data)
        return Response({'Erro': 'Nenhuma leitura encontrada'})

    @action(detail=False, methods=['get'])
    def ultimas_24(self, request):
        """retorna leituras das ultimas 24 horas"""
        from django.utils import timezone
        from datetime import timedelta
        
        agora= timezone.now() #verificando o horario atual com configuração correta do fuso horario
        
class AlertaViewSet(viewsets.ModelViewSet):
    queryset= Alerta.objects.all()
    serializer_class= AlertaSerializer
    
    @action(detail=False, methods=['get'])
    def nao_lido(self, request):
        '''retorna alerta não lidos'''    
        alertas= Alerta.objects.filter(lido=False)
        serializer= self.get_serializer(alertas, many="True") 
        return Response(serializer.data) 
    
    @action(detail=True, methods=['post'])
    def marcar_lido(self, request, pk=None):
        '''marcar alerta como lido'''
        alerta= self.get_object()
        alerta.lido= True
        alerta.save()
        serializer= self.get_serializer(alerta)
        return Response(serializer.data)
                  