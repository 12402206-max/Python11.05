from . import db
from .base import ModeloBase


class Sala(ModeloBase):
    __tablename__ = "salas"

    numero = db.Column(db.Integer, nullable=False, unique=True)
    capacidade = db.Column(db.Integer, nullable=False)

    sessoes = db.relationship("Sessao", back_populates="sala")

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.numero).all()

    def para_dict(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "capacidade": self.capacidade,
            "data_criacao": str(self.data_criacao),
        }
