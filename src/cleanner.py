import pandas as pd

def normalize_columns(df: pd.DataFrame):
    renamed_columns = {
        "CÓDIGO ÓRGÃO SUPERIOR": "codigo_orgao_superior",
        "NOME ÓRGÃO SUPERIOR": "nome_orgao_superior",
        "CÓDIGO ÓRGÃO": "codigo_orgao",
        "NOME ÓRGÃO": "nome_orgao",
        "CÓDIGO UNIDADE GESTORA": "codigo_unidade_gestora",
        "NOME UNIDADE GESTORA": "nome_unidade_gestora",
        "ANO EXTRATO": "ano_extrato",
        "MÊS EXTRATO": "mes_extrato",
        "CPF PORTADOR": "cpf_portador",
        "NOME PORTADOR": "nome_portador",
        "CNPJ OU CPF FAVORECIDO": "cnpj_ou_cpf_favorecido",
        "NOME FAVORECIDO": "nome_favorecido",
        "TRANSAÇÃO": "transacao",
        "DATA TRANSAÇÃO": "data_transacao",
        "VALOR TRANSAÇÃO": "valor_transacao",
    }
    
    normalized_df = df.rename(columns=renamed_columns)
    return normalized_df

def transform_str_to_float(df: pd.DataFrame) -> pd.DataFrame:
    transformed_df = df.copy()
    transformed_df["valor_transacao"] = pd.to_numeric(
        transformed_df["valor_transacao"].str.replace(",", ".", regex=False),
        errors="coerce",
    )
    return transformed_df

def transform_to_datetime(df: pd.DataFrame):
    transformed_df = df.copy()
    transformed_df["data_transacao"] = pd.to_datetime(
        transformed_df["data_transacao"],
        format="%d/%m/%Y",
        errors="coerce"
    ).dt.date

    return transformed_df
