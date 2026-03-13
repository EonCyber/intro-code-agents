
# Adicionar API Key ao Path

Pode ser adquirida em :
https://platform.claude.com/

```bash
export ANTHROPIC_API_KEY=""
``` 


# Comandos da Sessão

Shift + Tab – autoriza o claude escrever arquivos livremente na sessão

`/help` – mostra ajuda de comandos.
`/clear `– limpa histórico da conversa.
    - usar quando contexto parecer poluido
    - usar para reduzir o consumo de tokens
`/model` – muda modelo usado na sessão.
    - ex: `/model claude-3-5-sonnet`
`/config` – interface rápida para configurações.
    - usar para verificar o modelo, comportamente e permissoes
`/context` – mostra uso atual de contexto e tokens.
`/bug` – reporta um bug ao time do Claude.
`/export` – Exporta a conversa atual para arquivo.
    - ex: `/export session.md`
`/init` – Cria um arquivo claude.md no diretório atual.


`/plan` – Habilita modo Plan que é um modo de planejamento, onde vai quebrar cada ação em um plano antes de executar. (2x Shift+Tab ON ,depois 1x Shift+Tab Off)


# Aumentando o "Pensamento" do Claude
    Think --- Pense
    Think More --- Pense Mais
    Think a lot --- Pense Muito
    Think Longer --- Pense Por Mais Tempo
    Ultrathink --- "Ultra-Pensamento"

# Claude.md Contexto do Projeto

Funciona como um arquivo de contexto do projeto onde o Claude vai buscar padrões e regras antes de gerar suas respostas.

Nele nós podemos definir `arquitetura`, `padrões`, `estrutura de pastas`, `regras/exclusoes para o claude`, `estratégia de nomeclatura` e mais.


## Possuímos 3 Níveis de CLAUDE.md

- `CLAUDE.md`  Disponível para o projeto e compartilhável no repositório.
- `CLAUDE.local.md` Deve conter de instrucao pessoal nao compartilhável (não commitado)
- `~/.claude/CLAUDE.md` Contem contexto compartilhado com todos os projetos da máquina

# As 6 Seções Principais de um Claude.md

## 1 Comandos de Execução

No início do arquivo pontue os comandos necessários para rodar
o projeto, disparar testes, fazer o build e instalar dependencias, incluindo flags e tudo mais que for preciso.

Ex:
```bash
# Instala Dependencias
pip install -r requirments.txt
# Sobe o projeto localmente
python run main.py

```
## 2 Estrutura de Projeto

Explicar como funciona a estrutura de pastas do projeto e para que.

Ex:
```python
src/
    /controller # Deve conter apis
    /service # Deve conter a camada de business logic
    /repository # Responsavel pelo ORM
main.py 
```

## 3 Stack Utilizada (Tech Stack)

Definir exatamente que tipo de bibliotecas, linguagens e se possivel versões preferidas de cada uma.

## 4 Estilo de Programação (Code Style)

Exemplos de implementação:
```python
# Good snippet
...
# Bad snippet
...
```
Design Patterns
```python
# Utilizar Strategy Patterns implementado com Factories e Decorators
class Strategy(Protocol):
    def execute(self, args):
        ...
class StrategyRegistry:
    _strategies: Dict[str, Type[Strategy]] = {}
    def register(cls, name: str):
        def decorator(strategy_cls: Type[Strategy])
    def get(cls, name:str):
        ...
    def create(cls, name: str):
        ...

@StrategyRegistry.register("new-strat")
class NewStrategy:
    def execute(self, args):
        ...
    ...
``` 
Convenção de Nomes
```python
# Estamos usando snake_case
def my_function(self, paramA):
    ...
```

## 5 Arquitetura de Commit (Git Workflow)

Definir nomes de branchs, tipos de branchs e o que precisa para cada commit.

## 6 Limites (Boundaries)

Informe o que a IA nunca deve fazer, por exemplo:

Ex:
- Nunca comitar arquivos contendo PII
- Nunca comitar arquivos contendo secrets
- Nunca modificar a camada /config
- Nunca deletar testes unitarios com falha