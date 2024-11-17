from celery.schedules import timedelta
from celery_background.tasks import listen_usb_serial_ports
from django.conf import settings

boards_database = {}
boards_database = listen_usb_serial_ports(boards_database)

CELERY_BEAT_SCHEDULE = {
    'add': {
        'task': 'listen_usb_serial_ports',
        'schedule': timedelta(seconds=1),
        # 'args': (boards_database,),
        'args': (boards_database,),
        # store returned value in the global variable
    }
}
