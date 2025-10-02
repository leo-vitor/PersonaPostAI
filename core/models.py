# core/models.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base 

Base = declarative_base()

class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    descricao = Column(Text)
    tom_de_voz = Column(Text)