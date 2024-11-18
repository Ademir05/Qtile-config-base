import psutil

def getCpuTemp():
    dic = psutil.sensors_temperatures()
    return dic['k10temp']


if __name__ == '__main__':
    print(getCpuTemp())