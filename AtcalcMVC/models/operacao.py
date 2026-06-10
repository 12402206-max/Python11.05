from datetime import datetime
from . import db


class Operacao(db.Model):
    """Model — dados e acesso ao banco (tabela operacoes)."""

    __tablename__ = "operacoes"

    # Definição das colunas da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)
    num1 = db.Column(db.Float, nullable=False)
    num2 = db.Column(db.Float, nullable=True)  # Nullable=True pois a Raiz Quadrada não usa num2
    operacao = db.Column(db.String(10), nullable=False)
    etapas = db.Column(db.String(255), nullable=False)
    resultado = db.Column(db.String(50), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.now)

    @classmethod
    def salvar(cls, num1, num2, operacao, etapas, resultado):
        registro = cls(
            num1=num1,
            num2=num2,
            operacao=operacao,
            etapas=etapas,
            resultado=str(resultado),
        )
        
        # Comandos do SQLAlchemy para persistir os dados no banco de dados
        db.session.add(registro)
        db.session.commit()
        return registro

    @classmethod
    def listar_recentes(cls, limite=10):
        return (
            cls.query.order_by(cls.criado_em.desc()).limit(limite).all()
        )

    def __repr__(self):
        return f"<Operacao {self.id}: {self.etapas}>"