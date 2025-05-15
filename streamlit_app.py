import streamlit as st
from sqlalchemy import create_engine,Column,String,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,declarative_base
import pandas as pd
#from PIL import Image
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
#from yaml import SafeLoader


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
    vendedor=Column("vendedor",ForeignKey("usuarios.id"))
    def __init__(self,tipo_pagamento,descricao,vendedor):
        self.tipo_pagamento=tipo_pagamento
        self.descricao=descricao
        self.vendedor = vendedor


def cria_banco():
    print("cria banco")
    Base.metadata.create_all(bind=db)


def lista_vendas():
    usuario=session.query(Usuario).filter_by(login="joao")
    #vendas=session.query(Venda).all()
    vendas=session.query(Venda).filter_by(vendedor="Joao")
    print("Usuario:",usuario)
    #print(usuario.nome,usuario.id)
    #st.write(usuario.nome)
    #print(type(usuario))
    for venda in vendas:
        print(venda.id,venda.descricao,venda.tipo_pagamento)
    

    #df = pd.read_sql_query(usuario,con=db)
    df = pd.read_sql(sql=usuario.statement,con=db)
    df_vendas = pd.read_sql(sql=vendas.statement,con=db)
    #df = pd.DataFrame(vendas)

    #st.write(df)
    #st.dataframe(rows)
    
    st.dataframe(df)
    st.dataframe(df_vendas)

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
    #sidebar
    opcoes_menu = st.sidebar.selectbox("Selecione a opção:",("Insere Vendas","Lista Vendas"))

    if opcoes_menu ==  "Insere Vendas":
        with st.form("form_vendas"):
            pagamento = st.selectbox("Forma de Pagamento:",("A Vista","Pix","Cartão"))
            descricao = st.text_area("Descrição:")
            submit = st.form_submit_button("Submete")
            print(pagamento,descricao)
            if submit:
                #Insert
                print("Insere")
                vendas = Venda(tipo_pagamento=pagamento,descricao=descricao,vendedor="Joao")
                session.add(vendas)
                session.commit()
                st.write("##Inserido com sucesso")
    elif opcoes_menu == "Lista Vendas":
        print("botao apertado")
        lista_vendas()
    authenticator.logout(button_name='Logout',location='sidebar')
elif st.session_state["authentication_status"] is False:
    st.error("Usuaário ou Senha Inválidos")
elif st.session_state["authentication_status"] is None:
    st.warning("Por favor, utilize seu usuário e senha")
