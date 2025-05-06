import streamlit as st
from sqlalchemy import create_engine,Column,String,Integer,ForeignKey
from sqlalchemy.orm import sessionmaker,declarative_base

db = create_engine("sqlite:///chaveirofinal.db")
Session = sessionmaker(bind=db)
session = Session()
Base = declarative_base()

def cria_banco():
    print("cria banco")
    Base.metadata.create_all(bind=db)

pagamento = st.selectbox("Forma de Pagamento:",("A Vista","Pix","Cartão"))
descricao = st.text_area("Descrição:")
st.button("Submete",on_click=cria_banco)

print(pagamento,descricao)