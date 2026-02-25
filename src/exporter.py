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
    

def export_saques_dataframe(df:pd.DataFrame):
    saques = (df["transacao"] == "SAQUE - INT$ - APRES") | (df["transacao"] == "SAQUE CASH/ATM BB")
    df = df[saques]

    output_path = Path().resolve().parent / "data" / "processed" / "transacoes_de_saque.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")

    return print(f"[export_saques]: Arquivo exportado com sucesso {output_path}")


def export_data_by_servidor(df:pd.DataFrame):
    new_df = (
    df.groupby(by=["nome_portador"], as_index=False)
        .agg({
            "valor_transacao": ["sum", "mean", "count"],
        })
    )

    new_df.columns = ["Nome do servidor", "Gastos totais", "Valor médio por transação", "Quantidade de transações"]

    new_df["Gastos totais"] = new_df["Gastos totais"].round(2)
    new_df["Valor médio por transação"] = new_df["Valor médio por transação"].round(2) 

    output_path = Path().resolve().parent / "data" / "processed" / "resumo_servidores.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")

    return print(f"[export_data_by_servidor]: Arquivo exportado com sucesso {output_path}")
