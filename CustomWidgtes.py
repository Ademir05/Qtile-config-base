import psutil

from libqtile.widget import base
from libqtile import widget
import Colors

class CpuTemp(base.ThreadPoolText):
    defaults = [
        ("update_interval", 5, "Intervalo de actualización en segundos"),
        ("font", "sans", "Fuente del texto"),
        ("fontsize", 12, "Tamaño de la fuente"),
        ("foreground", "ffffff", "Color del texto"),
        ("background", "000000", "Color de fondo"),
    ]

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, text="Cargando...", **config)
        self.add_defaults(CpuTemp.defaults)

    def getCpuTemp(self):
        dic = psutil.sensors_temperatures()
        if 'k10temp' in dic:
            core = dic['k10temp']
            return core[0].current
        elif 'coretemp' in dic:
            core = dic['coretemp']
            return core[0].current
        else:
            return "No sensor"

    def poll(self):
        try:
            temp = float(self.getCpuTemp())
            return f"CPU Temp: {temp:.2f}°C" if isinstance(temp, (int, float)) else str(temp)
        except Exception as e:
            return f"Error: {str(e)}"


class BateryIfExist(base.ThreadPoolText):
    defaults = [
        ("update_interval", 5, "Intervalo de actualización en segundos"),
        ("font", "sans", "Fuente del texto"),
        ("fontsize", 12, "Tamaño de la fuente"),
        ("foreground", "ffffff", "Color del texto"),
        ("background", "000000", "Color de fondo"),
    ]
    def tiene_bateria(self):
        battery = psutil.sensors_battery()
        return battery is not None

    def poll(self):
        if self.tiene_bateria():
            return [
                widget.BatteryIcon(
                    background=self.defaults['background'],
                    scale=1.2,
                ),
                widget.Battery(
                    background=self.defaults['background'],
                    foreground=self.defaults['foreground'],
                    format='{percent:2.0%}',
                    update_interval=1,
                ),
            ]
        return []