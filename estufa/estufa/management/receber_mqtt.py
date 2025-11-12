import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from django.conf import settings
from estufa.models import Leitura, Alerta 

class Command(BaseCommand):
    help= 'Recebe dados MQTT e salva no banco de dados'
    
    def __init__(self):
        super().__init__()
        self.temperatura_atual= None #None: ausência de valor
        self.umidade.atual= None
        self.Client= mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect= self.on_connect
        self.client.on_message= self.on_massage
        
    def on_connect(self, client, userdara, flags, rc):
        if rc == 0: #return code(retorno do código)
            self.stdout.write(self.style.SUCESS('Connectado ao MQTT'))
            #stdout.write: PRINT SEM A QUEBRA DE LINHA
            
            client.subcribe("estufa/temperatura")
            client.subcribe("estufa/umidade")
            
        else:
            self.stdout.write(self.style.ERROR(f'Erro:{rc}'))
            
            
    def on_message(self, client, userdata, msg):
        try:
            valor= float(msg.playload.decode())
            if msg.topic == "estufa/temperatura":
                self.temperatura_atual= valor
                self.stdout.write(f"Temperatura: {valor}ºC")
                
            elif msg.topic == "estufa/umidade":
                self.temperatura_atual= valor
                self.stdout.write(f"Umidade: {valor}%")
                
            #se tivermos os dois valor tanto de umidade, tanto de temperatura, salvamos no banco de dados
            if self.temperatura_atual is not None and self.umidade_atual is not None:
                self.salvar_leitura()
                self.verificar_alertas()
                self.temperatura_atual= None
                self.umidade_atual= None
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro:{str(e)}"))
        
        
    def salvar_leitura(self):
        '''salvar leitura no banco de dados''' 
        leitra= Leitura.objects.create(
            temperatura= self.temperatura_atual,
            umidade= self.umidade_atual
        )  
        self.stdout.write(self.style.SUCESS(f"Leitura salva: {Leitura}"))         
                
    def verificar_alerta(self):
        '''verificar se há valores criticos e criar alertass'''
        if self.temperatura_atual > settings.TEMP_MAX: #coportamento da aplicação
            self.criar_alerta(
                "TEMP_ALTA",
                f"Temperatura{self.temperatura_atual}ºC acima do limite {settings.TEMP_MAXº}C"
            )
            
        elif self.temperatura_atual < settings.TEMP_MIN: #coportamento da aplicação
            self.criar_alerta(
                "TEMP_BAIXA",
                f"Temperatura{self.temperatura_atual}ºC abaixo do limite {settings.TEMP_MIN}Cº"
            )
            
        ''' try:
                self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
                self.client.loop_forever()
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING("\n \n Receptor parado"))'''
        
        if self.umidade_atual < settings.UMIDADE_MIN:
            self.criar.alerta(
                '''UMIDADE_BAIXA'''
                f"Umidade {self.umidade_atual}% abaixo do limite {settings.UMIDADE_MIN}%"
            )
        elif self.umidade_atual > settings.UMIDADE_MIN:
             self.criar.alerta(
                '''UMIDADE_ALTA'''
                f"Umidade {self.umidade_atual}% abaixo do limite {settings.UMIDADE_MAX}%"
            )
    def criar_alerta(self, tipo, mensagem):
        alerta= Alerta.objects.create(tipo=tipo, mensagem=mensagem)
        self.stdout.write(self.style.WARNING(f"Alerta: {alerta}"))
     
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Receptor MQTT Iniciado \n"))
        try:
            self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
            self.client.loop_forever()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\n\n Receptor Parado"))
            self.client.disconnect()  
            
         
        
