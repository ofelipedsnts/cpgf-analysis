# AGENTS.md

Guidelines for agentic coding agents working in this repository.

---

## Project Overview

Analysis of CPGF (Cartão de Pagamento do Governo Federal) transaction data from 2025.
The pipeline loads raw monthly CSVs, cleans and normalizes the data, and exports
processed outputs for reporting.

**Stack:** Python 3.13, pandas, JupyterLab, Streamlit (planned).

---

## Project Structure

```
cpgf-analysis/
├── data/
│   ├── raw/cpfg/          # Raw monthly CSVs (not committed)
│   └── processed/         # Exported outputs (not committed)
├── notebooks/             # Jupyter notebooks (numbered execution order)
│   ├── 01-exploration.ipynb
│   ├── 02-transformation.ipynb
│   ├── 03-export-by-orgao.ipynb
│   ├── 04-export-saques.ipynb
│   └── 05-servidor-stats.ipynb
└── src/
    ├── loader.py          # CSV ingestion
    ├── cleanner.py        # Data cleaning/transformation (note: filename typo kept for compatibility)
    ├── exporter.py        # CSV export helpers
    └── utils.py           # Shared utilities (currently empty)
```

---

## Environment Setup

The project uses a virtual environment at `.venv/`. Always use it:

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Python version:** 3.13.9

---

## Running the Project

There is no build system or CLI entrypoint. The project is driven by notebooks.

```bash
# Start JupyterLab
.venv/bin/jupyter lab

# Start classic Jupyter Notebook
.venv/bin/jupyter notebook
```

Execute notebooks in order: `01` → `02` → `03` → `04` → `05`.

---

## Linting and Formatting

No linting or formatting tools are currently configured. When adding them, prefer:

- **Formatter:** `ruff format` or `black`
- **Linter:** `ruff check`
- **Type checker:** `pyright` or `mypy`

Until configured, follow the conventions described below manually.

---

## Testing

No test suite exists. There is no `pytest` or any test framework installed.

When adding tests:
```bash
# Run all tests
.venv/bin/pytest

# Run a single test file
.venv/bin/pytest tests/test_loader.py

# Run a single test function
.venv/bin/pytest tests/test_loader.py::test_load_data_returns_dataframe
```

Place test files under `tests/` with the pattern `test_<module>.py`.

---

## Code Style Guidelines

### Language

- **Code** (variable names, function names, module names): English or Portuguese snake_case
- **Error messages and comments**: Portuguese (existing convention — keep consistent)
- **Docstrings**: Portuguese preferred, consistent with the domain language

### Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Functions | `snake_case` | `load_data`, `normalize_columns` |
| Variables | `snake_case` | `csv_files`, `renamed_columns` |
| Module-level private constants | `_SCREAMING_SNAKE_CASE` | `_PROJECT_ROOT`, `_DEFAULT_DATA_DIR` |
| DataFrame column names | `snake_case`, no accents | `codigo_orgao_superior`, `valor_transacao` |
| Files/modules | `snake_case` | `loader.py`, `cleanner.py` |

### Imports

- Use **absolute imports** only — no relative imports (`from .loader import ...` is discouraged)
- Follow PEP 8 import ordering:
  1. Standard library (`pathlib`, `os`, etc.)
  2. Third-party (`pandas`, `numpy`, etc.)
  3. Local (`from src.loader import ...`)
- Separate each group with a blank line

```python
# Good
from pathlib import Path

import pandas as pd

from src.loader import load_data
```

- In notebooks, always add the project root to `sys.path` in the first cell:

```python
import sys
from pathlib import Path

sys.path.append(str(Path().resolve().parent))
```

### Type Annotations

- Annotate **all** function parameters and return types
- Use Python 3.10+ union syntax: `Path | str` instead of `Union[Path, str]`
- Do not use `Optional[X]` — prefer `X | None`

```python
# Good
def load_data(data_dir: Path | str = _DEFAULT_DATA_DIR) -> pd.DataFrame:
    ...

# Bad — missing return type
def normalize_columns(df: pd.DataFrame):
    ...
```

### Docstrings

Use Google-style docstrings in Portuguese for all public functions:

```python
def load_data(data_dir: Path | str = _DEFAULT_DATA_DIR) -> pd.DataFrame:
    """Lê todos os arquivos CSV do diretório e retorna um único DataFrame.

    Args:
        data_dir: Caminho para o diretório contendo os CSVs.

    Returns:
        DataFrame concatenado com os dados de todos os arquivos CSV.

    Raises:
        FileNotFoundError: Se o diretório não existir.
        ValueError: Se nenhum arquivo CSV for encontrado.
    """
```

### Error Handling

- Use **guard clauses** at the top of functions for precondition checks
- Raise built-in exceptions with descriptive Portuguese messages
- Prefer `errors="coerce"` in pandas operations to avoid pipeline crashes on bad data

```python
# Good
if not data_dir.exists():
    raise FileNotFoundError(f"Diretório não encontrado: {data_dir}")

if not csv_files:
    raise ValueError(f"Nenhum arquivo CSV encontrado em: {data_dir}")
```

- Avoid bare `except:` clauses
- Do not use `return print(...)` — `print` returns `None`; use `print(...)` then `return`

### Functions

- Each `src/` function should do one thing and return a value — avoid side effects where possible
- Transformation functions must receive a DataFrame and return a new DataFrame (do not mutate in place):

```python
# Good
def transform_str_to_float(df: pd.DataFrame) -> pd.DataFrame:
    transformed_df = df.copy()
    transformed_df["valor_transacao"] = pd.to_numeric(...)
    return transformed_df

# Bad — mutates the original
def transform_str_to_float(df: pd.DataFrame) -> pd.DataFrame:
    df["valor_transacao"] = pd.to_numeric(...)
    return df
```

### CSV Conventions

- Raw files: `sep=";"`, `encoding="latin-1"` (Windows-1252 compatible)
- Processed files: `sep=","`, `encoding="utf-8"`, `index=False`
- Paths resolved via `pathlib.Path` relative to `_PROJECT_ROOT`, never hardcoded strings

---

## Data Pipeline Reference

```
raw CSVs (latin-1, sep=";")
  └─ load_data()              → raw DataFrame
       └─ normalize_columns() → snake_case column names
            └─ transform_to_datetime() → data_transacao as datetime
                 └─ transform_str_to_float() → valor_transacao as float64
                      └─ to_csv(..., encoding="utf-8") → data/processed/
```

### Column Name Mapping

| Original | Normalized |
|---|---|
| `CÓDIGO ÓRGÃO SUPERIOR` | `codigo_orgao_superior` |
| `NOME ÓRGÃO SUPERIOR` | `nome_orgao_superior` |
| `CÓDIGO ÓRGÃO` | `codigo_orgao` |
| `NOME ÓRGÃO` | `nome_orgao` |
| `CÓDIGO UNIDADE GESTORA` | `codigo_unidade_gestora` |
| `NOME UNIDADE GESTORA` | `nome_unidade_gestora` |
| `ANO EXTRATO` | `ano_extrato` |
| `MÊS EXTRATO` | `mes_extrato` |
| `CPF PORTADOR` | `cpf_portador` |
| `NOME PORTADOR` | `nome_portador` |
| `CNPJ OU CPF FAVORECIDO` | `cnpj_ou_cpf_favorecido` |
| `NOME FAVORECIDO` | `nome_favorecido` |
| `TRANSAÇÃO` | `transacao` |
| `DATA TRANSAÇÃO` | `data_transacao` |
| `VALOR TRANSAÇÃO` | `valor_transacao` |
