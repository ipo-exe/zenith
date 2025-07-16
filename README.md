# 🌟 zenith 🌟
Zenith holds the core principles for working efficiently

Check out updated [General Principles](https://github.com/ipo-exe/zenith/blob/main/principles.md).

---

## Sphinx dive in

**Sphinx** has a quickstart CLI. For instance, to create the following in the `docs` source directory:
- Separate source and build directories: no
- Project name: zenith
- Author name: Iporã Brito Possantti
- Project release: 0.0.1
- Project language: en  
`sphinx-quickstart docs --no-sep --project zenith --author "Iporã Brito Possantti" --release 0.0.1 --language en --ext-autodoc`

This creates
| file | description |
|---|---|
|conf.py| configuration|
|index.rst | table of content tree - toctree |

index.rst comes with the toctree rst directive, which is basically allows nesting rsts. Also the `ref` role allows cross-references to exist.

### Extensions
Useful extensions to add in the `conf.py`
```py
extensions = [
    'sphinx.ext.autodoc',

    # Readers can view the actual Python source of your functions/classes/modules directly from the docs.
    # Especially useful for open-source or public APIs.
    'sphinx.ext.viewcode',

    'sphinx.ext.githubpages',
]
```
#### Autodoc

Add this to conf.py if sphinx source root is kept in `./docs` and your package in `./src/package_name`
```python
# For autodoc
import sys
from pathlib import Path

sys.path.insert(0, str(Path('..', 'src').resolve()))

# For autodoc to use the type hinting
autodoc_typehints = "description"
```
Auto generate the .rst from package
`sphinx-apidoc -o docs package_name`
> to force overwrite, add `-f`

#### Git Hub Pages
1. Manually push to gh-pages Branch (Manual Setup)
    1. Build your docs `make html`
    1. Switch to a separate orphan branch:  
`git checkout --orphan gh-pages`
    1. Remove all tracked files and add the build  
    ```bash
    git rm -rf .
    cp -r docs/_build/html/* .
    touch .nojekyll  # (optional if you already use sphinx.ext.githubpages)
    ```

    4. Commit and push:
    ```bash
    git add .
    git commit -m "Deploy Sphinx docs to GitHub Pages"
    git push origin gh-pages --force
    ```

    5. On GitHub:  
    Go to your repository → Settings → Pages  
    Choose:    
        Source: gh-pages  
        Folder: / (root)

Your docs will be available at:  
`https://<your-username>.github.io/<your-repo>/`

2. GitHub Actions - Sphinx docs are built and published everytime you push

Example of `.github/workflows/deploy-docs.yml` to build the docs and push them to gh-pages.
```yml
name: Build and Deploy Sphinx Docs

on:
  push:
    branches:
      - main  # or change to your default branch

jobs:
  build-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: 3.11  # or your preferred Python version

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install sphinx
        pip install -r docs/requirements.txt || true  # optional, if you use it

    - name: Build HTML docs
      run: |
        cd docs
        make html

    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v4
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: docs/_build/html
        publish_branch: gh-pages
        force_orphan: true

```

### Build 
This generates the html page
`sphinx-build -M html docs docs/_built`

to let it autobuild, every time a change occurs
`sphinx-autobuild docs docs/_built`

> Watch out for `WARNING: XXX not included in toctree` (add them in index.rst)


---

Objective: 
1. Repositorio tem site para hospedar docsites? (SPHINX, como funciona?)
1. Importar o PLANS, importar o LOS ALAMOS (repos são toolings, LosAlamos é para pesquisa)
1. Em tempo real atualizar o root conforme novos projetos surgem. Como fica o fluxo?  
R.: `uv add <aliasName>@git+https://github.com/ipo-exe/losalamos.git@<branch/commit/tag>`

botar a documentacao do PLANS e os .rst para ver lado a lado

PLANS tem que ter um Manual para o usuario e nao so para o programador.
Ver se ha TODO tree no Pycharm
Zenith eh modelo para os projetos

ver como bota o uv no google collab, como chamar outros python no collab
test/benchmarking
test/unitest ou pytest
qnd roda o apidocs do Sphinx, ver como fazer mudan;as adicionais nos .rst
static page
Como fariamos para nao usar o Read-docs e emular tudo?

- Baixa o PLANS em um ambiente, roda build pelo sistema, roda sphinx apidocs,
- Se n houve erro, copia os html pro ipora github static pages, faz o commit
- Ajuste o README.md com a badge de 100% passado ou nao

A serious project, like a library thought to be used by others, must follow principles, such as using `tests` to ensure it stays stable; naming must be universal and logical.

---

## 🛠️ Installation
Get this repository model without the whole git history (shallow clone):  
`git clone --depth 1 git@github.com:ipo-exe/zenith.git`

---

Prerequisites is Python 3.8+ and `pipx` to install `uv` globally:
```bash
python -m pip install --user pipx
python -m pipx ensurepath
```
Get uv
```bash
pipx install uv
```
Create a project and initialize uv
```bash
mkdir my_project && cd my_project
uv venv  # creates a virtual environment
```
Activate the virtual environment
```bash
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\activate   # Windows
```
Manage dependencies
```bash
uv add/remove pandas numpy
```
### Custom GitHub lib
✅ Add dependency.
```bash
uv add "losalamos@git+https://github.com/ipo-exe/losalamos.git@latest"
```
This command...
- Updates `pyproject.toml`  
_(manifest of the whole project in a higher level)_
- Updates the `uv.lock`  
_(the update plan, like a receipt/manifest with hashes of the commits and repos)_
- Synchronizes the `uv.lock` with the actual `.venv`

🔄 Upgrade later
```bash
# Update plan (uv.lock) is modified to the latest commits/hashes
uv lock --upgrade-package losalamos

# Synchronize the uv.lock with the .venv
uv sync
```
Repeat for other libs like `zenith`, etc.  
_*All libs use the latest branch as the rolling release._