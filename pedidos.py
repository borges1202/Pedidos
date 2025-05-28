import streamlit as st
import pandas as pd
import pyshorteners
import os

st.set_page_config(layout="wide")

# Função para carregar dados salvos em Excel
def carregar_dados():
    if os.path.exists("pedidos.xlsx"):
        return pd.read_excel("pedidos.xlsx").to_dict(orient='list')
    return {
        'CODIGO': [],
        'QUANTIDADE': [],
        'OS': [],
        'DESCRIÇÃO': [],
        'url': []
    }

# Função para salvar os dados no arquivo Excel
def salvar_dados(dados):
    df = pd.DataFrame(dados)
    df.to_excel("pedidos.xlsx", index=False)

# Carregar os dados no início do aplicativo
if 'itens_novos' not in st.session_state:
    st.session_state.itens_novos = carregar_dados()

# Configuração do site
st.title('Gerenciador de Pedidos Eletrogoias')
with st.form(key='pedido_form', clear_on_submit=True):
    codigo = st.text_input('Codigo do componente', placeholder='...')
    quantidade = st.number_input('Quantidade', min_value=1, max_value=100, value=1)
    os = st.text_input('Numero da OS', placeholder='...')
    desc = st.text_input('Descrição', placeholder='...')
    url = st.text_input('url de compra', placeholder='...')

    enviar = st.form_submit_button(label='Enviar Pedido')
    if enviar:
        if not url:
            st.error("Por favor, insira uma URL.")
        else:
            # Tenta encurtar a URL usando pyshorteners
            try:
                if url:
                    type_tiny = pyshorteners.Shortener()
                    url_Curta = type_tiny.tinyurl.short(url)
            except Exception as e:
                    url_Curta = url # Se falhar, mantém a URL original


            # Adiciona os dados ao dicionário
            st.session_state.itens_novos['CODIGO'].append(codigo)
            st.session_state.itens_novos['QUANTIDADE'].append(quantidade)
            st.session_state.itens_novos['OS'].append(os)
            st.session_state.itens_novos['DESCRIÇÃO'].append(desc)
            st.session_state.itens_novos['url'].append(url_Curta)
            # Salvar os dados no arquivo Excel
            salvar_dados(st.session_state.itens_novos)
            st.success('Dados recebidos com sucesso!')
        

df = pd.DataFrame(st.session_state.itens_novos)
# Sidebar para Exibir os dados
st.sidebar.title('Planilha de Pedidos')
st.sidebar.header('Acompanhamento dos pedidos')
st.sidebar.dataframe(df)

if 'mostrar_opcoes' not in st.session_state:
    st.session_state.mostrar_opcoes = False

# Botão para mostrar o selectbox
if st.sidebar.button("editar tabela"):
    st.session_state.mostrar_opcoes = not st.session_state.mostrar_opcoes  # Alternar o estado

if st.session_state.mostrar_opcoes:
    box = st.sidebar.selectbox(
        'Selecione uma opção para editar',
        (st.session_state.itens_novos['CODIGO'])
    )

    if box:
        # Exibir os dados do pedido selecionado
        pedido_selecionado = st.session_state.itens_novos['CODIGO'].index(box)
        st.sidebar.write('Pedido Selecionado:', st.session_state.itens_novos['CODIGO'][pedido_selecionado])
        codigo_edicao = st.sidebar.text_input('Código:', st.session_state.itens_novos['CODIGO'][pedido_selecionado])
        quantidade_edicao = st.sidebar.number_input('Quantidade:', st.session_state.itens_novos['QUANTIDADE'][pedido_selecionado])
        os_edicao = st.sidebar.text_input('OS:', st.session_state.itens_novos['OS'][pedido_selecionado])
        desc_edicao = st.sidebar.text_input('Descrição:', st.session_state.itens_novos['DESCRIÇÃO'][pedido_selecionado])
        url_edicao = st.sidebar.text_input('URL:', st.session_state.itens_novos['url'][pedido_selecionado])

        try:
            if url_edicao:
                type_tiny_edicao = pyshorteners.Shortener()
                url_Curta_edicao = type_tiny_edicao.tinyurl.short(url_edicao)
        except:
            url_Curta_edicao = url_edicao  # Se falhar, mantém a URL original
        
        if st.sidebar.button('Salvar Edição'): # Botão para salvar a edição
            df.loc[pedido_selecionado, 'CODIGO'] = codigo_edicao
            df.loc[pedido_selecionado, 'QUANTIDADE'] = quantidade_edicao
            df.loc[pedido_selecionado, 'OS'] = os_edicao
            df.loc[pedido_selecionado, 'DESCRIÇÃO'] = desc_edicao
            df.loc[pedido_selecionado, 'url'] = url_Curta_edicao
            st.sidebar.write('Pedido atualizado com sucesso!')

            # Atualizar os dados no dicionário
            st.session_state.itens_novos['CODIGO'][pedido_selecionado] = codigo_edicao
            st.session_state.itens_novos['QUANTIDADE'][pedido_selecionado] = quantidade_edicao
            st.session_state.itens_novos['OS'][pedido_selecionado] = os_edicao
            st.session_state.itens_novos['DESCRIÇÃO'][pedido_selecionado] = desc_edicao
            st.session_state.itens_novos['url'][pedido_selecionado] = url_Curta_edicao
            
            # Salvar os dados atualizados no arquivo Excel
            salvar_dados(st.session_state.itens_novos)
            st.rerun()  # Atualiza a página para refletir as mudanças
        if st.sidebar.button('Excluir Pedido'):
            df = df.drop(pedido_selecionado).reset_index(drop=True)
            st.sidebar.write('Pedido excluído com sucesso!')

            # Atualizar os dados no dicionário
            for key in st.session_state.itens_novos.keys():
                st.session_state.itens_novos[key].pop(pedido_selecionado)

            # Salvar os dados atualizados no arquivo Excel
            salvar_dados(st.session_state.itens_novos)
            st.rerun() 