# Projet Wolf

Wolf Status

[![Documentation Status](https://readthedocs.org/projects/wolf-project/badge/?version=latest)](https://wolf-project.readthedocs.io/?badge=latest) [![Unittest](https://github.com/Eirlab/wolf/actions/workflows/unittest.yml/badge.svg)](https://github.com/Eirlab/wolf/actions/workflows/unittest.yml)

Wolf-Core Status

[![Documentation Status](https://readthedocs.org/projects/wolf-project/badge/?version=latest)](https://wolf-project.readthedocs.io/?badge=latest) [![Wolf Core](https://github.com/Eirlab/wolf-core/actions/workflows/unittest.yml/badge.svg)](https://github.com/Eirlab/wolf-core/actions/workflows/unittest.yml) [![Publish to Test PyPI](https://github.com/Eirlab/wolf-core/actions/workflows/publish.yaml/badge.svg)](https://github.com/Eirlab/wolf-core/actions/workflows/publish.yaml)

Le projet Wolf est un projet ayant pour but de créer un environnement d'interconnexion entre les différents outils pouvant être utilisés dans la gestion d'associations, de projets
etc

## Installation

Pour installer le projet, suivez les instructions ci-dessous :

Clonez le projet sur votre machine en utilisant la commande suivante :
bash

```bash
git clone git@github.com:sedelpeuch/wolf.git
```

### Installation pour les utilisateurs

Créez un environnement virtuel et installez le package :

```bash
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip install poetry
poetry install

```

### Installation pour les développeurs

Le projet utilise des submodules Git, vous devez donc les initialiser comme suit :

```bash
git submodule init
git submodule update
cd core
git checkout main
```

Ensuite, installez les dépendances du projet et le package wolf_core :

```bash
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip install poetry
cd core
poetry install
```

### Configuration

Le projet utilise les arguments de la ligne de commande pour définir les paramètres de connexion à divers outils. Vous pouvez placer vos tokens directement via les arguments de la
ligne de commande.

```bash
python install.py --token1 VOTRE_TOKEN1 --token2 VOTRE_TOKEN2 ...
```

N'oubliez pas de remplacer VOTRE_NOTION_TOKEN et VOTRE_DOLIBARR_TOKEN par vos véritables tokens.
Vous pouvez également placer vos tokens dans le fichier `install.py`.

Pour enregistrer la configuration et lancer le projet en tant que service systemd, exécutez la commande suivante :

```bash
deactivate
sudo python3 install.py
```

## Documentation

La documentation complète du projet est disponible dans le répertoire /docs. Vous pouvez consulter cette documentation
pour en savoir plus sur les
fonctionnalités du projet et son utilisation.

La documentation est disponibe en ligne à l'adresse suivante : https://wolf-eirlab-community.readthedocs.io/

## Contributions

Nous accueillons avec plaisir les contributions à notre projet ! Si vous souhaitez contribuer, veuillez suivre les
étapes suivantes :

- Forker le dépôt
- Créer une nouvelle branche
- Effectuer vos modifications
- Valider vos changements
- Pousser votre branche
- Soumettre une pull request

Nous apprécions les contributions de la communauté pour améliorer et faire évoluer le projet Wolf !

## Licence

Ce projet est distribué sous licence GPL3. Pour plus d'informations, veuillez consulter le fichier LICENSE.

Nous espérons que le projet Wolf répondra à vos besoins de gestion des ressources internes. N'hésitez pas à nous
contacter si vous avez des questions
ou des commentaires. Merci de votre intérêt pour notre projet !
