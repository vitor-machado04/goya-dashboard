import pandas as pd
from datetime import datetime

# Função para carregar os dados
def load_data():
    file_path = "data/book.csv"  # Caminho para o arquivo CSV
    df = pd.read_csv(file_path, encoding='ISO-8859-1', sep=";")
    
    # Limpeza de dados: substituindo ',' por '.' e convertendo para float
    df['Valor'] = df['Valor'].apply(lambda x: float(x.replace('.', '').replace(',', '.').strip()))  # Substitui '.' e ',' para formato numérico
    df['Data'] = pd.to_datetime(df['Mês'], format="%d/%m/%Y")
    
    return df

# Função para aplicar filtros
def apply_filters(df, nome, data_inicio, data_fim, documento):
    # Filtro de nome
    if nome:
        df = df[df['Nome'].str.contains(nome, case=False, na=False)]
    
    # Filtro de intervalo de datas (data_inicio até data_fim)
    if data_inicio and data_fim:
        df = df[(df['Data'] >= pd.to_datetime(data_inicio)) & (df['Data'] <= pd.to_datetime(data_fim))]
    
    # Filtro de documento
    if documento:
        df = df[df['Cpf/Cnpj'].str.contains(documento, case=False, na=False)]
    
    return df
