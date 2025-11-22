# 🗨️ TalkHub API - Backend

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13.5-14354C?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.121.3-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/MongoDB-4.15.4-47A248?style=for-the-badge&logo=mongodb&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Pytest-9.0.1-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" />
  <img src="https://img.shields.io/badge/Pydantic-2.12.4-4E8DBE?style=for-the-badge&logo=pydantic&logoColor=white" />
</p>

<p align="center">
  API para mensageria e autenticação de usuários, desenvolvida com Python, FastAPI e MongoDB Atlas.
</p>

---

## 🎯 Sobre o Projeto

Este projeto é o backend do TalkHub, uma plataforma de mensagens com autenticação, CRUD de usuários, integração com MongoDB Atlas e arquitetura escalável para produção. O backend gerencia usuários, autenticação, e está pronto para integração com recursos de chat e E2EE.

### 🔧 Principais Tecnologias

![Python](https://img.shields.io/badge/python-14354C?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-4E8DBE?style=for-the-badge&logo=pydantic&logoColor=white)

## ✨ Características

- 🔒 Autenticação de usuários (pronto para JWT)
- 🧑‍💼 CRUD completo de usuários
- 📱 Pronto para integração com E2EE e envio de SMS
- 🐳 Deploy com Docker
- 🧪 Testes automatizados com Pytest e mongomock

## 🚀 Tecnologias Utilizadas

- **Python 3.13.5** - Linguagem principal
- **FastAPI 0.121.3** - Framework web
- **MongoDB (pymongo 4.15.4)** - Banco de dados NoSQL
- **Docker 24.0** - Containerização
- **Pytest 9.0.1** - Testes automatizados
- **Pydantic 2.12.4** - Validação de dados

## 📁 Estrutura do Projeto

```
backend-talkhub/
├── api/
│   └── routes/         # Rotas da API (users, etc)
├── auth/               # Autenticação e login
├── controllers/        # Lógica dos endpoints
├── models/             # Modelos Pydantic
├── services/           # Regras de negócio
├── tests/              # Testes automatizados
├── utils/              # Utilitários
├── database/           # Conexão com MongoDB
├── config.py           # Configuração da aplicação
├── main.py             # Ponto de entrada FastAPI
├── requirements.txt    # Dependências Python
├── Dockerfile          # Build da imagem Docker
├── Makefile            # Comandos de automação
├── .env.example        # Exemplo de variáveis de ambiente
└── README.md           # Documentação
```

## ⚙️ Configuração do Ambiente

### 1. Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e preencha os valores:

```sh
cp .env.example .env
```

- Configure as credenciais do MongoDB Atlas no `.env`.

### 2. Instalação Local

Instale as dependências:

```sh
pip install -r requirements.txt
```

### 3. Execução Local

Execute a API:

```sh
uvicorn main:app --reload
```

Acesse a API em [http://localhost:8000](http://localhost:8000)

### 4. Execução com Docker

Para rodar toda a stack:

```sh
docker build -t talkhub-backend .
docker run -p 8000:8000 --env-file .env talkhub-backend
```

## 🐳 Docker

- O projeto já possui `Dockerfile` configurado para produção.
- As variáveis de ambiente são lidas do arquivo `.env`.
- Recomenda-se usar MongoDB Atlas para persistência de dados.

## 🧪 Testes

- Testes automatizados em `tests/`
- Para rodar: `pytest`
- Testes garantem isolamento e validação dos endpoints de usuários

---

<p align="center">
  Desenvolvido com 💜 por Felipe Kravec Zanatta
</p>
