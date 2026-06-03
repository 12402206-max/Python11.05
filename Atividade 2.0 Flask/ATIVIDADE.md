# AtividadeSQLalchemy 2.0 — Loja Tech (Flask + SQLAlchemy)

## Contexto

Você vai montar um **CRUD de produtos tecnológicos** (loja de informática), no mesmo estilo da **AulaSQLalchemy** (Flask + SQLAlchemy, **sem MVC**, tudo em `app.py` + templates).

Tema: cadastrar produtos como notebook, mouse, teclado, headset, etc.

---

## Objetivos

- Criar banco SQLite (`loja.db`)
- Definir a classe **`Produto`** (`db.Model`)
- Implementar **CRUD** no navegador
- Completar templates **Jinja2** com lacunas
- Usar `request.form`, `redirect`, `url_for`

---

## Estrutura do projeto (o que você recebe)

```
AtividadeSQLalchemy_2.0/
├── app.py                 ← INCOMPLETO (você completa)
├── requirements.txt
├── templates/
│   ├── lista.html         ← INCOMPLETO (Jinja)
│   └── formulario.html    ← INCOMPLETO (Jinja)
└── static/css/style.css   ← CSS base (pode personalizar)
```

Após rodar, será gerado: **`loja.db`**

---

## Model `Produto` (você deve criar no `app.py`)

| Coluna     | Tipo        | Descrição                          |
|-----------|-------------|------------------------------------|
| `id`      | Integer     | Chave primária                     |
| `nome`    | String(120) | Nome do produto                    |
| `categoria` | String(60) | Ex.: Notebook, Smartphone, Acessório |
| `preco`   | Float       | Preço em reais                     |
| `estoque` | Integer     | Quantidade em estoque              |

`__tablename__` = `"produtos"`

---

## Rotas obrigatórias

| Método | Rota | Ação |
|--------|------|------|
| GET | `/` | Listar produtos (ordenar por nome) |
| GET/POST | `/cadastrar` | Formulário + salvar novo produto |
| GET/POST | `/editar/<int:produto_id>` | Formulário + atualizar |
| POST | `/excluir/<int:produto_id>` | Excluir produto |

---

## O que está faltando (sua tarefa)

### No `app.py`

1. Importar `SQLAlchemy` de `flask_sqlalchemy`
2. Configurar `SQLALCHEMY_DATABASE_URI` → arquivo `loja.db` na pasta do projeto
3. Criar `db = SQLAlchemy(app)`
4. Completar a classe **`Produto`** (todas as colunas)
5. Chamar `db.create_all()` dentro de `app.app_context()`
6. Completar rotas: query na listagem, `add` + `commit` no cadastro, `get` + update no editar, `delete` + `commit` na exclusão
7. Validar: nome, categoria e preço obrigatórios; estoque ≥ 0

### Nos templates

1. **`lista.html`**: loop `{% for %}`, exibir preço formatado, estoque, links editar/excluir
2. **`formulario.html`**: `action` correto (cadastrar vs editar), campos `name` iguais ao `request.form` no Python

---

## Instalação

```powershell
cd flask/AtividadeSQLalchemy_2.0
pip install -r requirements.txt
python app.py
```

Abrir: **http://127.0.0.1:5000/**

---

## Critérios de entrega

- [ ] Projeto roda sem erro
- [ ] Tabela `produtos` criada em `loja.db`
- [ ] Cadastrar, listar, editar e excluir funcionam
- [ ] Lista mostra: id, nome, categoria, preço, estoque
- [ ] Formulário mantém valores após erro de validação (opcional bônus)

---

## Dicas

- Use a **AulaSQLalchemy** (`alunos`) como modelo — troque `Aluno` por `Produto` e os campos.
- Preço: `float(request.form.get("preco", 0))`
- Estoque: `int(request.form.get("estoque", 0))`
- Marque cada correção com comentário `# feito` para revisão em aula.

---



---

*Referência: `AulaSQLalchemy/app.py` — gabarito completo na pasta `gabarito/` (somente professor).*
