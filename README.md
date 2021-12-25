# RESTful API template


pr v2 validation


<!-- Add status badge here after we get it from sonarcloud or ci/cd pipeline. -->

- [RESTful API template](#restful-api-template)
  - [Deployment URL:](#deployment-url)
  - [Tech stack:](#tech-stack)
  - [Important resource:](#important-resource)
  - [TODO checklist:](#todo-checklist)
  - [Directory structure](#directory-structure)
  - [Setup virtual env using venv](#setup-virtual-env-using-venv)
  - [Setup virtual env using conda](#setup-virtual-env-using-conda)
  - [Setup docker & docker compose in development env](#setup-docker--docker-compose-in-development-env)
  - [Setup commit rules & pre-commit hooks in local](#setup-commit-rules--pre-commit-hooks-in-local)
    - [Install pre-commit hook & commitizen](#install-pre-commit-hook--commitizen)
    - [Run pre-commit hook on all the files](#run-pre-commit-hook-on-all-the-files)
    - [Run pre-commit hooks while committing code](#run-pre-commit-hooks-while-committing-code)
    - [Rebase feature branch with `develop`](#rebase-feature-branch-with-develop)
    - [Writing commit msg using conventional commit for semver](#writing-commit-msg-using-conventional-commit-for-semver)
    - [Create and push tags from staging](#create-and-push-tags-from-staging)
  - [Running application as docker-compose](#running-application-as-docker-compose)
    - [Build docker containers](#build-docker-containers)
    - [Run docker compose file as dev env](#run-docker-compose-file-as-dev-env)
    - [Run docker compose file as staging env](#run-docker-compose-file-as-staging-env)
  - [Create and push docker images to container registry from local](#create-and-push-docker-images-to-container-registry-from-local)
  - [Run application in local development env](#run-application-in-local-development-env)
  - [SQLite DB for development](#sqlite-db-for-development)
    - [Generate alembic settings](#generate-alembic-settings)
    - [Update alembic settings](#update-alembic-settings)
  - [Alembic migration](#alembic-migration)
    - [Generate alembic migration settings](#generate-alembic-migration-settings)
    - [Update data models in `models.py`](#update-data-models-in-modelspy)
    - [Update API endpoints in `main.py`](#update-api-endpoints-in-mainpy)
    - [Run DB migration](#run-db-migration)
  - [Running DB from docker compose and using DB management tools](#running-db-from-docker-compose-and-using-db-management-tools)
  - [How to use Makefile](#how-to-use-makefile)
  - [Creating & pushing docker image to docker registry from local](#creating--pushing-docker-image-to-docker-registry-from-local)
  - [Steps after creating a new repository using the API template](#steps-after-creating-a-new-repository-using-the-api-template)
  - [DNS settings:](#dns-settings)
  - [Ports and URLs:](#ports-and-urls)
  - [Cloud components:](#cloud-components)
  - [Running in minikube using skaffold](#running-in-minikube-using-skaffold)
  - [Diagrams:](#diagrams)
    - [Event driven microservice architecture](#event-driven-microservice-architecture)
    - [Architecture diagram will be here](#architecture-diagram-will-be-here)
    - [Network diagram will be here](#network-diagram-will-be-here)
    - [Deployment diagram will be here](#deployment-diagram-will-be-here)
    - [Data Backup diagram will be here](#data-backup-diagram-will-be-here)
  - [Connecting with the dev VM in azure:](#connecting-with-the-dev-vm-in-azure)
  - [CI/CD pipeline:](#cicd-pipeline)
    - [Running GitHub actions as service](#running-github-actions-as-service)
    - [CI pipeline:](#ci-pipeline)
    - [CD pipeline:](#cd-pipeline)
  - [SCM workflow:](#scm-workflow)
    - [Development flow:](#development-flow)
    - [Release management workflow:](#release-management-workflow)
      - [1st tag has to be created manually](#1st-tag-has-to-be-created-manually)
    - [Automated testing workflow:](#automated-testing-workflow)
    - [Continuous delivery approval based workflow:](#continuous-delivery-approval-based-workflow)
  - [Env variables:](#env-variables)
  - [Deployment envs:](#deployment-envs)
    - [Container names in different envs:](#container-names-in-different-envs)
  - [DL linked with the project:](#dl-linked-with-the-project)
  - [Dependency files:](#dependency-files)
  - [Exploring `poetry` for dependency management in python](#exploring-poetry-for-dependency-management-in-python)
    - [Some useful `poetry` commands](#some-useful-poetry-commands)
    - [Some important information](#some-important-information)
    - [Important files](#important-files)
    - [Publishing library as artifact to artifact store](#publishing-library-as-artifact-to-artifact-store)
  - [Developers working on the project:](#developers-working-on-the-project)
  - [Reference:](#reference)



## Deployment URL:

* [Dev Deployment CD Pipeline](https://github.com/pandalearnstocode/api-template-ms/blob/develop/.github/workflows/dev-deployment.yml)


## Tech stack:

* __Language:__ Python
* __Version:__ 3.8
* __API:__ FastAPI
* __DB:__ SQLite, PostgreSQL
* __DB Manager:__ pgAdmin
* __Containerization:__ Docker, Docker Compose
* __Latest stable version:__ 0.0.0
* __Last release date:__ 15/12/2021
* __Release notes:__ URL of release note file <!-- TODO: Update this whenever available -->
* __Change logs:__ URL of change log file  <!-- TODO: Update this whenever available -->


![Backend tech stack](./static/backend-teckstack.png)

<!-- Editable link here: https://lucid.app/lucidchart/9a3ac5ca-550d-4725-b86a-229a7efa4c21/edit?invitationId=inv_3865e75a-5277-413f-88ae-477ca86d3b31 -->

## Important resource:

<!-- TODO: Populate the following details as and when it is available for the project. -->

* Project wiki :
* SonarCloud :
* Snyk :
* Container Registry :
* Azure RG :
* Azure Subscription :
* CI Pipeline:
* CD Pipeline:
* Monitoring tool:
* Cloud resource tracker:

## TODO checklist:

- [] update unfinished sections of the readme file
- [] migrate content of the readme file to the project wiki
- [] configure meaningful rules from flake8, pylint, black, bandit and pydocstring for API development
- [] setup minikube, [tilt](https://tilt.dev/) & [skaffold](https://skaffold.dev/).
- [] configure poetry. refer [this](https://github.com/nsidnev/fastapi-realworld-example-app/)
- [] check how to get rid of multiple docker, docker compose, env and requirements files.
- [] checkout [this](https://github.com/Kludex/fastapi-microservices) `bump lib to arq==0.22` : working
- [] checkout [this](https://github.com/karthikasasanka/fastapi-celery-redis-rabbitmq) : not verified

<!-- TODO: Update the following tree structure with updated folder structure. -->

## Directory structure

```bash
.
├── app                                 # primary application folder
│   ├── apis                            # this houses all the API packages
│   │   ├── api_a                       # api_a package
│   │   │   ├── __init__.py             # empty init file to make the api_a folder a package
│   │   │   ├── mainmod.py              # main module of api_a package
│   │   │   └── submod.py               # submodule of api_a package
│   │   └── api_b                       # api_b package
│   │       ├── __init__.py             # empty init file to make the api_b folder a package
│   │       ├── mainmod.py              # main module of api_b package
│   │       └── submod.py               # submodule of api_b package
│   ├── core                            # this is where the configs live
│   │   ├── auth.py                     # authentication with OAuth2
│   │   ├── config.py                   # sample config file
│   │   └── __init__.py                 # empty init file to make the config folder a package
│   ├── __init__.py                     # empty init file to make the app folder a package
│   ├── main.py                         # main file where the fastAPI() class is called
│   ├── routes                          # this is where all the routes live
│   │   └── views.py                    # file containing the endpoints of api_a and api_b
│   └── tests                           # test package
│       ├── __init__.py                 # empty init file to make the tests folder a package
│       ├── test_api.py                 # functional testing the API responses
│       └── test_functions.py           # unit testing the underlying functions
├── Caddyfile                           # simple reverse-proxy with caddy
├── commitizen-setup.sh                 # a file to setup commit rules
├── data                                # data mount folder to get the data from cloud to local
│   ├── compression.py                  # utils file to fetch data from cloud storage
│   ├── get_data.py                     # utils file to fetch data from cloud storage
│   └── settings.py                     # utils settings file to fetch data from cloud
├── docker-compose.yml                  # docker-compose file
├── Dockerfile                          # dockerfile
├── docker-setup.sh                     # list of commands to setup docker and docker compose in local
├── Makefile                            # Makefile to apply Python linters
├── mkdocs.yaml                         # MkDocs wiki page settings
├── mypy.ini                            # type checking configs
├── pydocstyle_wrapper.py               # Wrapper function to extract logs from flake8, mypy, pydocstyle
├── pyproject.toml                      # pep-518 compliant config file
├── README.md                           # a basic readme template
├── requrements-dev.in                  # .in file to enlist the top-level dev requirements
├── requirements-dev.txt                # pinned dev dependencies
├── requirements.in                     # .in file to enlist the top-level app dependencies
└── requirements.txt                    # pinned app dependencies
├── run_lint.sh                         # utils file to run QA/QC tasks in CI and extract output for SonarCloud
├── scripts                             # some of the reusable repetitive scripts can be stored here
│   └── update_deps.sh                  # update dependency script
├── static                              # any static artifacts can be stored in this folder
│   └── scm-workflow.png                # scm workflow diagram
├── templates                           # any reusable template can be stored in this folder
│   └── pull_request_template.md        # GitHub pull request template
└── wiki                                # mkdocs project wiki source files lives here
```

## Setup virtual env using venv

```bash
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
sudo apt-get install -y python3-venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt && pip install -r requirements-dev.txt
uvicorn app.main:app --port 5000 --reload
deactivate
```

## Setup virtual env using conda

```bash
conda create --name ca-be-api-template python=3.8
conda activate ca-be-api-template
pip install -r requirements.txt && pip install -r requirements-dev.txt
uvicorn app.main:app --port 5000 --reload
conda deactivate
```

## Setup docker & docker compose in development env

```bash
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache policy docker-ce
sudo apt install -y docker-ce
sudo usermod -aG docker ${USER}
su - ${USER}
sudo usermod -aG docker LinuxAdmin
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Update the version of docker and docker-compose with the latest stable version available. Change `LinuxAdmin` to the current user. 

## Setup commit rules & pre-commit hooks in local

### Install pre-commit hook & commitizen

```bash
pip install commitizen-emoji commitizen==2.20.0 pre-commit
pre-commit install
```

### Run pre-commit hook on all the files

```bash
pre-commit run --all-files
```

### Run pre-commit hooks while committing code

```bash
git add README.md
git commit . -m 'docs: quick fix in readme file' --no-verify
git push origin develop
```

### Rebase feature branch with `develop`

```bash
git pull origin develop --rebase
```

DO NOT change the history of working branch which is `develop` in this case. If there some change during merge, try to rebase feature branch with develop. Take all the income changes from develop and resolve merge conflict with the feature branch and then raise pull request.

### Writing commit msg using conventional commit for semver

To enforce the conventional commit rule either follow this or attach appropriate tags in the commit message.

```bash
git add .
cz -n cz_commitizen_emoji c
git push origin develop
```


### Create and push tags from staging

Normally this will be done in CI pipeline via pull request in the staging branch. But, just in case something breaks we should be able to run the following commands to generate the changelogs and tags and we can push that to remote.

```bash
cz bump --changelog --check-consistency
git push --tags
```

## Running application as docker-compose

### Build docker containers

```bash
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.staging.yml build
```

or


```bash
make build-docker-images
```

### Run docker compose file as dev env

```bash
make run-container-dev
make kill-container-dev
```

In case of dev env we are using sqlite db which is mounted in `app/database.db` file. Inside docker it is located in `code/app/database.db`. The same file is mounted in the docker volume named as `sqlite_data`. We are passing the from `dev.env` file as `DATABASE_URL` variable. This variable is retrieved in `app/config.py` in `Settings.db_url`. This variable must be used for all the place where we are going to refer a `db_url` (for db migration and in the FastAPI app). Same thing is applicable for all the other envs. In case we are using a cloud component in production this should be replaced with the cloud db url and should be passed as GitHub repository secret. 


### Run docker compose file as staging env

```bash
make run-container-staging
make kill-container-staging
```

If something is running on port 80, use the following command to kill the task running on port 80,

```bash
sudo kill -9 $(sudo lsof -t -i:80)
```

Check Swagger UI docs here: `http://0.0.0.0:6969/docs`

## Create and push docker images to container registry from local

```bash
docker build -t ca-mmm-be-api:v1 .
docker push mydockerregistry.acr.io/ca-mmm-be-api:v1
```

## Run application in local development env

```bash
make run-local
```

Check Swagger UI docs here: `http://0.0.0.0:5000/docs`

Note: In case of local env the `db_url` is coming from `.env` file as `DATABASE_URL` variable. `app/database.db` is added to gitignore file.

## SQLite DB for development

To view the record in the file we can we use the [DB browser](https://sqlitebrowser.org/) for SQLite.

### Generate alembic settings

```bash
alembic init alembic
```

### Update alembic settings

* replace `sqlalchemy.url = driver://user:pass@localhost/dbname` in `alembic.ini` with `sqlite:///database.db`. (this is just a example, in real use case this should be changed with the db uri parameter which should be passed from *.env file)
* in `alembic/env.py` file add `from sqlmodel import SQLModel` in the import section.
* in `alembic/env.py` file add the following line in import section, `from app.models import Task`.
* in `alembic/env.py` change `target_metadata = None` to `target_metadata = SQLModel.metadata`.
* in `alembic/script.py.mako` add `import sqlmodel` in the import section.

## Alembic migration

### Generate alembic migration settings

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

### Update data models in `models.py`

```python
from sqlmodel import SQLModel, Field
from typing import Optional # This is a new add line

class TaskBase(SQLModel):
    task_name: str
    task_description: Optional[str] = None # This is a new add line

class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)

class TaskCreate(TaskBase):
    pass
```

### Update API endpoints in `main.py`

In this case, endpoints remains unchanged but in a realistic scenario endpoints has to be changed to take the new information into account.

### Run DB migration

```bash
alembic revision --autogenerate -m "add description"
alembic upgrade head
```

## Running DB from docker compose and using DB management tools

<!-- TODO: Once staging docker compose file is done update it here. -->

## How to use Makefile

<!-- TODO: List all the functionalities of make file here and keep this up to date. -->

## Creating & pushing docker image to docker registry from local

## Steps after creating a new repository using the API template

## DNS settings:

* develop: dev.marketingbudgetallocator.live
* staging: staging.marketingbudgetallocator.live
* production: marketingbudgetallocator.live

## Ports and URLs:

* local: http://127.0.0.1:5000/docs
* dev: http://127.0.0.1:6969/docs
* staging: http://127.0.0.1:8000/docs
* production: https://127.0.0.1:443/docs


## Cloud components:

<!-- TODO: Once we select and deploy the cloud component the list should go here. -->

## Running in minikube using skaffold

```bash
minikube start
docker build -t hello-fastapi .
docker run -p 80:80 hello-fastapi
skaffold dev --port-forward
curl localhost:9000
docker ps
minikube delete --all
```

## Diagrams:

### Event driven microservice architecture

![Microservice with FastAPI](./static/microservice-fastapi.png)

<!-- Reference: https://www.merixstudio.com/blog/how-use-fastapi-microservices-python/ -->

### Architecture diagram will be here

### Network diagram will be here

### Deployment diagram will be here

### Data Backup diagram will be here

## Connecting with the dev VM in azure:

## CI/CD pipeline:

### Running GitHub actions as service

```bash
sudo ./svc.sh install
sudo ./svc.sh start
```
### CI pipeline:

<!-- TODO: Once CI pipeline is developed the description, how to use and automated behavior of the pipeline should go here. -->

### CD pipeline:

<!-- TODO: Once CD pipeline is developed the description, how to use and automated behavior of the pipeline should go here. -->

## SCM workflow:

* To check what all has to be fixed search for `fixme` or `TODO` in the project folder.
* List all the container name, base images, container registry and image in in container registry in README.md file.
* Post deployment to production if there is a `hotfix` the same changes should be reflected in `staging` and `develop` branch as well.

![SCM Workflow](./static/scm-workflow.png)

### Development flow:

Lets imaging that there is an issue in github repository which is assigned to you &#8594; To start development checkout a feature branch from `develop` for example `feature/#1-create staging docker-compose` &#8594; Modify code as required &#8594; Commit to staging area in local with smaller code changes (validated with pre-commit hook & commit msg structure) &#8594; Test the staging docker-compose is working &#8594; Write test case wherever possible to validate the feature (unit tests) &#8594; Update documentation &#8594;  Push code to feature branch &#8594; Raise a pull request with the attached issue/ ticket number/ card id from project, resolve merge conflict, if required rebase with the develop (flake8, pylint, pydocstyle, bandit, mympy) &#8594; Assign someone for peer review during rasing the pull request &#8594; During review take sonar cloud results into account &#8594; Further development & modification to the code to make include enhancement suggested in CI QA/QC pipeline &#8594; Finally once all the checks are validated merge pull request with develop and delete the feature branch. &#8594; Update the card in DevOps/GitHub Projects. Development workflow ends here.

### Release management workflow:

Once a new code is merge to develop &#8594; Create, scan, build & push docker image to container registry &#8594; Deploy the same image in the staging envs &#8594; Generate project wiki docs &#8594;Deploy project wiki docs &#8594; Run unit tests on the dev envs using GitHub actions &#8594; Communicate the tests results using a teams & mail notification.

#### 1st tag has to be created manually 

```bash
git tag -a 0.0.0 -m "Init version"
git push --tags 
git add .
git commit -m "fix: svc installed."
cz bump
cz changelog
```

```bash
git push origin :refs/tags/0.0.0 # delete tags from remote
git tag -d 0.0.0 # delete tags from local
```

After creating tag 0.0.0 CI pipeline will trigger based on commit msg while merging code from `develop` to `staging`.

### Automated testing workflow:

If the tests results are fine, run all the linting, formatting (black, autoflake8, isort) and other changes in the staging area. &#8594; Bump version, generate changelogs and release notes. &#8594; Update tags and releases in GitHub &#8594;Check if the dependency needs to be updated or not, if required to that &#8594; Commit code to staging branch &#8594; Trigger a build pipeline to deploy this in staging server &#8594; Run all the regression tests, integration tests, load tests here &#8594; Generate results and publish the same in project Wiki or some other place &#8594; Communicate build stats and tests result to via email & teams notification.

### Continuous delivery approval based workflow:

If all the tests results in staging looks good, raise a pull request to master &#8594; Merge pull request to master &#8594; Build and push docker image to container registry &#8594; Deploy to production &#8594; Wait for manual approval for the deployment with a wait time &#8594; Once approved, deploy in production and send notification.

![Branching model](./static/git-model.png)


Check gitflow related details [here](https://nvie.com/posts/a-successful-git-branching-model/).

## Env variables:

<!-- TODO: List down all the env variables & GitHub secrets used for the project. A location where all these variables are stored. -->

## Deployment envs:

<!-- TODO: List down all the envs where the application will be deployed. How it can be accessed. What all things will be performed in these respective envs. -->

### Container names in different envs:

<!-- TODO: What will be image name generated in different branches including rc branch and candidates. What should be the container name in the deployment files. How to map them with the developed featured. What should be the retaliation period for all the branches other than the master branch. -->

## DL linked with the project:

<!-- TODO: Create different DLs for different purpose and list down here once these are configured. These needs to be used in different pipelines and communication channel. -->

## Dependency files:

* dev
* staging
* prod
* tests
* docs

__Note:__ Right now, only `requirements.txt` is used for all the envs but this should be changed depending on envs. 


## Exploring `poetry` for dependency management in python

In general `pip` & `venv` is a good combination of tool when you don't have to manage multiple dependencies for your project. But imaging that in a project you need to management multiple dependency files to deploy code into multiple envs. It is possible to do this with `pip`, but in that case you need to manage multiple requirements files. To solve this project I have checked a few alternative like  `pyenv`, `pipx`, `pipenv`, `poetry` etc. According to my experience, poetry is the simplest and most efficient one. I was checking some of the useful tutorials about this and here I am just taking a note of some of the useful points regarding this tool.

### Some useful `poetry` commands

```bash
# Download poetry in Ubuntu
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
source $HOME/.poetry/env # Add to PATH
poetry --version # Check version of poetry
poetry self update # Update version
poetry new project1 # Create a new project
cd project1
tree . 
poetry run pytest # Run pytest for the project
poetry add pandas # Add a package as dependency of a project
poetry remove pandas # Delete a project from the file
poetry add --dev pytest # Add a package as dev dependency in a poetry project
poetry add -D coverage[toml] pytest-cov # --dev & -D same
poetry install # Install all the dependencies for a project
poetry build # Build a python library using poetry
poetry publish # Publish library to PyPI
poetry export - requirements.txt --output requirements.txt # Generate requirements.txt
poetry use python3.8 # Use specific version of python in the project
```

### Some important information

### Important files

* `pyproject.toml` is the single file for all project related metadata.
* `poetry.lock` file is the granular metadata.
* `.pypirc` will not work with poetry. 
* `config.toml` & `auth.toml` is used for setting up the artifact repository.
* export `POETRY_PYPI_TOKEN_PYPI`, export `POETRY_HTTP_BAISC_PYPI_USERNAME` and export `POETRY_HTTP_BAISC_PYPI_PASSWORD` can be used for this.

### Publishing library as artifact to artifact store

```toml
# config.toml : ~/.config/pypoetry/config.toml
[repositories]
pypi = {url = "https://upload.pypi.org/legacy/"}
testpypi = {url = "https://test.pypi.org/legacy/"}
```

```toml
# auth.toml: ~/.config/pypoetry/auth.toml
[http-basic]
pypi = {username = "myuser", password = "topsecret"}
testpypi = {username = "myuser", password = "topsecret"}
```

Check GitHub issue related to this [here](https://github.com/python-poetry/poetry/issues/111).


## Developers working on the project:

* __Primary owner:__
* __Secondary owner:__
* __Team members:__

## Reference:

* https://github.com/rednafi/fastapi-nano
* https://testdriven.io/blog/fastapi-sqlmodel/
* https://fastapi.tiangolo.com/advanced/async-sql-databases/
* https://github.com/encode/databases
* https://github.com/testdrivenio/fastapi-sqlmodel-alembic
* https://github.com/Lance0404/asiayo-rest-sql
* https://fastapi.tiangolo.com/tutorial/sql-databases/
* https://github.cdnweb.icu/smartgic/shortgic
* https://testdriven.io/blog/fastapi-sqlmodel/
* https://python.plainenglish.io/building-a-phone-directory-with-mysql-fastapi-and-angular-cd48673904f4
* https://alembic.sqlalchemy.org/en/latest/autogenerate.html
* https://towardsdatascience.com/build-an-async-python-service-with-fastapi-sqlalchemy-196d8792fa08
* https://hackernoon.com/how-to-set-up-fastapi-ormar-and-alembic
* https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
* https://testdriven.io/blog/fastapi-sqlmodel/
* https://shipit.dev/posts/trigger-github-actions-on-pr-close.html
* https://azure.github.io/AppService/2020/12/11/cicd-for-python-apps.html
* https://peterevans.dev/posts/github-actions-how-to-automate-code-formatting-in-pull-requests/
* https://itnext.io/a-beginners-guide-to-deploying-a-docker-application-to-production-using-docker-compose-de1feccd2893
