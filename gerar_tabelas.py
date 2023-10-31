import pandas as pd
import camelot


meses = {
    'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04', 'MAI': '05', 'JUN': '06',
    'JUL': '07', 'AGO': '08', 'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12'
}
def process_table(table):
    df = table.df.copy()
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)
    df = pd.melt(df, id_vars=df.columns[0], var_name='Mês', value_name='Fator')
    df.columns = ['Mês', 'Ano', 'Fator']
    df["Ano"] = df["Ano"].str.replace(" ",'', regex=False)
    df['Fator'] = pd.to_numeric(df['Fator'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False), errors='coerce')
    df = df.dropna().reset_index(drop=True)
    df['Mês'] = df['Mês'].map(meses)
    df['Ano-Mês'] = df['Ano'] + '-' + df['Mês']
    return df[["Ano-Mês","Fator"]].set_index('Ano-Mês')

url = 'https://www.tjsp.jus.br/Download/Tabelas/TabelaEmendaConstitucional113-2021.pdf'
tables = camelot.read_pdf(url, pages='all')
processed_tables = [process_table(table) for table in tables]
final_df = pd.concat(processed_tables)
final_df.to_json('tabela_de_atualizacao_ec113.json')
final_df.to_csv('tabela_de_atualizacao_ec113.csv')
