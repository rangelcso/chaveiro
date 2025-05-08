import streamlit as st
from sqlalchemy import create_engine,Column,String,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,declarative_base

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

def vendas():
    pagamento = st.selectbox("Forma de Pagamento:",("A Vista","Pix","Cartão"))
    descricao = st.text_area("Descrição:")
    print(pagamento,descricao)
    st.button("Submete",on_click=cria_banco)

def lista_vendas():
    usuario=session.query(Usuario).filter_by(login="joao").first()
    #usuario=session.query(Usuario).all
    #print(usuario)
    print(usuario.nome,usuario.id)
    st.write(usuario.nome)

#sidebar
if st.sidebar.button("Insere Venda"):
    vendas()
#if st.sidebar.button("Lista Vendas",on_click=lista_vendas()):
if st.sidebar.button("Lista Vendas"):
    print("botao apertado")
    lista_vendas()
