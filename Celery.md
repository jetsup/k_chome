# Celery Commands

To run celery in background, use the following command:

```bash
celery multi start w1 -A k_chome -l INFO --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log
```

To stop celery, use the following command:

```bash
celery multi stop w1 -A k_chome -l INFO
```

To restart celery, use the following command:

```bash
celery multi restart w1 -A k_chome -l INFO --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log
```
