from pathlib import Path
import pandas as pd

# Raiz do projeto: dois níveis acima de src/loader.py
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_DATA_DIR = _PROJECT_ROOT / "data" / "raw" / "cpfg"


def load_data(data_dir: Path | str = _DEFAULT_DATA_DIR) -> pd.DataFrame:
    data_dir = Path(data_dir)

    if not data_dir.exists():
        raise FileNotFoundError(f"Diretório não encontrado: {data_dir}")

    csv_files = sorted(data_dir.glob("*.csv"))

    if not csv_files:
        raise ValueError(f"Nenhum arquivo CSV encontrado em: {data_dir}")

    dataframes = [
        pd.read_csv(file, sep=";", encoding="latin-1")
        for file in csv_files
    ]

    df = pd.concat(dataframes, ignore_index=True)

    return df
