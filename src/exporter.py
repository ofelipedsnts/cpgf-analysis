import pandas as pd
from pathlib import Path

def export_data_by_orgao(df:pd.DataFrame):
    df = (
    df.groupby(by=["nome_orgao_superior"], as_index=False)
        .agg({
            "codigo_orgao_superior": ["count"],
            "valor_transacao": ["sum", "mean"]
        })
    )

    df.columns = ["Orgão Superior", "Qtd. de Transações", "Gastos Totais", "Média de gastos"]

    df.sort_values(by="Gastos Totais", ascending=False)

    output_path = Path().resolve().parent / "data" / "processed" / "total-gastos-por-orgao.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")

    return print(f"Arquivo exportado com sucesso {output_path}")