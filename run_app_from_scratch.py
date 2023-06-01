import os
import re
import sys
from colorama import Fore, Back, Style


DJANGO_SUPERUSER_PASSWORD = "applepie94"
SUPERUSER_NAME = "admin"
SUPERUSER_EMAIL = "litreview_admin@localhost"
PROJECT_DIR = "."
APP_LIST = ["authentication", "litreview",]
DATABASE_PATH = f"{PROJECT_DIR}/db.sqlite3"
PATTERN = re.compile(r"^([\d]+)_([\w\d\.]+)")
MEDIA_PATH = f"{PROJECT_DIR}/media/"


def remove_app_migrations(app):
    for file in os.listdir(f"{PROJECT_DIR}/{app}/migrations/"):
        if(re.match(PATTERN,file)):
            file_path = f"{PROJECT_DIR}/{app}/migrations/{re.search(PATTERN,file).group()}"
            print(f"{Fore.GREEN}[REMOVING MIGRATION FILE]: {file_path}{Style.RESET_ALL}")
            os.remove(file_path)
            return True
    return False


def remove_app_database():
    if os.path.isfile(MEDIA_PATH):
        print(f"{Fore.GREEN}[REMOVING DATABASE]: {DATABASE_PATH}{Style.RESET_ALL}")
        os.remove(DATABASE_PATH)
        return True
    return False


def remove_app_media():
    if os.path.isfile(DATABASE_PATH):
        print(f"{Fore.GREEN}[REMOVING DATABASE]: {DATABASE_PATH}{Style.RESET_ALL}")
        os.remove(DATABASE_PATH)
        return True
    return False


def initialise_project():
    os.system('python manage.py makemigrations')
    print(f"{Fore.GREEN}[RENEWING migrations] done{Style.RESET_ALL}")
    os.system('python manage.py migrate')
    print(f"{Fore.GREEN}[RENEWING DATABASE] migrate done{Style.RESET_ALL}")
    os.environ["DJANGO_SUPERUSER_PASSWORD"] = DJANGO_SUPERUSER_PASSWORD
    os.system(f"python ./manage.py createsuperuser --username {SUPERUSER_NAME} --email {SUPERUSER_EMAIL} --no-input")
    print(f"{Fore.GREEN}[RENEWING SUPERUSER] done{Style.RESET_ALL}")


if __name__ == "__main__":
    print(f"{Back.YELLOW}{sys.argv[0]}{Style.RESET_ALL}")
    for app in APP_LIST:
        remove_app_migrations(app)
    remove_app_database()
    initialise_project()
