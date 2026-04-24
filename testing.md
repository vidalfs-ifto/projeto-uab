# Plano de Testes - Sistema de Atendimento

Este documento descreve a estratégia de testes para o Sistema de Atendimento, seguindo a metodologia **TDD (Test-Driven Development) First**. A prioridade é garantir que as funcionalidades críticas sejam validadas por testes automatizados antes ou durante o desenvolvimento, assegurando a integridade do sistema e prevenindo regressões.

## 1. Objetivos

- Validar a lógica de negócio conforme `doc/03-especs.md`.
- Garantir o Controle de Acesso Baseado em Funções (RBAC).
- Assegurar a integridade da trilha de auditoria (logs).
- Proporcionar um ambiente de desenvolvimento ágil e seguro com feedback imediato.

## 2. Configuração do Ambiente de Testes

As dependências de teste foram incluídas no `requirements.txt`. Para instalar:

```bash
pip install -r requirements.txt
```

### Execução dos Testes

Para executar todos os testes com relatório de cobertura:

```bash
pytest --cov=app tests/
```

## 3. Estratégia de Testes

### 3.1. Tipos de Teste

1.  **Testes Unitários:** Validação de modelos, utilitários e funções isoladas (ex: hashing de senhas, decoradores de permissão).
2.  **Testes de Integração:** Validação de rotas (controllers), persistência no banco de dados e fluxo entre componentes.
3.  **Mocks:** Utilizados para simular provedores externos (OAuth Google) e evitar dependências de rede.

### 3.2. Banco de Dados de Teste

Será utilizado um banco de dados SQLite em memória (`sqlite:///:memory:`) para garantir que os testes sejam rápidos e isolados.

## 4. Plano de Cenários (TDD First)

### 4.1. Autenticação e Autorização (Crítico)

| Funcionalidade | Cenário de Teste | Prioridade | Técnica |
| :--- | :--- | :--- | :--- |
| **Login** | Sucesso com credenciais válidas e criação de sessão. | Alta | Integração |
| **Login** | Falha com senha incorreta ou usuário inexistente. | Alta | Integração |
| **Registro** | Cliente consegue se registrar autonomamente. | Alta | Integração |
| **RBAC** | Bloqueio de acesso (403) ao tentar acessar rota sem permissão. | Crítica | Unitário/Decorador |
| **OAuth** | Sucesso no login via Google e criação automática de usuário. | Média | Mock (Authlib) |

### 4.2. Gestão de Usuários e Auditoria (Crítico)

| Funcionalidade | Cenário de Teste | Prioridade | Técnica |
| :--- | :--- | :--- | :--- |
| **Criação Admin** | Proprietário cria novo Administrador com sucesso. | Crítica | Integração |
| **Criação Atendente** | Administrador cria novo Atendente com sucesso. | Alta | Integração |
| **Auditoria** | Verificação se um registro de log foi gerado após criar usuário. | Crítica | Integração/Model |
| **Isolamento** | Atendente não pode criar outros usuários (Admin/Proprietário). | Crítica | Integração |

### 4.3. Ciclo de Vida de Tickets

| Funcionalidade | Cenário de Teste | Prioridade | Técnica |
| :--- | :--- | :--- | :--- |
| **Abertura** | Cliente abre ticket com assunto e descrição. | Alta | Integração |
| **Resposta** | Atendente altera status para "RESOLVIDO" e associa seu ID. | Alta | Integração |
| **Visibilidade** | Cliente vê apenas seus próprios tickets. | Crítica | Integração |
| **Visibilidade** | Atendente vê todos os tickets do sistema. | Média | Integração |

### 4.4. Relatórios Gerenciais

| Funcionalidade | Cenário de Teste | Prioridade | Técnica |
| :--- | :--- | :--- | :--- |
| **Filtro Geral** | Admin visualiza agregados totais de tickets. | Média | Integração |
| **Filtro Atendente** | Admin visualiza tickets específicos de um atendente sob sua gestão. | Média | Integração |

## 5. Mocking de Dependências Externas

Para o OAuth do Google, utilizaremos o `pytest-mock` para injetar um retorno simulado da biblioteca `Authlib`:

```python
# Exemplo de Mock no arquivo tests/conftest.py
@pytest.fixture
def mock_google_oauth(mocker):
    mock = mocker.patch('app.controllers.auth_controller.OBTER_DADOS_GOOGLE')
    mock.return_value = {'email': 'teste_oauth@gmail.com', 'nome': 'Teste Google'}
    return mock
```

## 6. Critérios de Aceite para Entrega

- Cobertura de testes superior a 80%.
- Todos os testes de cenários "Críticos" e "Altos" devem passar.
- Nenhum segredo (SECRET_KEY, senhas) deve estar presente nos arquivos de teste.
- O banco de dados de produção não deve ser afetado pela execução dos testes.
