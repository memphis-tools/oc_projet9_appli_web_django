from django.core.management.base import BaseCommand
from colorama import Fore, Style
import subprocess
import os
import re


PROJECT_DIR = "."
DATABASE_NAME = "db.sqlite3"
DATABASE_PATH = f"{PROJECT_DIR}/{DATABASE_NAME}"
APPS = ['authentication', 'litreview']


class Command(BaseCommand):
    help = "Script dédié à initialiser une base de données en environnement de développement."

    def handle(self, *args, **kwargs):
        """
        What it does: remove the database and any migrations to permmit a fresh start app usage.
        """
        print(f"{Fore.YELLOW}[REMOVING DATABASE]{Style.RESET_ALL}")
        if os.path.isfile(f"{DATABASE_PATH}"):
            subprocess.run(["rm", DATABASE_PATH])
            print(f"{Fore.GREEN}[DATABASE REMOVED]{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[NO DATABASE FOUND]{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[REMOVING IMAGES]{Style.RESET_ALL}")
        pattern = re.compile(r'.*([jpg|png])$')
        for file in os.listdir(f"{PROJECT_DIR}/media/"):
            if re.match(pattern, file):
                os.remove(f"{PROJECT_DIR}/media/{file}")
        print(f"{Fore.GREEN}[IMAGES REMOVED]{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[REMOVING MIGRATIONS]{Style.RESET_ALL}")
        pattern = re.compile(r'([0]{3}).*py$')
        subprocess.run(["rm", "-rf", f"{PROJECT_DIR}/oc_projet10_rest_framework/__pycache__"])
        for app in APPS:
            subprocess.run(["rm", "-rf", f"{PROJECT_DIR}/{app}/__pycache__"])
            subprocess.run(["rm", "-rf", f"{PROJECT_DIR}/{app}/migrations/__pycache__"])
            for file in os.listdir(f"{app}/migrations/"):
                if re.match(pattern, file):
                    os.remove(f"{PROJECT_DIR}/{app}/migrations/{file}")
        print(f"{Fore.GREEN}[MIGRATIONS REMOVED]{Style.RESET_ALL}")
