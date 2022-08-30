import sys
import time
import json

import paho.mqtt.client as paho
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
#import schedule

from exporter import Exporter

def main(port=9098, update_period=2):

    start_http_server(port)
    data_collector = Exporter()
    try:
        REGISTRY.register(data_collector)
        print("Prometheus exporter started")

        try:
            client = paho.Client("prometheus_exporter")
            client.connect("localhost", 1883)
            client.loop_start()
            print("MQTT client conectado")
        except:
            print("Error: falló conexión al MQTT broker")
            client = None

        while True:
            # Actualizar metrics
            data_collector.update()

            # Obtener metricas del sistema y enviar por mqtt
            if client is not None:
                metrics = data_collector.metrics()            
                client.publish("sensores/monitoreo", json.dumps(metrics))

            # Esperar al siguiente interavalo
            time.sleep(update_period)

    except KeyboardInterrupt:
        print("Finalizando el programa")
    except Exception as e:
        print("Error:", e)

    if client is not None:
        print("MQTT client desconectado")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()