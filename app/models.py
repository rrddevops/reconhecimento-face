from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from .database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, unique=True, index=True, nullable=False)
    imagem_base64 = Column(String, nullable=False)
    face_encoding = Column(JSONB, nullable=False) 