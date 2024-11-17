from __future__ import absolute_import, unicode_literals
from celery import shared_task
from serial.tools import list_ports


@shared_task(name="listen_usb_serial_ports")
def listen_usb_serial_ports(current_serial_ports: dict = {}):
    new_serial_ports = {}  # Dictionary to store newly discovered ports

    # filter for those with VID and PID
    device_list = [
        port for port in list_ports.comports() if port.vid != None or port.pid != None
    ]

    for device in device_list:
        key = (
            f"{device.vid:04X},{device.pid:04X}"  # Format key with zero-padded VID/PID
        )
        if key not in current_serial_ports:
            new_serial_ports[key] = device.device

    updated_ports = {**current_serial_ports, **new_serial_ports}

    return updated_ports
