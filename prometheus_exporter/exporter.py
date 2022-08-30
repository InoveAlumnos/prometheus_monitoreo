import psutil
from prometheus_client.core import GaugeMetricFamily
import time

  
class Exporter():
    def __init__(self):
        self.cpu_usage = 0
        self.ram_usage = 0
        self.disk_usage = 0
        self.temp = 0
        self.uptime_seconds = 0

        self.start_time = time.time()

    def metrics(self):
        return {
                "cpu": self.cpu_usage,
                "ram": self.ram_usage,
                "disk": self.disk_usage,
                "temp": self.temp,
                "uptime": self.uptime_seconds,
                }

    def update(self):
        # uso total de la CPU (todos los cores)
        try:
            self.cpu_usage = psutil.cpu_percent()
        except:
            self.cpu_usage = 0
       
        # uso de RAM
        try:
            psutil.virtual_memory()
            dict(psutil.virtual_memory()._asdict())
            self.ram_usage = psutil.virtual_memory().percent
        except:
            self.ram_usage = 0

        # uso del disco
        try:
            partitions = psutil.disk_partitions()
            for p in partitions:
                if p.mountpoint == "/":  # disco principal
                    self.disk_usage = psutil.disk_usage(p.mountpoint)._asdict()["percent"]
                    break
                if p.mountpoint == "/etc/hosts": # en docker "/" figura como "/etc/hosts"
                    self.disk_usage = psutil.disk_usage(p.mountpoint)._asdict()["percent"]
                    break
        except:
            self.disk_usage = 0
        
        # temperatura del core
        try:
            temperatures = psutil.sensors_temperatures(fahrenheit=False)
            max_core_temp = 0
            cores = temperatures["coretemp"]
            for core in cores:
                if max_core_temp < core.current:
                    max_core_temp = core.current

            self.temp = max_core_temp
        except:
            self.temp = 0

        # tiempo ejecutandose el exporter
        self.uptime_seconds = int(time.time() - self.start_time)

    # Funciones creadas para prometheus
    def __cpu(self):
        cpu_gauge = GaugeMetricFamily('cpu', 'cpu usage')
        cpu_gauge.add_metric([], value=self.cpu_usage)        
        return cpu_gauge

    def __ram(self):
        ram_gauge = GaugeMetricFamily('ram', 'ram usage')
        ram_gauge.add_metric([], value=self.ram_usage)
        return ram_gauge

    def __disk(self):
        disk_gauge = GaugeMetricFamily('disk', 'disk usage')
        disk_gauge.add_metric([], value=self.disk_usage)
        return disk_gauge

    def __temperature(self):
        temp_gauge = GaugeMetricFamily('temperature', 'temperature ºc')
        temp_gauge.add_metric([], value=self.temp)
        return temp_gauge

    def __uptime(self):
        uptime_gauge = GaugeMetricFamily('uptime', 'machine uptime')
        uptime_gauge.add_metric([], value=str(self.uptime_seconds))
        return uptime_gauge

    def collect(self):
        yield self.__cpu()
        yield self.__ram()
        yield self.__disk()
        yield self.__temperature()
        yield self.__uptime()

    
if __name__ == "__main__":
    data_colector = Exporter()
    data_colector.update()