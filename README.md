![Screenshot](https://img.shields.io/badge/python-v3.10-blue?logo=python&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/django-v4-blue?logo=python&logoColor=yellow)
# [OpenClassRoom](https://openclassrooms.com/) - Parcours développeur Python
![Screenshot](oc_parcours_dev_python.png)
## Projet 9 - Développer une application Web en utilisant Django

### Description projet
Application permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande.

### Exigences
- [x] Utiliser le rendu côté serveur dans Django.
- [x] Développer une application web en utilisant Django.

## Comment utiliser le projet ?
1. Clone the repository

      `git clone https://github.com/memphis-tools/oc_projet9_appli_web_django.git`

      `cd oc_projet9_appli_web_django`

2. Setup a virtualenv

      `python -m venv env`

      `source env/bin/activate`

      `pip install -U pip`

      `pip install -r requirements.txt`

3. Run app with default dummy database

	You will find **3 users already created : donald, daisy and loulou**. You can choose to subscribe as new user.
	In order to test features you will also find some dummy projects, reviews and tickets:

    `python ./manage.py runserver`

    If you wish to remove any changes and go back the default dummy database:

    `python ./manage.py init_app_litreview`

    Optionnal - Run app from scratch

      `python ./manage.py reset_app_litreview`

      `python ./manage.py makemigrations`

      `python ./manage.py migrate`

      `python ./manage.py runserver`

## Comment fonctionne l'application ?
C'est une application WEB, dépourvue d'API. On demeure dans un cas d'exemple, de développement.

On simule une application utile à une communauté qui souhaite échanger des avis à propos de livres publiés (tout format).

Les publications possibles se décomposent en des demandes de critiques ('tickets'), et en des expressions de critiques ('reviews').

A 1 ticket correspond 1 critique.

Chaque utilisateur peut s'abonner ou se désabonner des publications d'un autre utilisateur.

Il faut considérer en l'état qu'il n'y a qu'un seul admin, avec un id=1. Si vous démarrez l'appli from scratch, il faut en préambule créer ce compte admin.

Deux profils utilisateurs sont prévus, mais il n'y a pas de prérogatives ou contraintes implémentées pour le moment.

Un utilisateur non connecté ne peut avoir accès qu'aux pages d'authentification /d'enregistrement.

Un utilisateur connecté peut ajouter un ticket, une critique en réponse à un ticket, ou enfin un 'couple ticket-critique'.

Un utilisateur connecté peut accéder à ses seules publications ("posts"). De plus, il peut modifier ou supprimer chacunes d'entre elles.

Une image n'est pas indispensable pour créer un ticket.

Une critique implique une notation graduée de 0 (le plus bas) à 5.
