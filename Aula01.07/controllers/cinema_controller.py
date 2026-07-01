from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for

from models import Filme, Sala, Sessao, db

cinema_bp = Blueprint("cinema", __name__, url_prefix="/cinema")


@cinema_bp.route("/")
def index():
    sessoes = Sessao.listar_com_detalhes()
    return render_template("cinema/lista_sessoes.html", sessoes=sessoes)


@cinema_bp.route("/sessao/cadastrar", methods=["GET", "POST"])
def cadastrar_sessao():
    filmes = Filme.listar()
    salas = Sala.listar()

    if request.method == "POST":
        sessao = Sessao(
            filme_id=request.form.get("filme_id", type=int),
            sala_id=request.form.get("sala_id", type=int),
            data_hora=datetime.strptime(request.form["data_hora"], "%Y-%m-%dT%H:%M"),
            preco=request.form.get("preco", type=float),
        )
        db.session.add(sessao)
        db.session.commit()
        return redirect(url_for("cinema.index"))

    return render_template("cinema/formulario_sessao.html", filmes=filmes, salas=salas)
