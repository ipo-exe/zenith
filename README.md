# 🌟 zenith 🌟
Zenith holds the core principles for working efficiently

Check out updated [General Principles](https://github.com/ipo-exe/zenith/blob/main/principles.md).

---

Objective: 
1. Repositorio tem site para hospedar docsites? (SPHINX, como funciona?)
1. Importar o PLANS, importar o LOS ALAMOS (repos são toolings, LosAlamos é para pesquisa)
1. Em tempo real atualizar o root conforme novos projetos surgem. Como fica o fluxo?  
R.: `uv add <aliasName>@git+https://github.com/ipo-exe/losalamos.git@<branch/commit/tag>`

base_object -> base_class
(it is a class)
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