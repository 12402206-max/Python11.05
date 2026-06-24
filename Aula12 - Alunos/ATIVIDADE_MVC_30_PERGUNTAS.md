# Atividade Aula 12 — Model, Controller e View (StreamFlix)

**Disciplina:** Python / Flask  
**Profª:** Janaína Duarte  
**Projeto:** `flask/Aula12/`  
**Objetivo:** Explorar o código, localizar arquivos e explicar o que cada camada faz.

---

## Como responder

1. Abra a pasta `flask/Aula12/` no editor ou GitHub.
2. Navegue pelas pastas `models/`, `controllers/` e `views/`.
3. Rode o site (`python app.py`) quando a pergunta pedir para testar no navegador.
4. Responda com **caminho do arquivo** + **explicação em suas palavras**.
**Identificação**

- Nome: Gabriel Almeida Barbosa
- Turma: 3B1

---

## Bloco A — Model (perguntas 1 a 10)

**1.** Em qual pasta ficam as classes que representam tabelas do banco SQLite? Cite o caminho.
R: Fica em `models/`. E o caminho é `base.py`, `filme_favorito.py` e `historico_busca.py`.

**2.** Qual é o nome do arquivo de banco criado quando o app roda? Em qual arquivo Python essa configuração está?
R: É o `streamflix.db`. A configuração está no `app.py`.

**3.** Quais classes Model existem no projeto (nome das classes)? Em quais arquivos `.py` cada uma está?
R: 3 classes: `ModeloBase` (em `models/base.py`), `FilmeFavorito` (em `models/filme_favorito.py`) e `HistoricoBusca` (em `models/historico_busca.py`).

**4.** De qual superclasse `FilmeFavorito` e `HistoricoBusca` herdam? O que elas ganham automaticamente por herança (cite 3 campos)?
R: As duas herdam de `ModeloBase`. Ai elas ganham `id`, `data_criacao` e `data_atualizacao`.

**5.** Qual é o `__tablename__` da tabela de favoritos? Por que usamos `__tablename__` em vez de só o nome da classe?
R: É `filmes_favoritos`. Não Lembro  o porquê usar só `__tablename__`

**6.** No model `FilmeFavorito`, qual coluna guarda o id do filme vindo da API TMDB? Ela tem alguma restrição especial (`unique`, `nullable`)?
R: É a coluna `tmdb_id`. Sim, ela tem `nullable=False` e `unique=True` 

**7.** Abra `models/filme_favorito.py`. O que o método `@classmethod adicionar` faz passo a passo? O que acontece se o filme já existir nos favoritos?
R:  O método `adicionar`: primeiro chama `buscar_por_tmdb` para ver se o filme já está salvo, se não existir, cria um novo objeto `FilmeFavorito`, adiciona na sessão e salva no banco . se caso o filme já existir nos favoritos, ele simplesmente não é duplicado.

**8.** Onde está o método que lista as últimas 8 buscas? Qual é o nome da classe e do método?
R: Está em `models/historico_busca.py`, na classe `HistoricoBusca`, método `ultimas` 

**9.** O model grava dados da API TMDB inteira ou só alguns campos espelhados? Cite 4 campos salvos em `FilmeFavorito`.
R: Não sei

**10.** Em `models/__init__.py`, o que é exportado além de `db`? Por que o controller importa `from models import FilmeFavorito` em vez de importar o arquivo inteiro da pasta?
R: Além de `db`, é exportado o `ModeloBase`, `FilmeFavorito` e `HistoricoBusca`. O controller importa `from models import FilmeFavorito` porque assim ele pega só a classe que precisa.


## Bloco B — Controller (perguntas 11 a 20)

**11.** Quantos Blueprints existem no projeto? Cite o **nome** de cada um e o **url_prefix** (se tiver).
R: 3 Blueprints: `dashboard`, `filmes` (`url_prefix="/filmes"`) e `favoritos` (`url_prefix="/favoritos"`).

**12.** Em qual arquivo está a rota `/filmes/populares`? Qual é o nome da função Python que responde essa URL?
R: Está em `controllers/filmes_controller.py`. A função é `populares()`.

**13.** O que a função `populares()` faz antes de chamar `render_template`? Cite duas chamadas (Model, Service ou API).
R: Antes do `render_template`, ela chama `api.filmes_populares()` e `FilmeFavorito.listar()`

**14.** Quando o usuário busca um filme em `/filmes/buscar`, qual controller registra o termo no banco? Qual model é usado e em qual linha aproximada?
R: É o `filmes_controller.py`, na função `buscar()`. Ele usa o model `HistoricoBusca`, chamando `HistoricoBusca.registrar(termo, len(filmes))` 

