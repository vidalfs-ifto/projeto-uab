# Sistema de Atendimento

Este é um sistema web de atendimento baseado em Flask, implementado conforme as especificações em `doc/03-especs.md`.

## Funcionalidades
- Autenticação e Autorização baseada em roles (Proprietário, Administrador, Atendente, Cliente).
- Registro de Clientes e Login.
- Integração OAuth com Google.
- Gestão de Usuários (Proprietário cria Administradores, Administrador cria Atendentes).
- Sistema de Tickets (Clientes abrem, Atendentes respondem).
- Relatórios Gerenciais (apenas para Administradores).
- Auditoria de ações críticas (LogModel).

## Requisitos
- Python 3.10+
- Flask
- SQLAlchemy
- Authlib
- Requests
- pytest (para testes)

## Instalação
1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv .venv`
3. Ative o ambiente virtual: `source .venv/bin/activate`
4. Instale as dependências: `pip install -r requirements.txt`
5. Configure o arquivo `.env` baseado no `.env.example`.

## Execução
Para iniciar o sistema:
```bash
python run.py
```

## Testes
Para executar os testes automatizados:
```bash
PYTHONPATH=. pytest
```
Consulte `doc/testing.md` para mais detalhes sobre o plano de testes.
