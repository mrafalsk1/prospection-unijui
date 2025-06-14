# API de Prospecção de Alunos - UNIJUÍ

## 1\. Descrição do Projeto

Esta é uma API RESTful robusta, desenvolvida em Python com Flask, projetada para gerir e otimizar o processo de prospecção e captação de futuros alunos para a universidade. A API centraliza os dados de leads (alunos), eventos, escolas de origem e formações de interesse, fornecendo uma base sólida para equipas de marketing e admissão.

O projeto foi concebido seguindo as melhores práticas de engenharia de software, incluindo uma arquitetura em camadas, documentação automática e um sistema de autenticação para garantir a segurança dos dados.

## 2\. Funcionalidades Principais

- **CRUD Completo**: Operações de Criar, Ler, Atualizar e Deletar para todas as entidades principais:

  - Alunos (Students)
  - Eventos (Events)
  - Escolas (Schools)
  - Formações (Formations)
  - Interações (Interactions) - O registo de um aluno num evento.

- **Criação Aninhada**: Capacidade de criar entidades relacionadas de forma aninhada. Por exemplo, ao criar um novo aluno, é possível criar a sua escola de origem na mesma requisição.
- **Filtragem Avançada**: A listagem de interações permite a filtragem por student_id e/ou event_id.
- **Documentação Automática**: Geração automática de uma documentação interativa com Swagger UI, detalhando todos os endpoints, modelos de dados e possíveis retornos.
- **Autenticação Segura**: Todos os endpoints são protegidos por um sistema de autenticação baseado em chave de API estática, que deve ser enviada no cabeçalho Authorization.
- **Arquitetura Escalável**: O código está organizado numa arquitetura de 3 camadas (Controllers, ServiçAos e Modelos) para garantir a separação de responsabilidades, reutilização de código e facilidade de manutenção.

## 3\. Arquitetura

O projeto segue um padrão de arquitetura em camadas para garantir um código limpo e organizado:

- **Camada de API (Controllers)**: Localizada em src/api/, é responsável por gerir as requisições e respostas HTTP. Utiliza flask-restx para definir namespaces, recursos e a documentação Swagger. Esta camada delega toda a lógica de negócio para a camada de serviço.
- **Camada de Serviço (Services)**: Localizada em src/services/, contém toda a lógica de negócio da aplicação. As funções aqui são responsáveis por orquestrar as operações, validar regras de negócio e interagir com a camada de dados.
- **Camada de Dados (Models)**: Localizada em src/models/, representa a estrutura da base de dados através de modelos SQLAlchemy. Utiliza a sintaxe moderna com Mapped e back_populates para garantir clareza e compatibilidade com ferramentas de análise estática.

A estrutura de diretórios é a seguinte:

```/
├─ migrations/
├─`─ src/
│   ├── __init__.py        # Factory da aplicação Flask
│   ├── api/
│   │   ├── __init__.py    # Configuração principal do Flask-RESTX
│   │   ├── dtos/          # Modelos de dados para a API (Swagger)
│   │   ├── decorators.py  # Decorators para autenticação e tratamento de erros
│   │   └── *_controller.py # Endpoints para cada entidade
│   ├── models/
│   │   └── *.py           # Modelos de dados do SQLAlchemy
│   ├── services/
│   │   └── *_service.py   # Lógica de negócio para cada entidade
│   └── utils/
│       └── service_utils.py # Utilitários para a camada de serviço (Enum de erros)
├── config.py
├── .env
└── run.py
```

## 4\. Tecnologias Utilizadas

- **Linguagem**: Python 3.12+
- **Framework Web**: Flask, Flask-RESTX
- **Base de Dados**: PostgreSQL
- **ORM**: SQLAlchemy, Flask-SQLAlchemy
- **Migrações**: Alembic, Flask-Migrate
- **Gestão de Dependências**: uv

## 5\. Configuração e Instalação

Siga os passos abaixo para configurar e executar o projeto localmente.

### Pré-requisitos

- Python 3.12 ou superior
- PostgreSQL instalado e em execução
- uv

### 1\. Clonar o Repositório

```
    git clone
    cd prospection-unijui
```

### 2\. Configurar Variáveis de Ambiente

Crie um arquivo chamado .env na raiz do projeto e adicione as seguintes variáveis. Substitua os valores pelos seus.

```
    DATABASE_URL="postgresql://seu_usuario:sua_senha@localhost:5432/unijui_prospecting"
    SECRET_KEY="aqui-vai-uma-chave-secreta-muito-forte-e-dificil-de-adivinhar"   `
```

### 3\. Configurar a Base de Dados

Certifique-se de que a base de dados (unijui_prospecting, neste exemplo) já foi criada no seu PostgreSQL.

```
   export FLASK_APP=run.py   # macOS/Linux
   set FLASK_APP=run.py     # Windows CMD
   # Inicie o ambiente de migrações (só na primeira vez)
   uv run flask db init  # Gere o script de migração com base nos modelos
   uv run flask db migrate -m "M`igração inicial com todas as entidades"
   # Aplique a migração para criar astabelas
   uv run flask db upgrade   `
```

### 4\. Executar a API

As dependências são instaladas automaticamente no primeiro comando `uv run`

```bash
    uv run flask run
```

O ambiente virtual também é criado automaticamente com em .venv, logo há a possibilidade de iniciar a API pelo venv da mesma forma que é feito com pip.

A sua API estará agora a correr em http://127.0.0.1:5000.

### 5\. Documentação Swagger

Abra o seu navegador e navegue até:**http://127.0.0.1:5000/api/v1/doc/**

Todos os endpoints da API são protegidos. Para fazer uma requisição, é necessário enviar a sua SECRET_KEY no cabeçalho Authorization.

**Formato do Cabeçalho:**

`Authorization: ApiKey`

**Para testar na UI do Swagger:**

1.  Clique no botão **"Authorize"** no canto superior direito.
2.  Na janela que se abre, insira a sua chave no formato ApiKey sua_chave_secreta.
3.  Clique em **"Authorize"** e feche a janela.
4.  Agora, todas as suas requisições feitas através da UI incluirão o cabeçalho de autorização correto.
