## Objectifs
1) Déployer manuellement l'app sur heroku cloud
2) Réaliser un changement en local et déployer manuellement sur Heroku
3) Mettre en place un pipeline de CI/CD vers Github avec déploiement sur Heroku
4) Réaliser un changement en local, lancer le pipeline et déployer sur heroku

## Réalisations

### 1. Déploiement manuel de l'application

#### Login (si ce n'est pas déjà fait)
```
$ heroku login
```

#### Préparer un environnement pour l'application à déployer
```
$ heroku create
```

#### Déployer
Le déploiement consiste à pousser les sources sur l'environnement créé, puis créer l'environnement logiciel (l'exécuteur python avec ses librairies)
```
git push heroku main
```

> A l'issue de cette étape, un log apparaît dans le terminal avec, vers la fin, l'url d'accès de votre application. Elle est de la forme `https://serene-caverns-82714.herokuapp.com/` avec un nom et un id numérique générés aléatoirement.

#### Provisionner des ressources de compute
Le déploiement ne suffit pas à lancer l'application, il faut ensuite provisionner des ressources de calcul (ou _compute_)
```
heroku ps:scale web=1
```

> A la fin du TP, penser à réduire à 0 la ressource de _compute_ provisionnés en répétant la commande ci-dessus avec '0' à la place de '1'.

### 2. Réaliser un changement en local et déployer manuellement sur Heroku

#### Implémenter une nouvelle fonction

Objectif : ajouter une fonction dans le script de récupération des données `fecth_data.py` pour collecter automatiquement les 7 derniers jours de données à partir de la date du jour. La zone à compléter est identifiée par un `TODO`.

Signature de la fonction
```
def calculate_date_from_delta(n_days: int, date_start: datetime = None):
```

Documentation de la fonction
```
Calcule une date suivant une date d'origine et un delta en jours.
Si la date d'origine est laissée vide, la fonction considérer la date d'aujourd'hui.
Retourne la date calculée au format d'une string "%Y-%m-%d"

Args:
    n_days (int): nombre de jours à retrancher
    date_start (datetime, optional): date d'origine. Defaults to None.

Returns:
    str: date calculée, au format "%Y-%m-%d"
```

Code de l'appel dans le main du fichier `fetch_data.py` (déjà présent)
```
last_n_days: int = 7

for d in range(0, last_n_days + 1):
    date: str = calculate_date_from_delta(d)
    print(date)
    fetch_data(build_url(date))
```

Tests unitaires : afin de valider le code de la fonction, un script de tests unitaires est fourni dans le dossier `test`. L'exécution du script devrait valider les 3 tests.

L'exécution du script se fait de la manière suivante :
```
# Powershell

# activer l'environnement
$ .\.venv\Scripts\activate

# exécuter les tests
$ $env:PYTHONPATH=$PWD; python.exe .\test\TestCalculateDateFromDelta.py
```

> Il est nécessaire d'activer l'environnement python crée avec venv pour exécuter le test dans les conditions du réel. Si l'activation ne fonctionne pas, penser à changer temporairement les _policies_ d'exécution à l'aide de la commande suivante :

```
# Powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

#### Test en local
```
$ heroku local -f Procfile.windows
```

#### Résultat attendu
Vous devriez voir le graphique qui contient maintenant un historique de 7 jours de données.

#### Déploiement manuel de l'application sur heroku

Commiter les changements puis déployer sur le cloud.
```
git push heroku main
```

Vérifier la ressource de compute associée à l'application et l'augmenter le cas échéant
```
# vérifier la ressource
$ heroku ps:scale

# ajouter une ressource si elle est à 0
$ heroku ps:scale web=1
```

### 3. Pipeline de CI/CD

TODO

### 4. Exécution du pipeline après un changement local

TODO