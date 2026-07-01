from . import db
from .base import ModeloBase


class Ingresso(ModeloBase):
    __tablename__ = "ingressos"

    sessao_id = db.Column(db.Integer, db.ForeignKey("sessoes.id"), nullable=False)
    assento = db.Column(db.String(10), nullable=False)
    nome_comprador = db.Column(db.String(120), nullable=False)

    sessao = db.relationship("Sessao", back_populates="ingressos")

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.id.desc()).all()

    def para_dict(self):
        return {
            "id": self.id,
            "sessao_id": self.sessao_id,
            "assento": self.assento,
            "nome_comprador": self.nome_comprador,
            "data_criacao": str(self.data_criacao),
        }
