import math
from flask import Blueprint, render_template, request
from models import Operacao

# Define o Blueprint com o nome esperado pelo url_for do HTML
calculadora_bp = Blueprint("calculadora", __name__)


@calculadora_bp.route("/", methods=["GET", "POST"])
def index():
    etapas = None
    resultados = None

    if request.method == "POST":
        try:
            # Captura os dados enviados pelo formulário HTML
            num1 = float(request.form.get("num1"))
            operacao = request.form.get("operacao")

            # Tratamento especial para a Raiz Quadrada (que não usa o num2)
            if operacao == "sqrt":
                num2 = None
                if num1 < 0:
                    resultados = "Erro: Raiz de número negativo"
                    etapas = f"√({num1})"
                else:
                    res = math.sqrt(num1)
                    # Formata para inteiro se não tiver casas decimais
                    resultados = (
                        int(res) if res.is_integer() else round(res, 4)
                    )
                    etapas = f"√({num1})"
            else:
                # Operações normais que usam os dois números
                num2 = float(request.form.get("num2"))

                if operacao == "+":
                    res = num1 + num2
                    etapas = f"{num1} + {num2}"
                elif operacao == "-":
                    res = num1 - num2
                    etapas = f"{num1} - {num2}"
                elif operacao == "*":
                    res = num1 * num2
                    etapas = f"{num1} × {num2}"
                elif operacao == "/":
                    if num2 == 0:
                        resultados = "Erro: Divisão por zero"
                        etapas = f"{num1} ÷ {num2}"
                    else:
                        res = num1 / num2
                        etapas = f"{num1} ÷ {num2}"
                elif operacao == "**":
                    res = num1**num2
                    etapas = f"{num1} ^ {num2}"

                # Se não houve erro de divisão por zero, define o resultado
                if resultados is None:
                    resultados = (
                        int(res) if res.is_integer() else round(res, 4)
                    )

            # Só salva no banco de dados se o cálculo foi bem-sucedido (sem erros)
            if "Erro" not in str(resultados):
                Operacao.salvar(
                    num1=num1,
                    num2=num2,
                    operacao=operacao,
                    etapas=etapas,
                    resultado=resultados,
                )

        except Exception as e:
            resultados = f"Erro no processamento: {e}"
            etapas = "Erro"

    # Busca a lista atualizada de operações do banco para exibir no histórico
    historico = Operacao.listar_recentes()

    # Renderiza a página passando as variáveis que o Jinja espera no HTML
    return render_template(
        "calculadora.html",
        etapas=etapas,
        resultados=resultados,
        historico=historico,
    )