# Prometheus

En este repositorio encontrará dos carpetas:
- prometheus_server --> con la configuración del servidor de prometheus
- prometheus_exporter --> el servicio que utilizaremos para monitorear nuestro sistema/device y que extrae información del sistema y la publica por HTTP (por defecto puerto 9098)

### Lanazar docker con ambos sistemas
Para lenvatar ambos sistemas y poder ver los mensajes de log en la consola ejecutar:
```sh
$ docker-compose up
```
Para lenvatar ambos sistemas y que no le quede tomada la consola ejecutar:
```sh
$ docker-compose start
```
Para detener los procesos ejecutar:
```sh
$ docker-compose down
$ docker-compose stop
```

### Visualizar prometheus server dashboard
Ingresar a la siguiente URL (modifique la IP según el caso):
```
http://127.0.0.1:9090/
```

### Telemetria por HTTP del prometheus exporter
Ingresar a la siguiente URL (modifique la IP según el caso):
Debe refrescar la página para que se actualice el contenido (que por defecto cambia cada 2segundos)
```
http://127.0.0.1:9098/
```

### Telemetria por MQTT
Este programa además viene configurado para conectarse a un broker mqtt local ("localhost", 1883) y enviar datos por el tópico:
```
metrics
```
Para visualizar las metricas en la consola ejecute:
```sh
$ mosquitto_sub -h localhost -t metrics
```
Deberá ver que la telemetria de monitoreo tiene un formato JSON como el siguiente:
```
{"cpu": 5.9, "ram": 40.0, "disk": 76.4, "temp": 50.0, "uptime": 265}
```

### Telemetría
- cpu: porcentaje (%) de cpu en uso del sistema
- ram: porcentaje (%) de RAM en uso del sistema
- disk: porcentaje (%) del disco en uso del sistema
- temp: temperatura en grados del sistema
- uptime: tiempo en segundos que lleva activo el sistema de monitoreo