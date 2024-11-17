from k_chome.periodic_tasks import CELERY_BEAT_SCHEDULE

# using rabbitmq as the broker
broker_url = "amqp://guest:guest@localhost:5672//"

# We can either set Redis, RabbitMQ, Postgresql, MySQL, MongoDB
# or other databases as the result backend.
# using django-db as the result backend

# result_backend = "mongodb://localhost:27017/django-revision-celery-log"
result_backend = "django-db"

# User pickle for complex data structures while passing arguments to tasks
# json, yaml, msgpack are other options.
task_serializer = "pickle"

timezone = "Africa/Nairobi"

# celery caches the results of tasks, so that if the same task is called again
# it can return the cached result instead of re-executing the task.
# By Default celery uses the Django cache backend
# using database redis 2 as the cache backend

cache_backend = "redis://localhost:6379/2"

# Either define imports here or set autodiscover_tasks either one is enough
imports = ("celery_background.tasks",)

# celery will stop accepting pickled content so need to allow pickle for deserialization
accept_content = ["json", "pickle"]
