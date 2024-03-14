# Objectifs
1) Déployer manuellement l'app sur heroku cloud
2) Réaliser un changement en local et déployer manuellement sur Heroku
3) Mettre en place un pipeline de CI/CD vers Github avec déploiement sur Heroku
4) Réaliser un changement en local, lancer le pipeline et déployer sur heroku

# Réalisations

## 1. Déploiement manuel de l'application

### Login (si ce n'est pas déjà fait)
```
$ heroku login
```

### Préparer un environnement pour l'application à déployer
```
$ heroku create
```

### Déployer
Le déploiement consiste à pousser les sources sur l'environnement créé, puis créer l'environnement logiciel (l'exécuteur python avec ses librairies)
```
git push heroku main
```

> A l'issue de cette étape, un log apparaît dans le terminal avec, vers la fin, l'url d'accès de votre application. Elle est de la forme `https://serene-caverns-82714.herokuapp.com/` avec un nom et un id numérique générés aléatoirement.

### Provisionner des ressources de compute
Le déploiement ne suffit pas à lancer l'application, il faut ensuite provisionner des ressources de calcul (ou _compute_)
```
heroku ps:scale web=1
```

> A la fin du TP, penser à réduire à 0 la ressource de _compute_ provisionnés en répétant la commande ci-dessus avec '0' à la place de '1'.

## 2. Réaliser un changement en local et déployer manuellement sur Heroku

### Implémenter une nouvelle fonction

Objectif : ajouter une fonction dans le script de récupération des données `fecth_data.py` pour collecter automatiquement les 7 derniers jours de données à partir de la date du jour. La zone à compléter est identifiée par un `TODO`.

Signature de la fonction
```python
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
```python
def load_data_from_lag_to_today(n_days: int):
    for d in range(0, n_days + 1):
        date: str = calculate_date_from_delta(d)
        print(date)
        fetch_data(build_url(date))
```

Tests unitaires : afin de valider le code de la fonction, un script de tests unitaires est fourni dans le dossier `test`. L'exécution du script devrait valider les 3 tests.

L'exécution du script se fait de la manière suivante :
```powershell
# Powershell

# activer l'environnement
$ .\.venv\Scripts\activate

# exécuter les tests
$ $env:PYTHONPATH=$PWD; python.exe .\test\TestCalculateDateFromDelta.py
```

> Il est nécessaire d'activer l'environnement python crée avec venv pour exécuter le test dans les conditions du réel. Si l'activation ne fonctionne pas, penser à changer temporairement les _policies_ d'exécution à l'aide de la commande suivante :

```powershell
# Powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### Test en local
```
$ heroku local -f Procfile.windows
```

#### Résultat attendu
Vous devriez voir le graphique qui contient maintenant un historique de 7 jours de données.

### Déploiement manuel de l'application sur heroku

Commiter les changements puis déployer sur le cloud.
```
git push heroku main
```

Vérifier la ressource de compute associée à l'application et l'augmenter le cas échéant
```powershell
# vérifier la ressource
$ heroku ps:scale

# ajouter une ressource si elle est à 0
$ heroku ps:scale web=1
```

## 3. Pipeline de CI

### Workflow CI Github

1. **Créez un fichier de workflow GitHub Actions**

   Dans votre dépôt GitHub, créez un dossier `.github/workflows` si ce n'est pas déjà fait. Ensuite, créez un fichier YAML pour votre workflow, par exemple `deploy.yml`.

   > Documentation vers un workflow de projet en python https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python

2. **Configurez le fichier de workflow**

   Ouvrez votre fichier YAML et configurez votre workflow. Voici un exemple de configuration qui installe les dépendances Python, effectue du formattage de code (_linting_) avec `black` et `flake8` :

   ```yaml
    name: Python application CI

    on:
      push:
        branches: [ "main" ]

    permissions:
      contents: read

    jobs:
      build:

        runs-on: ubuntu-latest

        steps:
        - uses: actions/checkout@v4
        - name: Set up Python 3.11
          uses: actions/setup-python@v4
          with:
            python-version: '3.11'
            cache: 'pip'
        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install flake8 pytest
            if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        - name: Lint with flake8
          run: |
            # stop the build if there are Python syntax errors or undefined names
            flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
            # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
            flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
        - name: Lint with black
          uses: psf/black@stable  # formatting with black
          continue-on-error: true

   ```

3. **Poussez vos changements**

   Après avoir configuré votre fichier YAML, poussez-le dans votre dépôt GitHub. Le workflow sera déclenché sur les événements configurés, par exemple un `push` sur la branche `main`.

5. **Vérifiez l'exécution du workflow**

   Allez dans l'onglet Actions de votre dépôt GitHub pour suivre l'exécution de votre workflow et vérifier le déploiement.


#### Ajouter un test unitaire au workflow
- ajouter un test unitaire dans le workflow
  - créer le test
  - l'exécuter en local
  - ajouter les lignes qui vont bien dans le workflow
- ajouter un test d'intégration dans le workflow

### Pipeline de CI/CD

1. **Créez un fichier de workflow GitHub Actions**

   Dans votre dépôt GitHub, créez un dossier `.github/workflows` si ce n'est pas déjà fait. Ensuite, créez un fichier YAML pour votre workflow, par exemple `deploy.yml`.

   > https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python

2. **Configurez le fichier de workflow**

   Ouvrez votre fichier YAML et configurez votre workflow. L'exemple ci-dessous reprend le workflow pour l'intégration continue dans le job `build` et ajoute un job `deploy` pour le déploiement vers heroku :

   ```yaml
    name: CI on Github - CD on Heroku

    on:
    push:
        branches: [ "main" ]

    permissions:
    contents: read

    jobs:
    build:
        runs-on: ubuntu-latest

        steps:
        - uses: actions/checkout@v4
        - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
            python-version: '3.11'
            cache: 'pip'
        - name: Install dependencies
        run: |
            python -m pip install --upgrade pip
            pip install flake8 pytest
            if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        - name: Lint with flake8
        run: |
            # stop the build if there are Python syntax errors or undefined names
            flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
            # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
            flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
        - name: Lint with black
        uses: psf/black@stable  # formatting with black
        continue-on-error: true

    deploy:
        needs: build
        runs-on: ubuntu-latest
        steps:
        - uses: actions/checkout@v4
        - name: Set up Heroku
        uses: akhileshns/heroku-deploy@v3.13.15 # This is a popular GitHub Action for deploying to Heroku
        with:
            heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
            heroku_app_name: ${{ vars.HEROKU_APP_NAME }} # Replace with your Heroku app name
            heroku_email: ${{ secrets.HEROKU_EMAIL }} # Your Heroku account email
            # Optional: Add this if your project is not at the repo root
            # appdir: "your-app-directory"

   ```

3. **Configurez vos secrets et vos variables sur GitHub**

   Dans GitHub, allez dans les paramètres de votre dépôt (Settings), puis dans Secrets. Ajoutez vos secrets `HEROKU_API_KEY` et `HEROKU_EMAIL`. Vous pouvez obtenir votre clé API Heroku dans les paramètres de votre compte sur Heroku. Suivez la même procédure pour la variable du nom d'application.

   > Références
   https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository
   https://devcenter.heroku.com/articles/authentication#retrieving-the-api-token

4. **Poussez vos changements**

   Après avoir configuré votre fichier YAML, poussez-le dans votre dépôt GitHub. Le workflow sera déclenché sur les événements configurés, par exemple un `push` sur la branche `main`.

5. **Vérifiez le déploiement**

   Allez dans l'onglet Actions de votre dépôt GitHub pour suivre l'exécution de votre workflow et vérifier le déploiement.
