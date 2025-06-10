# Projet softdesk

Créez une API sécurisée RESTful en utilisant Django REST

## Contexte :

SoftDesk, une société d'édition de logiciels de collaboration, a décidé de publier une application permettant de remonter et suivre des problèmes techniques.

### **Prérequis :** 

+ Un environnement de développement (VSCode, Pycharm...)
+ Python 3.X
+ avoir installé pipenv (gestionnaire de packages et d'environnement pour python) s'il n'est pas présent

### Exécution des commandes

Sous Windows : avec la ligne de commandes (cmd)

Sous Linux : dans le bash

### Pour récuperer les fichiers du projet :

https://github.com/NicolasF425/softdesk.git

## Environnement virtuel

dans le répertoire du projet (softdesk normalement), exécuter pipenv install puis pipenv shell pour activer l'environnement

### Fonctionnement

Aller dans le répertoire du projet

lancer l'api : python manage.py runserver 

## Endpoints locaux

url de base : http://127.0.0.1:8000/

Console administrateur : ...admin/

Création et listing des User : ...api/user/

Modification et suppression d'un User : .../api/user/id_user/

Création et listing des Project : ...api/project/

Modification et suppression d'un Project : .../api/project/id_project/

Création et listing des Issue : ...api/issue/

Modification et suppression d'un Issue : .../api/issue/id_issue/

Création et listing des Comment : ...api/comment/

Modification et suppression d'un Comment : .../api/comment/id_comment/

# Utilisation du token JWT

.../api/token/ pour demander un token au serveur

.../api/token/refresh/ pour demander un nouveau token après expiration du précédent

## Restrictions d'accès (hors accès superuser)

L'utilisateur peut se créer un compte sans restrictions d'accès

L'accès en lecture aux projets, issues et comments est limité aux utilisateurs inscrits et contributeurs

La modification ou la suppression d'un compte, d'un projet, d'une issue ou d'un comment ne peut être réalisée que par le propriétaire de la ressource

!!! La suppression d'une ressource provoque la suppression des ressources liées (supprimer un compte utilisateur entrainera la suppression des touts les projets, et issues et commentaires liés à ces projets)












