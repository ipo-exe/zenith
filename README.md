# zenith
Zenith holds the core principles for working efficiently

Check out updated [General Principles](https://github.com/ipo-exe/zenith/blob/main/principles.md).

---

Objective: 
1. Repositorio tem site para hospedar docsites? (SPHINX, como funciona?)
1. Importar o PLANS, importar o LOS ALAMOS (repos são toolings, LosAlamos é para pesquisa)
1. Em tempo real atualizar o root conforme novos projetos surgem. Como fica o fluxo?

A serious project, like a library thought to be used by others, must follow principles, such as using `tests` to ensure it stays stable; naming must be universal and logical.

---
## Repo structure

Zenith repo follows a standard structure:

```
zenith/
|
├── LICENSE
├── README.md
├── .gitignore
├── pyproject.toml
|
├── src/                       # src folder
│    └── zenith/               # lib folder
│         ├── __init__.py
│         ├── module1.py
│         ├── ...
│         ├── modulex.py
│         └── data/            # run-time data
│ 
├── tests/                     # testing scripts
│    └── conftest.py
│    └── unit/                 # unit tests     
│    │    ├── test_module1.py
│    │    ├── ...
│    │    └── test_modulex.py
│    └── bcmk/                 # benchmarking tests
│    │    ├── test_bcmk1.py
│    │    ├── ...
│    │    └── test_bcmkx.py
│    └── data/                 # test-only data
│         ├── test_bcmk1_data1.csv
│         ├── ...
│         └── test_bcmkx_datax.tif
│ 
├── docs/                      # documentation resources
│    ├── update.py             # master script for updating doc files   
│    ├── docs1.md   
│    ├── ...
│    ├── docsx.rst
│    ├── index.rst  (sphinx)
│    ├── about.rst  (sphinx)
│    ├── usage.rst  (sphinx)
│    ├── api.rst    (sphinx)
│    ├── conf.py    (sphinx)
│    ├── make.bat   (sphinx)
│    ├── Makefile   (sphinx)
│    ├── figs/                 # figs-only data
│    │    ├── fig1.jpg
│    │    ├── fig1.svg
│    │    ├── ...
│    │    └── gifx.gif                  
│    ├── data/                 # doc-only data
│    |    ├── ref.bib
│    |    ├── ...
│    |    └── docs.csv
│    ├── generated/ (sphinx)
│    └── _build/    (sphinx)
|
├── examples/                  # learning resources 
│    ├── example_tutorial1.ipynb    
|    ├── ...
│    └── example_tutorialx.py            
|
└── scrips/                    # extra resources 
     ├── script_routine1.py    
     ├── ...
     └── script_routinex.bat    

```

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
