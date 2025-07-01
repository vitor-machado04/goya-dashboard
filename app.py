import streamlit as st
import pandas as pd
import os
from utils import load_data, apply_filters
from datetime import datetime
from io import StringIO

st.set_page_config(
    page_title="Dashboard de Pagamentos",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

logo_path = "./goya.png"
st.sidebar.image(logo_path, width=200)

st.markdown(
    """
    <style>
    /* Definir o fundo branco e texto preto para a aplicação */
    .reportview-container {
        background-color: white;  /* Cor do fundo branco para toda a aplicação */
        color: black;  /* Texto preto no conteúdo */
    }

    /* Estilizar o fundo da barra lateral (sidebar) */
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf, #2e7bcf);  /* Fundo azul na sidebar */
        color: white;  /* Texto branco na sidebar */
    }

    .st-emotion-cache-jx6q2s {
        background-color: #324280 !important;  /* Fundo azul para a barra lateral */
        color: white !important;  /* Texto branco na barra lateral */
    }

    /* Ajustar o texto na área de conteúdo (dados e tabelas) */
    .block-container {
        background-color: white;  /* Fundo branco no conteúdo */
        color: black;  /* Texto preto no conteúdo */
    }

    /* Garantir que a tabela tenha fundo branco e texto preto */
    .stDataFrame table, .stDataFrame th, .stDataFrame td {
        color: black !important;  /* Texto preto dentro da tabela */
        background-color: white !important;  /* Fundo branco */
    }

    /* Estilo para o input na barra lateral (sidebar) */
    .sidebar .stTextInput input {
        color: white !important;  /* Texto branco dentro dos inputs na sidebar */
    }

    /* Estilo para outros inputs também */
    input, .stNumberInput input {
        color: black !important;  /* Texto preto dentro dos inputs */
    }

    /* Garantir que o fundo da aplicação geral seja branco */
    .stApp {
        background-color: white !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

def load_data():
    file_path = "./data/book.csv"
    
    # Verificar se o arquivo existe no caminho local
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='ISO-8859-1', sep=";")
        st.success(f"Arquivo {file_path} carregado com sucesso!")
    else:
        st.warning(f"Arquivo {file_path} não encontrado!")
        
        # Permitir ao usuário fazer o upload de um arquivo CSV
        uploaded_file = st.file_uploader("Faça o upload de um arquivo CSV", type="csv")
        if uploaded_file is not None:
            # Carregar o arquivo CSV enviado pelo usuário
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1', sep=";")
            st.success("Arquivo enviado com sucesso!")
        else:
            st.error("Por favor, faça o upload de um arquivo CSV.")
            return None

    # Processamento de dados
    df['Valor'] = df['Valor'].apply(lambda x: float(x.replace('.', '').replace(',', '.').strip()))
    df['Data'] = pd.to_datetime(df['Mês'], format="%d/%m/%Y")
    
    return df

def apply_filters(df, nome, data_inicio, data_fim, documento):
    if nome:
        df = df[df['Nome'].str.contains(nome, case=False, na=False)]

    if data_inicio and data_fim:
        df = df[(df['Data'] >= pd.to_datetime(data_inicio)) & (df['Data'] <= pd.to_datetime(data_fim))]

    if documento:
        df = df[df['Cpf/Cnpj'].str.contains(documento, case=False, na=False)]
    
    return df

df = load_data()

if df is not None:  # Verifique se os dados foram carregados corretamente
    current_year = datetime.now().year
    start_date = datetime(current_year, 1, 1)

    st.title("🦷 Dashboard de Pagamentos")

    st.sidebar.header("Filtros")

    nome = st.sidebar.text_input("Filtrar por Nome")

    data_inicio = st.sidebar.date_input("Data Início", value=start_date)
    data_fim = st.sidebar.date_input("Data Fim", value=datetime.now())

    documento = st.sidebar.text_input("Filtrar por CPF/CNPJ")

    filtered_df = apply_filters(df, nome, data_inicio, data_fim, documento)

    st.write("Dados Filtrados:")
    st.dataframe(filtered_df)

    st.subheader("Melhores Meses - Total Pago")
    monthly_payment = filtered_df.groupby(filtered_df['Data'].dt.month)['Valor'].sum().sort_values(ascending=False)
    monthly_payment.index = monthly_payment.index.map({1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'})
    st.bar_chart(monthly_payment)

    st.subheader("Clientes que mais fazem atendimento")
    top_clients = filtered_df.groupby('Nome')['Valor'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_clients)

    st.subheader("Valor Total")
    total_value = filtered_df['Valor'].sum()
    st.write(f"R$ {total_value:,.2f}")
