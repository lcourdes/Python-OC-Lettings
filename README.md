## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure
- Un compte Docker Hub
- Un compte Sentry
- Un compte AWS

### macOS / Linux

#### Cloner le repository

```sh
cd /path/to/put/project/in
git clone https://github.com/lcourdes/Python-OC-Lettings.git
```

#### Créer l'environnement virtuel

```sh
cd /path/to/Python-OC-Lettings-FR
python -m venv venv
```
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site en local

- Copier le fichier *local_run.sh.example*
```sh
cd /path/to/Python-OC-Lettings-FR
cp local_run.sh.example local_run.sh
```

- Modifier les informations dans le fichier obtenu pour configurer votre session.
  - Mode Debug : True ou False
  - Votre clé secrète Django
  - Les hôtes autorisés

```sh
cd /path/to/Python-OC-Lettings-FR
source venv/bin/activate
pip install -r requirements.txt
bash local_run.sh
```

- Aller sur `http://localhost:8000` dans un navigateur.

#### Linting

```sh
cd /path/to/Python-OC-Lettings-FR
source venv/bin/activate
flake8
```

#### Tests unitaires

- Copier le fichier *pytest_run.sh.example*
```sh
cd /path/to/Python-OC-Lettings-FR
cp pytest_run.sh.example pytest_run.sh
```

- Modifier les informations dans le fichier obtenu pour configurer votre session.
  - Mode Debug : True ou False
  - Votre clé secrète Django
  - Les hôtes autorisés

```sh
cd /path/to/Python-OC-Lettings-FR
source venv/bin/activate
bash pytest_run.sh
```

#### Base de données

```sh
cd /path/to/Python-OC-Lettings-FR
export DJANGO_SECRET_KEY='your_secret_key'
python3 manage.py dbshell # Pour ouvrir une session shell `sqlite3`
.open oc-lettings-site.sqlite3 # Pour se connecter à la base de données
.tables # Pour afficher les tables de la base de données
pragma table_info (profiles_profile); # Pour afficher la synthèse du tableau des profils
select user_id, favorite_city from profiles_profile where favorite_city like 'B%'; # Pour lancer une requête sur la table des profils 
.quit # Pour quitter
```

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`


#### Docker

Pour créer une image Docker : 

```sh
cd /path/to/Python-OC-Lettings-FR
source venv/bin/activate
docker build . --tag your_tag_name 
```

Pour envoyer l'image Docker ainsi créée sur votre Docker Hub :
- Prérequis : créez un repository public sur votre Docker hub.

```sh
docker login # Entrez votre nom d'utilisateur et votre mot de passe
docker push docker_username/repository_name:your_tag_name
```

Pour récupérer votre image Docker et la lancer en local.

- Copier le fichier *docker_run.sh.example*
```sh
cd /path/to/Python-OC-Lettings-FR
cp docker_run.sh.example docker_run.sh
```

- Modifier les informations dans le fichier obtenu pour configurer votre session.
  - Mode Debug : True ou False
  - Votre clé secrète Django
  - Les hôtes autorisés
  - La clé DSN de votre projet sentry

```sh
cd /path/to/Python-OC-Lettings-FR
bash docker_run.sh docker_username/repository_name:your_tag_name
```

#### Déploiement sur AWS

Prérequis :
- Avoir un compte AWS
- Avoir un nom de domaine qui pointe sur le DNS public d'une instance EC2
- Avoir une instance EC2 sur laquelle : 
  - nginx est installé
  - avoir un certificat ssl (par exemple obtenu avec certbot) dont le nom et la clé privée sont stockées dans :
    - /etc/letsencrypt/live/your_domain_name.com/fullchain.pem;
    - /etc/letsencrypt/live/your_domain_name.com/privkey.pem;

Connectez-vous à votre instance soit directement depuis votre compte AWS, soit depuis un terminal local en utilisant votre ssh obtenu lors de la création de l'intance EC2.

Créez un fichier de configuration nginx :

```sh
sudo nano /etc/nginx/conf.d/domain_name.conf
```

Copiez le contenu du fichier de configuration *domain_name.conf.example* dans le fichier de configuration de nginx.

Dans ce fichier, renseignez votre nom de domaine. Si votre certificat SSL est stocké différemment de ce qui est énoncé dans les prérequis, renseignez son chemin d'accès. 

Afin d'assurer le déploiement sur votre instance EC2 redémarrez nginx : 
```sh
sudo systemctl restart nginx
```

Tout comme sur votre machine locale vous pouvez récupérer une image depuis votre Docker Hub pour la lancer sur votre instance EC2.

#### Sentry

Prérequis : 
- Avoir un compte sentry
- Créer un projet django dans sentry

Vous pouvez renseigner le DNS de votre projet sentry dans le fichier *docker_run.sh*
Les transactions seront alors visibles dans votre dashboard Sentry.

Afin de vérifier la bonne configuration de Sentry, accédez depuis votre navigateur à `/sentry-debug/` pour déclencher une erreur. 

#### Pipeline CI/CD

La pipeline CI/CD est actuellement gérée dans le fichier *github/workflows/github-actions.yml*. La pipeline s'exécute pour tout push sur votre repository Github via Gitactions. 

Pour que la pipeline fonctionne correctement, dans *votre repository Github -> Settings -> Security -> Secrets and Variables -> actions* renseignez les informations de la manière suivante : 

| Key                | Value                                                                                                      |
|--------------------|------------------------------------------------------------------------------------------------------------|
| AWS_HOSTNAME       | Il s'agit du DNS public de l'instance EC2. Exemple : 'ec2-00-000-000-00.eu-west-3.compute.amazonaws.com'   |
| AWS_PRIVATEKEY     | Il s'agit du contenu complet de la clé privée (fichier .pem) obtenue lors de la création de l'instance EC2 |
| AWS_USERNAME       | Si votre instance EC2 a été lancée sur une machine Amazon Linux : 'ec2-user'                               |
| DJANGO_SECRET_KEY  | Votre clé Django secrète                                                                                   |
| DOCKERHUB_PASSWORD | Votre mot de passe ou token d'accès à votre compte Docker Hub                                              |
| DOCKERHUB_USERNAME | Votre nom d'utilisateur Docher Hub                                                                         |
| SENTRY_DSN         | "https://your_sentry_id.ingest.sentry.io/your_project_id"                                                  |


Actions de la pipeline : 
  - Push sur toute autre branche que 'main' : 
    - Vérification du linting avec flake8
    - Vérification des tests avec pytest
  - Push sur 'main' : 
    - Vérification du linting avec flake8
    - Vérification des tests avec pytest
    - Création d'une image Docker (dont le tag correspond au has du commit en cours) envoyée sur votre Docker Hub
    - Connection à votre instance AWS EC2
    - Récupération de l'image Docker 
    - Déploiement de l'image sur votre instance EC2