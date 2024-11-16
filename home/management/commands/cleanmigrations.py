from django.core.management.base import BaseCommand
import os
import shutil

# Update this list every time a new app is created
APPS = [
    "celery_background",
    "communication",
    "home",
    "k_api",
    "k_auth",
    "k_chome",
    "thing",
]
MIGRATION_DIR = "migrations"


class Command(BaseCommand):
    # Should only be used during development, DEBUG=True
    help = "Clean all migrations files in migration folder"

    def add_arguments(self, parser):
        parser.add_argument(
            "-a",
            "--apps",
            nargs="+",
            type=str,
            help="Specify app names (space-separated) to clean migrations for. Defaults to all in APPS list.",
        )

    def handle(self, *args, **options) -> str | None:
        apps_to_clean = options.get("apps", APPS)

        if not apps_to_clean:
            apps_to_clean = APPS

        self.stdout.write(
            self.style.WARNING(
                "**WARNING:** You are about to delete migration files. This is destructive and should only be used with caution.\n"
                "Continue? (y/N): "
            ),
            ending="",
        )

        confirmation = input().lower()
        if confirmation not in ("y", "yes"):
            self.stdout.write(self.style.SUCCESS("Cleaning cancelled."))
            return

        self.stdout.write(self.style.SUCCESS("Deleting migration files..."))
        for app in apps_to_clean:
            migration_path = os.path.join(app, MIGRATION_DIR)
            # do not delete the __init__.py file
            try:
                for file in os.listdir(migration_path):
                    if file != "__init__.py":
                        dir_content = os.path.join(migration_path, file)
                        if os.path.isfile(dir_content):
                            os.remove(dir_content)
                            self.stdout.write(
                                self.style.SUCCESS(f"Deleted '{file}' file")
                            )
                        elif os.path.isdir(dir_content):
                            shutil.rmtree(dir_content)
                            self.stdout.write(
                                self.style.SUCCESS(f"Deleted '{file}' directory")
                            )
            except FileNotFoundError:
                self.stdout.write(
                    self.style.ERROR(
                        f"Migration folder for '{app}' not found. Skipping..."
                    )
                )
