import streamlit as st
from sqlalchemy import create_engine,Column,String,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,declarative_base
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from datetime import datetime

db = create_engine("sqlite:///chaveirofinal.db")
Session = sessionmaker(bind=db)
session = Session()
Base = declarative_base()

#tabelas
class Usuario(Base):
    __tablename__ = "usuarios"
    id=Column("id",Integer,primary_key=True,autoincrement=True)
    nome = Column("nome",String)
    login = Column("login",String)
    senha = Column("senha",String)

    def __init__(self,nome,login,senha):
        self.nome = nome
        self.login=login
        self.senha=senha

class Venda(Base):
    __tablename__ = "vendas"
    id=Column("id",Integer,primary_key=True,autoincrement=True)
    tipo_pagamento=Column("tipo_pagamento",String)
    descricao = Column("descricao",String)
    data=Column("data",String)
    vendedor=Column("vendedor",ForeignKey("usuarios.id"))
    def __init__(self,tipo_pagamento,descricao,data,vendedor):
        self.tipo_pagamento=tipo_pagamento
        self.descricao=descricao
        self.data=data
        self.vendedor = vendedor

def cria_banco():
    print("cria banco")
    Base.metadata.create_all(bind=db)

def lista_vendas():
    #vendas=session.query(Venda).filter_by(vendedor="Joao")
    vendas=session.query(Venda).filter()
    #print(usuario.nome,usuario.id)
    #st.write(usuario.nome)
    #print(type(usuario))
    #for venda in vendas:
    #    print(venda.id,venda.descricao,venda.tipo_pagamento)
    st.title("Listagem de Vendas")
    #df = pd.read_sql_query(usuario,con=db)
    df_vendas = pd.read_sql(sql=vendas.statement,con=db).loc[:,["tipo_pagamento","descricao","data","vendedor"]].rename(columns={"tipo_pagamento":"Forma de Pagamento","descricao":"Descrição","data":"Data","vendedor":"Vendedor"})
    #st.dataframe(rows)
    
    st.dataframe(df_vendas,hide_index=True)
def lista_vendedores():
    st.title("Listagem de Vendedores")
    usuario=session.query(Usuario).filter()
    df = pd.read_sql(sql=usuario.statement,con=db).loc[:,["nome","login"]].rename(columns={"nome":"Nome","login":"Login"})
    st.dataframe(df,hide_index=True)

with open("config.yaml") as file:
    config = yaml.load(file,SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login()
#name, authentication_status, username = authenticator.login('Login', 'main')

#if authentication_status:
if st.session_state["authentication_status"]:
    print("login:",st.session_state["username"])
    #sidebar
    opcoes_menu = st.sidebar.selectbox("Selecione a opção:",("Insere Vendas","Lista Vendas","Lista Vendedores","Cadastra Vendedor"))

    if opcoes_menu ==  "Insere Vendas":
        st.title("Registro de Vendas")
        with st.form("form_vendas"):
            pagamento = st.selectbox("Forma de Pagamento:",("Dinheiro","Pix","Cartão"))
            descricao = st.text_area("Descrição:")
            submit = st.form_submit_button("Submete")
            #print(pagamento,descricao)
            if submit:
                #Insert
                #cria_banco()
                print("Insere")
                data_atual = datetime.now()
                vendas = Venda(tipo_pagamento=pagamento,descricao=descricao,data=data_atual,vendedor=st.session_state["username"])
                session.add(vendas)
                session.commit()
                st.write("Venda inserida com sucesso")
    elif opcoes_menu ==  "Cadastra Vendedor":
        st.title("Cadastro de Vendedor")
        with st.form("form_vendedor"):
            nome = st.text_input("Nome:")
            login = st.text_input("Login:")
            senha = st.text_input("Senha:")
            submit = st.form_submit_button("Submete")
            if submit:
                #Insert
                cria_banco()
                print("Insere Vendedor")
                vendedor = Usuario(nome=nome,login=login,senha=senha)
                session.add(vendedor)
                session.commit()
                st.write("##Vendedor inserido com sucesso")
    elif opcoes_menu == "Lista Vendas":
        lista_vendas()
    elif opcoes_menu == "Lista Vendedores":
        lista_vendedores()
    authenticator.logout(button_name='Logout',location='sidebar')
elif st.session_state["authentication_status"] is False:
    st.error("Usuaário ou Senha Inválidos")
elif st.session_state["authentication_status"] is None:
    st.warning("Por favor, utilize seu usuário e senha")
