from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base import ModeloBase
from .filme import Filme
from .ingresso import Ingresso
from .sala import Sala
from .sessao import Sessao

__all__ = ["db", "ModeloBase", "Filme", "Sala", "Sessao", "Ingresso"]