**15.** Abra `controllers/favoritos_controller.py`. Qual método HTTP é exigido para adicionar favorito (`GET` ou `POST`)? Qual a URL completa de exemplo para adicionar o filme id 550?
R: É o método `POST`. exemplo: `/favoritos/adicionar/550`.

**16.** No `filmes_controller.py`, rota `detalhe(filme_id)`: o que acontece se `api.detalhe(filme_id)` retornar `None`?
R: Se `api.detalhe(filme_id)` retornar `None`, a rota faz um `redirect` de volta para `filmes.populares`.

**17.** Onde os Blueprints são **registrados** no Flask? Cite o arquivo e o comando usado (3 registros).
R:  São registrados em `app.py`, com os comandos: `app.register_blueprint(dashboard_bp)`, `app.register_blueprint(filmes_bp)` e `app.register_blueprint(favoritos_bp)`( eu acho ).

**18.** Qual controller cuida da página inicial `/`? Quais variáveis ele envia para o template `index.html`?
R: É o `dashboard_controller.py`. Ele envia: `populares`, `melhores`, `total_favoritos`, e `modo_demo`.

**19.** A pasta `services/tmdb_api.py` é Model, Controller ou View? Justifique: quem chama essa classe e para quê?
R: É um Service, porque esta na pasta service. Quem chama essa classe são os controllers (`dashboard_controller.py`, `filmes_controller.py`), para buscar informações de filmes na API .

**20.** No controller de busca, de onde vem o termo digitado quando o usuário usa o formulário da home (`index.html`)? É `request.form` ou `request.args`? Explique a diferença nesse projeto.
R: Não lembro.

## Bloco C — View (perguntas 21 a 30)

**21.** Onde ficam os templates HTML? Qual caminho completo da pasta?
R: Ficam em `views/templates/`.

**22.** Qual template é a “base” de todas as páginas (layout com menu)? Como os outros templates usam esse layout (qual comando Jinja)?
R: É o `layout.html`. Os outros templates usam `{% extends "layout.html" %}`.

**23.** Abra `views/templates/layout.html`. Liste os 5 links do menu e o `url_for` de cada um.
R:
StreamFlix - `url_for('dashboard.index')`
Populares - `url_for('filmes.populares')`
Melhores - `url_for('filmes.melhores')`
Buscar - `url_for('filmes.buscar')`
Favoritos - `url_for('favoritos.listar')`

**24.** Qual arquivo HTML exibe a seção **“Onde assistir (Brasil)”**? De onde vem a variável `streaming` usada nessa tela?
R: É `views/templates/filmes/detalhe.html`. A `streaming` vem do controller `filmes_controller.py`.

**25.** O arquivo `filmes/_card.html` é uma página inteira ou um pedaço reutilizado? Quem inclui esse arquivo e com qual tag Jinja?
R: É um pedaço reutilizado. Quem inclui é o `index.html` usando tag Jinja `{% include "filmes/_card.html" %}`.

**26.** Em `filmes/detalhe.html`, como a View sabe se o filme já está nos favoritos? Qual variável booleana/objeto controla o botão “Salvar” vs “Remover”?
R: Não sei.
**27.** Onde está o CSS do site? Como o `layout.html` carrega esse arquivo (função Flask/Jinja)?
R: O CSS está em `views/static/css/style.css`. O `layout.html` carrega com `{{ url_for('static', filename='css/style.css') }}`.

**28.** Na listagem de favoritos (`favoritos/lista.html`), qual loop Jinja percorre os registros? Cite 3 campos exibidos na tabela.
R: O loop é `{% for fav in favoritos %}`. Que exibem: `fav.titulo`, `fav.nota` e `fav.ano`.

**29.** O que significa `{% if modo_demo %}` no layout? Quem disponibiliza essa variável para **todos** os templates?
R: Significa "se o site estiver em modo demonstração" mostra um aviso na tela. É o `context_processor` (`inject_globals`).
**30.** Desenhe ou descreva o fluxo completo quando o aluno clica em **“Salvar favorito”** no detalhe do filme, indicando **View → Controller → Model** (e redirect de volta). Cite arquivos envolvidos.
R: não sei, perdao
---

## Entrega

- Arquivo `.txt` ou `.md` com as 30 respostas 

**Critério:** respostas que mostrem que você **abriu o código**, não chute.

Boa exploração!
---