from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from colorama import Fore, Style
import subprocess
import os
import re
from datetime import datetime
from PIL import Image

from authentication.models import UserFollows
from litreview.models import Ticket, Review

SUPERUSER_NAME = "admin"
SUPERUSER_PASSWORD = "applepie94"
SUPERUSER_EMAIL = "admin@bluelake.fr"
PROJECT_DIR = "."
DATABASE_NAME = "db.sqlite3"
DATABASE_PATH = f"{PROJECT_DIR}/{DATABASE_NAME}"
APPS = ['authentication', 'litreview']


class Command(BaseCommand):
    help = "Script dédié à initialiser une base de données en environnement de développement."

    def handle(self, *args, **kwargs):
        """
        What it does:
        - remove the database
        - remove any images in media/ folder
        - remove any __pycache__ files in apps folder
        - remove any migrations files in apps folder
        - re-initialise app by making migrations and applying migrate
        - create 1 superadmin account with id=1
        - create 3 dummy users
        - create dummy subscriptions:
            user id=2 follows only user id=3.
            user id=3 and id=4 follow everybody
        - create 1 ticket for user id=2 and 2 tickets for other users
        - create 1 'ticket+review' for user id=2
        - create 1 'review' from user id=3, for user id=2 and his ticket id=1
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

        print(f"{Fore.YELLOW}[PERFORMING MIGRATIONS]{Style.RESET_ALL}")
        subprocess.run(["python", "manage.py", "makemigrations"])
        print(f"{Fore.GREEN}[MIGRATIONS PERFORMED]{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[APPLYING MIGRATIONS TO DATABASE FOR APP: authentication]{Style.RESET_ALL}")
        subprocess.run(["python", "manage.py", "migrate", "authentication"])
        print(f"{Fore.GREEN}[MIGRATIONS APPLIED TO DATABASE]{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[APPLYING MIGRATIONS TO DATABASE FOR APP: softdesk]{Style.RESET_ALL}")
        subprocess.run(["python", "manage.py", "migrate", "litreview"])
        print(f"{Fore.GREEN}[MIGRATIONS APPLIED TO DATABASE]{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[APPLYING MIGRATIONS TO DATABASE FOR GENERAL PURPOSE]{Style.RESET_ALL}")
        subprocess.run(["python", "manage.py", "migrate"])
        print(f"{Fore.GREEN}[MIGRATIONS APPLIED TO DATABASE]{Style.RESET_ALL}")

        User = get_user_model()
        users_list = [
            {
                "username": "donald",
                "first_name": "donald",
                "last_name": "duck",
                "email": "donald.duck@bluelake.fr"
            },
            {
                "username": "daisy",
                "first_name": "daisy",
                "last_name": "duck",
                "email": "daisy.duck@bluelake.fr"
            },
            {
                "username": "loulou",
                "first_name": "loulou",
                "last_name": "duck",
                "email": "loulou.duck@bluelake.fr"
            },
        ]
        print(f"{Fore.YELLOW}[DUMMY SUPERUSER CREATION]{Style.RESET_ALL}")
        # keep in mind that user 1 is the default admin
        User.objects.create_superuser(SUPERUSER_NAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD)
        print(f"{Fore.GREEN}[DUMMY SUPERUSER CREATED]{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[DUMMY USERS CREATION]{Style.RESET_ALL}")
        for user in users_list:
            pre_user = User.objects.create_user(
                username=user["username"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                email=user["email"],
                password="applepie94"
            )
            pre_user.save()
            pre_user.followed_user = User.objects.get(username=user["username"].lower())
            pre_user.user_follow = UserFollows(user=pre_user.followed_user, followed_user=pre_user.followed_user)
            pre_user.save()
        print(f"{Fore.GREEN}[DUMMY USERS CREATED]{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[DUMMY SUBSCRIPTIONS CREATION]{Style.RESET_ALL}")
        user = User.objects.get(id=2)
        followed_user = User.objects.get(id=3)
        user_follow = UserFollows(user=user, followed_user=followed_user)
        user_follow.save()

        for followed_id in ["2", "4"]:
            user = User.objects.get(id=3)
            followed_user = User.objects.get(id=followed_id)
            user_follow = UserFollows(user=user, followed_user=followed_user)
            user_follow.save()

        for followed_id in ["2", "3"]:
            user = User.objects.get(id=4)
            followed_user = User.objects.get(id=followed_id)
            user_follow = UserFollows(user=user, followed_user=followed_user)
            user_follow.save()
        print(f"{Fore.GREEN}[DUMMY SUBSCRIPTIONS CREATED]{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[DUMMY TICKETS CREATION]{Style.RESET_ALL}")
        # we create 2 ticket for user id=3 et id=4, mais 1 seul ticket pour user id=2
        # keep in mind that user 1 is the default admin
        user = User.objects.get(id=2)
        img = Image.open(r"./images_livres_echantillon/odyssee_des_fourmis.jpg")
        img.thumbnail(settings.IMAGE_PREFERED_SIZE)
        img = img.save(fp="./media/odyssee_des_fourmis.jpg")
        ticket = Ticket.objects.create(
            title="Vu Odyssée des fourmis, ça vaut le coup ?",
            description="""
                Pellentesque risus arcu, placerat vitae tempor nec, mattis sed massa.
                Fusce purus tellus.
                """,
            user=user,
            image="./odyssee_des_fourmis.jpg",
            has_been_reviewed=True
        )
        ticket.save()

        user = User.objects.get(id=3)
        img = Image.open(r"./images_livres_echantillon/grandes_dates_histoires_du_monde.jpg")
        img.thumbnail(settings.IMAGE_PREFERED_SIZE)
        img = img.save(fp="./media/grandes_dates_histoires_du_monde.jpg")
        ticket = Ticket.objects.create(
            title="Vu Grandes dates de l'histoire du monde, pas écrit trop petit ?",
            description="""
                Quisque malesuada dui nec eros dignissim condimentum.
                Curabitur facilisis vestibulum vehicula.
                Duis metus diam, dictum et egestas ut, sodales quis dolor.
                Nunc a justo at ante consequat efficitur. Vestibulum maximus urna a sapien viverra malesuada.
                """,
            user=user,
            image="./grandes_dates_histoires_du_monde.jpg",
            has_been_reviewed=True
        )
        ticket.save()

        img = Image.open(r"./images_livres_echantillon/art_de_moucher_les_facheux.jpg")
        img.thumbnail(settings.IMAGE_PREFERED_SIZE)
        img = img.save(fp="./media/art_de_moucher_les_facheux.jpg")
        ticket = Ticket.objects.create(
            title="Vu Art de moucher les facheux, Rigolo ?",
            description="""
                Praesent sagittis tellus eleifend mi accumsan ultrices.
                Etiam id dolor sed lacus bibendum euismod ut ut ligula.
                In iaculis venenatis sollicitudin. Morbi rhoncus ex magna.
                """,
            user=user,
            image="./art_de_moucher_les_facheux.jpg",
            has_been_reviewed=True
        )
        ticket.save()

        user = User.objects.get(id=4)
        img = Image.open(r"./images_livres_echantillon/geostrategix.jpg")
        img.thumbnail(settings.IMAGE_PREFERED_SIZE)
        img = img.save(fp="./media/geostrategix.jpg")
        ticket = Ticket.objects.create(
            title="Vu Geostrategix, Intéressant et accessible ?",
            description="""
                Integer scelerisque eros mi, ut euismod justo hendrerit quis. Quisque quis massa ex.
                In a orci nec orci varius ornare nec non tortor.
                Donec nec imperdiet tortor. Duis nulla enim, mollis eget vehicula sed, aliquam.
                """,
            user=user,
            image="./geostrategix.jpg",
            has_been_reviewed=True
        )
        ticket.save()

        user = User.objects.get(id=4)
        img = Image.open(r"./images_livres_echantillon/art_de_la_guerre.jpg")
        img.thumbnail(settings.IMAGE_PREFERED_SIZE)
        img = img.save(fp="./media/art_de_la_guerre.jpg")
        ticket = Ticket.objects.create(
            title="Vu Geostrategix, Intéressant et accessible ?",
            description="""
                Interdum et malesuada fames ac ante ipsum primis in faucibus.
                Ut gravida dapibus dictum. Morbi quis faucibus augue.
                Pellentesque et fringilla metus. Vivamus dictum, arcu imperdie.
                Tempus tristique, augue sapien aliquam nisi, cursus condimentum turpis.
                """,
            user=user,
            image="./art_de_la_guerre.jpg",
            has_been_reviewed=True
        )
        ticket.save()
        print(f"{Fore.GREEN}[DUMMY TICKETS CREATED]{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[DUMMY TICKET+REVIEW CREATION]{Style.RESET_ALL}")
        # keep in mind that user 1 is the default admin
        # on crée 1 seule instance "demande critique + critique" au nom du user id=2
        # la création d'une critique passe par la création traditionnelle d'un ticket
        user = User.objects.get(id=2)
        img = Image.open(r"./images_livres_echantillon/art_de_la_repartie.jpg")
        img.thumbnail(settings.IMAGE_PREFERED_SIZE)
        img = img.save(fp="./media/art_de_la_repartie.jpg")
        ticket = Ticket.objects.create(
            title="Vu Art de la répartie, contenu original ?",
            description="""
                Morbi ac dui fermentum, tincidunt augue vitae, consequat massa.
                Proin pellentesque dolor eget odio porttitor laoreet.
                Nulla efficitur mauris vel nibh feugiat euismod.
                Aliquam tempor odio ac tortor egestas, nec varius dolor mattis. Curabitur vitae.
                """,
            user=user,
            image="./art_de_la_repartie.jpg",
            has_been_reviewed=True,
            time_created=datetime.today()
        )
        ticket.save()

        review = Review.objects.create(
            ticket=ticket,
            rating="3",
            headline="Y avait de l'idée, mais...",
            body="""
                Maecenas feugiat nec nulla ac rhoncus. Vestibulum posuere, ligula vel accumsan malesuada.
                Nisl tortor aliquam orci, et pharetra diam mauris vel lacus.
                Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;.
                """,
            user=user,
        )
        review.save()
        print(f"{Fore.GREEN}[DUMMY TICKET+REVIEW CREATED]{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[DUMMY REVIEWS CREATION]{Style.RESET_ALL}")
        # user id=3 makes a review for user id=2
        # the ticket id=1 is the one created by user id=2
        ticket = Ticket.objects.get(id=1)
        user = User.objects.get(id=3)
        review = Review.objects.create(
            ticket=ticket,
            rating="4",
            headline="Plutôt sympa",
            body="""
                Suspendisse eget elit est. Aenean porttitor interdum luctus.
                Integer nibh sapien, viverra vitae aliquam et, sollicitudin pretium arcu.
                Aenean vel augue lacus. Donec ultricies justo.
                """,
            user=user,
        )
        review.save()

        print(f"{Fore.GREEN}[DUMMY REVIEWS CREATED]{Style.RESET_ALL}")
