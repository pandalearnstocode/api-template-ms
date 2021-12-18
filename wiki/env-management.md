# Using `poetry`

## Useful commands

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
source $HOME/.poetry/env
poetry --version
poetry self update
poetry new project1
cd project1
tree .
poetry run pytest
poetry add pandas
poetry remove pandas
poetry add --dev pytest
poetry add -D coverage[toml] pytest-cov # --dev & -D same
poetry install
poetry build
poetry publish
poetry export - requirements.txt --output requirements.txt
poetry use python3.8
```
## Some important information

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

```
# Run dotnet build and package
- name: dotnet build and publish
run: |
    dotnet restore
    dotnet build --configuration '${{ env.BUILD_CONFIGURATION }}'
    dotnet pack -c '${{ env.BUILD_CONFIGURATION }}' --version-suffix $GITHUB_RUN_ID

# Publish the package to Azure Artifacts
- name: 'dotnet publish'
run: dotnet nuget push --api-key AzureArtifacts bin/Release/*.nupkg
```