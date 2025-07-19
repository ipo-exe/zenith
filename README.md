# 🌟 zenith 🌟
Zenith holds the [General Principles](https://github.com/ipo-exe/zenith/blob/main/principles.md) and is a model for projects

Stable libraries have `tests` it stays stable; naming must be universal and logical for the community.

Short-term tasks: 
1. Repositorio tem site para hospedar docsites? (SPHINX, como funciona?)  
  \>> A documentacao do PLANS deve ter certos `.rst` que queremos evitar sobrescrever. Por exemplo, "PLANS tem que ter um Manual para o usuario e nao so para o programador". Discutir com Iporã  
  \>> Ajuste o README.md com a badge de 100% passado ou nao

1. Como importar os _tooling repos_ PLANS e, para pesquisa, LOS ALAMOS?  
  \>> No ambiente local com `uv`,
  `!uv add git+https://github.com/ipo-exe/zenith.git@docs/trying-sphinx`
  \>> No `Google Collab`,  
  `!pip install git+https://github.com/ipo-exe/zenith.git@docs/trying-sphinx`


1. Em tempo real atualizar o root conforme novos projetos surgem. Como fica o fluxo?  
   \>> Adicionei o `.pre-commit-config.yaml` para sempre fazer o `uv` atualizar antes de cada commit  
   \>> Deve adicionar `uv add --dev pre-commit` ao projeto, e instalar `uv run pre-commit install`  
R.: `uv add <aliasName>@git+https://github.com/ipo-exe/losalamos.git@<branch/commit/tag>`

Extra: Ver se ha TODO tree no Pycharm

test/benchmarking  
test/unitest ou pytest  

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

---

## Code Documentation via Sphinx

**Sphinx** has a quickstart CLI.  
To start Sphinx from the root of a project with layout `./src/package` with the following specs:
| | |
|---|---|
| Separate source and build directories | no |
| Project name | zenith |
| Author name | Iporã Brito Possantti |
| Project release | 0.0.1 |
| Project language | en   |
| Extensions | • AutoDoc <br>• ViewCode (_Readers can view the actual Python source of your functions/classes/modules directly from the docs. Especially useful for open-source or public APIs._ <br>• GitHubPages |

Run the following:
```bash
# Run at root to create the 'docs' folder in separate mode.
#   docs/source - .rst files & conf.py
#   docs/build  - build output
#   docs        - keeps 'make.bat' and 'Makefile'
uv run sphinx-quickstart docs --sep --project zenith --author "Iporã Brito Possantti" --release 0.0.1 --language en --ext-autodoc --ext-viewcode --ext-githubpages

# Adjust `conf.py` to use type hinting and to find your `./src/package_name`
uv run python -c "p='docs/source/conf.py'; l='import sys\\nfrom pathlib import Path\\n\\n# Allow sphinx to find the package\\nconf_dir = Path(__file__).parent\nsys.path.insert(0, str((conf_dir.parent.parent / \"src\").resolve()))\\n\\n# Enable autodoc using type hinting annotations\\nautodoc_typehints = \"description\"\\n\\n'; c=open(p, encoding='utf-8').read(); open(p, 'w', encoding='utf-8').write(l + c)"
```

Mind you that `index.rst` comes with the toctree rst directive, which enables nesting rsts. Also the `ref` role allows cross-references to exist. The `docs/source/_static` is for `.css, .js, .png, .svg` files

### **Activate GitHub Actions**: publish docs at every `PUSH`

Create the action at the branch root `./.github/workflows/deploy-docs.yml`.  
It will be necessary to allow your GitHub Token to give write permissions in the repo.

Enable it under `Repo Settings > Actions > General > Workflow Permissions`,  
by setting it to `Read and write permission`.