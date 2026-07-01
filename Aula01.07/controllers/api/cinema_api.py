# Versao "API" do cinema_controller.py.
# Mesmo Model, mesmo banco, mesma logica de consulta -- so muda a "casca":
# em vez de render_template(...) devolvemos jsonify(...).

from datetime import datetime

from flask import Blueprint, jsonify, request

from models import Filme, Ingresso, Sala, Sessao, db

# Blueprint separado com prefixo /api -- deixa claro que tudo aqui e JSON, nao HTML.
api_cinema_bp = Blueprint("api_cinema", __name__, url_prefix="/api")


# ------------------------------------------------------------------
# FILMES  (GET /api/filmes, GET /api/filmes/<id>, POST /api/filmes)
# ------------------------------------------------------------------
@api_cinema_bp.route("/filmes", methods=["GET"])
def listar_filmes():
    filmes = Filme.listar()
    return jsonify([f.para_dict() for f in filmes])


@api_cinema_bp.route("/filmes/<int:filme_id>", methods=["GET"])
def detalhe_filme(filme_id):
    filme = db.session.get(Filme, filme_id)
    if not filme:
        return jsonify({"erro": "Filme não encontrado"}), 404
    return jsonify(filme.para_dict())


@api_cinema_bp.route("/filmes", methods=["POST"])
def criar_filme():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie JSON no body (Content-Type: application/json)"}), 400

    try:
        filme = Filme(
            titulo=str(dados["titulo"]).strip(),
            duracao_min=int(dados["duracao_min"]),
            classificacao=str(dados["classificacao"]).strip(),
        )
    except (KeyError, ValueError, TypeError):
        return jsonify({"erro": "Campos obrigatórios: titulo, duracao_min, classificacao"}), 400

    if not filme.titulo:
        return jsonify({"erro": "Título não pode ser vazio"}), 400

    db.session.add(filme)
    db.session.commit()
    return jsonify(filme.para_dict()), 201


# ------------------------------------------------------------------
# SALAS  (GET /api/salas, GET /api/salas/<id>, POST /api/salas)
# ------------------------------------------------------------------
@api_cinema_bp.route("/salas", methods=["GET"])
def listar_salas():
    salas = Sala.listar()
    return jsonify([s.para_dict() for s in salas])


@api_cinema_bp.route("/salas/<int:sala_id>", methods=["GET"])
def detalhe_sala(sala_id):
    sala = db.session.get(Sala, sala_id)
    if not sala:
        return jsonify({"erro": "Sala não encontrada"}), 404
    return jsonify(sala.para_dict())


@api_cinema_bp.route("/salas", methods=["POST"])
def criar_sala():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie JSON no body (Content-Type: application/json)"}), 400

    try:
        sala = Sala(
            numero=int(dados["numero"]),
            capacidade=int(dados["capacidade"]),
        )
    except (KeyError, ValueError, TypeError):
        return jsonify({"erro": "Campos obrigatórios: numero, capacidade"}), 400

    db.session.add(sala)
    db.session.commit()
    return jsonify(sala.para_dict()), 201


# ------------------------------------------------------------------
# SESSOES (recurso principal: GET, GET/<id>, POST, PUT, DELETE + 404)
# ------------------------------------------------------------------
@api_cinema_bp.route("/sessoes", methods=["GET"])
def listar_sessoes():
    # Igualzinho ao cinema_controller.index(): Sessao.listar_com_detalhes()
    sessoes = Sessao.listar_com_detalhes()
    return jsonify([s.para_dict() for s in sessoes])


@api_cinema_bp.route("/sessoes/<int:sessao_id>", methods=["GET"])
def detalhe_sessao(sessao_id):
    sessao = db.session.get(Sessao, sessao_id)
    if not sessao:
        return jsonify({"erro": "Sessão não encontrada"}), 404
    return jsonify(sessao.para_dict())


