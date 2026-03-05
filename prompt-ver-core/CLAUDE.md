# CLAUDE.md

## Environment Setup

Requires Python 3.13.7 and `uv` as the package manager.

```bash
# Install dependencies
uv sync

# To install a new single dependency use
uv add <new_dependency>

# Run the project
uv run python main.py
```

## Project Structure

Its an Hexagonal Architecture Structure

```python
src/
    app/ # Application Layer (deve conter use cases)
    domain/ # Core Puro (dtos, models, entidades, sem infra)
    adapters/ # Conectores com Libs, Clientes Externos e Impl de Ports
    ports/ # Interfaces para Solucoes Inbound e Outbound
    infra/ # Configuracoes de db, message broker e do projeto em geral
    main.py # Inicializa e faz Instanciações
```

## Tech stack:

Our Language is Python Version 3.13.7

- **Database:** SQLAlchemy (async) + aiosqlite — persists prompt versions
- **Messaging:** NATS (nats-py) — receives incoming prompt payloads
- **Logging:** structlog for structured log output
- **CLI/Output:** rich for terminal formatting

## Code Style

Naming Convention:
```python
# We're using snake_case for functions, variables and files
compound_folder/

my_var = 10

def my_function(self, paramA):
    ...
```