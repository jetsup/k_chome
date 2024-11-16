from serial.tools import list_ports

device_list = list_ports.comports()
for device in device_list:
    if device.vid != None or device.pid != None:
        port = device.device
        vid = "{:04X}".format(device.vid)
        pid = "{:04X}".format(device.pid)
        print(f"Port\t: {port}\nVID\t: {vid}\nPID\t: {pid}")