@api_cinema_bp.route("/sessoes", methods=["POST"])
def criar_sessao():
    # Formulário HTML? request.form["filme_id"]
    # API REST? request.get_json() -- o body vem em JSON, não em <input name="...">
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie JSON no body (Content-Type: application/json)"}), 400

    try:
        filme_id = int(dados["filme_id"])
        sala_id = int(dados["sala_id"])
        data_hora = datetime.strptime(dados["data_hora"], "%Y-%m-%dT%H:%M")
        preco = float(dados["preco"])
    except (KeyError, ValueError, TypeError):
        return jsonify({
            "erro": "Campos obrigatórios: filme_id, sala_id, data_hora (AAAA-MM-DDTHH:MM), preco"
        }), 400

    if not db.session.get(Filme, filme_id):
        return jsonify({"erro": "Filme não encontrado"}), 404
    if not db.session.get(Sala, sala_id):
        return jsonify({"erro": "Sala não encontrada"}), 404

    sessao = Sessao(filme_id=filme_id, sala_id=sala_id, data_hora=data_hora, preco=preco)
    db.session.add(sessao)
    db.session.commit()

    # 201 = "criei um recurso novo". Em HTML redirecionaria; aqui devolve o objeto criado.
    return jsonify(sessao.para_dict()), 201


@api_cinema_bp.route("/sessoes/<int:sessao_id>", methods=["PUT"])
def atualizar_sessao(sessao_id):
    sessao = db.session.get(Sessao, sessao_id)
    if not sessao:
        return jsonify({"erro": "Sessão não encontrada"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie JSON no body"}), 400

    # Atualiza só o que veio no JSON -- o resto fica como estava.
    try:
        if "filme_id" in dados:
            novo_filme_id = int(dados["filme_id"])
            if not db.session.get(Filme, novo_filme_id):
                return jsonify({"erro": "Filme não encontrado"}), 404
            sessao.filme_id = novo_filme_id
        if "sala_id" in dados:
            nova_sala_id = int(dados["sala_id"])
            if not db.session.get(Sala, nova_sala_id):
                return jsonify({"erro": "Sala não encontrada"}), 404
            sessao.sala_id = nova_sala_id
        if "data_hora" in dados:
            sessao.data_hora = datetime.strptime(dados["data_hora"], "%Y-%m-%dT%H:%M")
        if "preco" in dados:
            sessao.preco = float(dados["preco"])
    except (ValueError, TypeError):
        return jsonify({"erro": "Dados inválidos"}), 400

    db.session.commit()
    return jsonify(sessao.para_dict())


@api_cinema_bp.route("/sessoes/<int:sessao_id>", methods=["DELETE"])
def excluir_sessao(sessao_id):
    sessao = db.session.get(Sessao, sessao_id)
    if not sessao:
        return jsonify({"erro": "Sessão não encontrada"}), 404

    db.session.delete(sessao)
    db.session.commit()

    # 204 = deu certo, mas sem corpo na resposta.
    return "", 204


# ------------------------------------------------------------------
# INGRESSOS (GET, GET/<id>, POST)
# ------------------------------------------------------------------
@api_cinema_bp.route("/ingressos", methods=["GET"])
def listar_ingressos():
    ingressos = Ingresso.listar()
    return jsonify([i.para_dict() for i in ingressos])


@api_cinema_bp.route("/ingressos/<int:ingresso_id>", methods=["GET"])
def detalhe_ingresso(ingresso_id):
    ingresso = db.session.get(Ingresso, ingresso_id)
    if not ingresso:
        return jsonify({"erro": "Ingresso não encontrado"}), 404
    return jsonify(ingresso.para_dict())


@api_cinema_bp.route("/ingressos", methods=["POST"])
def criar_ingresso():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie JSON no body (Content-Type: application/json)"}), 400

    try:
        sessao_id = int(dados["sessao_id"])
        assento = str(dados["assento"]).strip()
        nome_comprador = str(dados["nome_comprador"]).strip()
    except (KeyError, ValueError, TypeError):
        return jsonify({"erro": "Campos obrigatórios: sessao_id, assento, nome_comprador"}), 400

    if not db.session.get(Sessao, sessao_id):
        return jsonify({"erro": "Sessão não encontrada"}), 404
    if not assento or not nome_comprador:
        return jsonify({"erro": "assento e nome_comprador não podem ser vazios"}), 400

    ingresso = Ingresso(sessao_id=sessao_id, assento=assento, nome_comprador=nome_comprador)
    db.session.add(ingresso)
    db.session.commit()
    return jsonify(ingresso.para_dict()), 201
