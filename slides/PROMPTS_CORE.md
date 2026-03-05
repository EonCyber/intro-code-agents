# Estrutura de Prompt de Codigo

Dividir o desenvolvimento em Fases.

## O prompt de Cada Fase Deve

- Explicar o objetivo da fase.

- Definir as Diretrizes.

- Sugestoes de Desenvolvimento.

- Resultados esperados.

- Limitadores.

# PRIMEIRA FASE - Domínio

```
# Fase de Desenvolvimento — Camada de Domain

## Objetivo da Fase

Nesta fase iremos implementar a camada de Domain do sistema de versionamento de prompts.

O objetivo é modelar corretamente os conceitos centrais do domínio, garantindo regras de negócio, consistência e capacidade de transição de estado entre as camadas da aplicação.

O foco deve estar na modelagem rica do domínio, evitando estruturas anêmicas.

---

## Diretrizes

- Definir as entidades principais do sistema.
- Garantir que o domínio encapsule suas próprias regras.
- Modelar transições de estado de forma explícita.
- Considerar versionamento como parte central do comportamento do sistema.
- Preservar histórico sem perda de informação.
- Garantir que o modelo permita futura evolução para arquitetura orientada a eventos.

---

## Sugestões Iniciais de Entidades

O sistema deve conter entidades que representem:

- Prompt  
- Versão de Prompt  
- Estados relacionados ao ciclo de vida (ativo, inativo, deletado)

Cada Prompt deve conter informações como:

- Identificador único
- Versões associadas
- Controle de versão ativa
- Conteúdo versionado
- Timestamps relevantes
- Flags de uso ou ativação

---

## O que se espera como resultado

- Definição das entidades do domínio
- Definição clara das responsabilidades de cada entidade
- Modelagem que permita:
  - Criação de novas versões
  - Ativação de versões específicas
  - Soft deletion
  - Recuperação
- Estrutura preparada para futuras extensões

---

## Fora do Escopo

- Persistência
- Infraestrutura
- API
- Interface
- Implementação de banco de dados

O foco exclusivo é a modelagem da camada de Domain.
```

# SEGUNDA FASE - App e Ports 

```
# Fase de Desenvolvimento — Camadas Application (app) e Ports (port)

## Objetivo da Fase

Nesta fase iremos implementar as camadas de Application e Ports do sistema de versionamento de prompts.

A camada `app` deve orquestrar os casos de uso utilizando exclusivamente as regras e entidades já definidas na camada `domain`.

A camada `port` deve definir as abstrações necessárias para que a aplicação interaja com persistência, publicação de eventos e demais dependências externas.

Nenhuma implementação concreta deve ser criada nesta fase.

---

# Estrutura do Projeto

app/
port/

A dependência deve respeitar:

- app depende de domain
- app depende de port
- port não depende de infra
- port não depende de adapter
- nenhuma camada externa deve ser referenciada

---

# Camada Application (app)

A camada deve conter casos de uso explícitos e isolados.

## Casos de Uso Esperados

- Criar novo Prompt
- Criar nova versão de Prompt existente
- Alterar conteúdo com geração automática de nova versão
- Ativar uma versão específica
- Soft delete de Prompt
- Recuperação de Prompt
- Listagem:
  - Buscar por ID
  - Listar versões
  - Listar ativos
  - Listar deletados

## Regras Importantes

- Toda alteração de conteúdo deve gerar nova versão.
- Apenas uma versão pode estar ativa por Prompt.
- A aplicação deve respeitar as invariantes do Domain.
- A lógica de negócio permanece no Domain.
- Application apenas coordena fluxo e persistência.

## Organização Esperada

- Separação clara entre comandos (write) e consultas (read).
- Cada caso de uso deve ser independente.
- Dependências devem ser injetadas via construtor.
- Nenhuma dependência concreta deve ser utilizada.

---

# 🔌 Camada Ports (port)

A camada `port` deve definir as interfaces necessárias para suportar os casos de uso da Application.

## Portas Esperadas

- Repositório de Prompt
- Publicador de Eventos de Domínio (se aplicável)
- Unidade de Trabalho (se necessário para consistência transacional)

As portas devem:

- Ser definidas como interfaces ou Protocols.
- Conter apenas contratos mínimos necessários.
- Não conter lógica de negócio.
- Não conhecer tecnologia específica.

---

# Consistência Arquitetural

- Versionamento deve ser tratado como parte central dos fluxos.
- A aplicação deve coordenar corretamente criação de versões e ativação.
- As portas devem refletir apenas as necessidades reais dos casos de uso.

---

# Fora do Escopo

- Implementações concretas
- Banco de dados
- Mensageria
- Framework web
- Adapters
- Infraestrutura

O foco exclusivo é a orquestração da aplicação e a definição das abstrações necessárias.
```

# TERCEIRA FASE - Implementação de Diffs

```
# Fase de Desenvolvimento — Implementação de Lógica de Diff entre Versões

## Objetivo da Fase

Nesta fase iremos implementar a lógica responsável por comparar versões de um Prompt, permitindo a identificação clara das diferenças entre duas versões específicas.

A funcionalidade deve facilitar a inspeção de mudanças, preservando consistência arquitetural e respeitando as responsabilidades de cada camada.

---

# Diretrizes Arquiteturais

- A lógica de comparação deve pertencer ao Domain.
- A camada `app` deve apenas orquestrar o caso de uso.
- Nenhuma tecnologia específica de renderização (HTML, frontend, etc.) deve ser utilizada.
- O resultado deve ser estruturado e neutro, preparado para consumo externo.
- O design deve permitir futura evolução do algoritmo de diff sem impactar os casos de uso.

---

# Camada Domain

O domínio deve:

- Definir a estrutura que representa o resultado de um diff.
- Implementar a lógica de comparação entre duas versões.
- Garantir que apenas versões válidas possam ser comparadas.
- Manter coerência com as regras já definidas para versionamento.

A comparação deve:

- Identificar adições
- Identificar remoções
- Identificar modificações
- Preservar ordem quando relevante

A modelagem deve permitir futura evolução para comparação semântica, se necessário.

---

# Camada Application

A camada `app` deve implementar um novo caso de uso responsável por:

- Receber identificador do Prompt
- Receber duas versões a serem comparadas
- Recuperar os dados via `PromptRepositoryPort`
- Delegar a comparação ao Domain
- Retornar o resultado estruturado

O caso de uso deve ser tratado como Query (leitura).

---

# Camada Ports

Verificar se o repositório atual já suporta:

- Buscar Prompt por ID
- Acessar versões específicas

Caso necessário, ajustar a interface do repositório mantendo contratos mínimos.

Nenhuma implementação concreta deve ser criada.

---

# Consistência Arquitetural

- A lógica de diff não deve depender de infraestrutura.
- A Application não deve conter algoritmo de comparação.
- O retorno deve ser independente de tecnologia de apresentação.
- O design deve permitir futura extensão (ex: múltiplos algoritmos de diff).

---

# Fora do Escopo

- Renderização visual
- Highlight em HTML
- Implementação de biblioteca externa
- Integração com frontend
- Infraestrutura

O foco exclusivo é a modelagem e implementação da lógica de comparação entre versões dentro da arquitetura hexagonal.
```

# Quarta Fase - Infra e Adapters

```
# Fase de Desenvolvimento — Infraestrutura e Adapters

## Objetivo da Fase

Nesta fase iremos implementar as camadas `infra` e `adapter`, conectando o core do sistema (domain + app + port) ao mundo externo.

O sistema deve:

- Expor interface via eventos NATS
- Persistir dados utilizando SQLite
- Implementar repositórios com SQLAlchemy
- Utilizar logging estruturado com structlog e rich
- Manter total isolamento do domínio

Nenhuma regra de negócio deve ser implementada nesta fase.

---

# Estrutura do Projeto

adapter/
infra/

As dependências devem respeitar:

- adapter depende de app e port
- infra pode ser usada pelos adapters
- domain e app não devem depender de infra
- nenhuma tecnologia externa deve vazar para dentro do core

---

# Adapter de Mensageria (NATS)

A camada `adapter/messaging` deve:

- Conectar ao NATS
- Escutar eventos (subjects)
- Mapear cada subject para um caso de uso da Application
- Traduzir payloads para objetos de entrada dos use cases
- Implementar padrão request/reply para operações de leitura
- Tratar timeout e erros adequadamente
- Logar todas as entradas e saídas

Requisitos:

- Commands devem funcionar de forma assíncrona
- Queries (listagens e buscas) devem usar request/reply síncrono
- Deve existir correlação de request (correlation id)
- Nenhuma lógica de negócio deve existir no adapter

---

#  Adapter de Persistência

A camada `adapter/persistence` deve:

- Implementar as interfaces definidas em `port`
- Utilizar SQLAlchemy para persistência
- Converter entidades de domínio ↔ modelos ORM
- Não expor modelos ORM para fora do adapter
- Garantir isolamento entre modelo relacional e modelo de domínio

---

# Infraestrutura

A camada `infra` deve conter:

## Banco de Dados

- Configuração do engine SQLite
- Configuração de sessão
- Inicialização de tabelas
- Configuração adequada para ambiente concorrente (ex: WAL se necessário)

## NATS Client

- Inicialização e gerenciamento de conexão
- Configuração centralizada

## Logging

- Configuração centralizada de structlog
- Integração com rich para saída formatada no terminal
- Logger reutilizável pelos adapters
- Logging estruturado com contexto

---

# Logging

Todos os fluxos devem ser logados:

- Recebimento de evento
- Execução de caso de uso
- Persistência
- Resposta enviada
- Erros e exceções

O domínio não deve depender diretamente do logger.

---

# Consistência Arquitetural

- Nenhuma regra de negócio pode ser implementada fora do Domain.
- Application continua responsável apenas pela orquestração.
- Adapters apenas traduzem e conectam.
- Infra apenas configura tecnologia.

---

# Fora do Escopo

- Documentação AsyncAPI (será fase 5)
- HTTP
- Swagger
- Frontend
- Otimizações avançadas de performance

O foco exclusivo é conectar o sistema ao mundo externo mantendo a arquitetura hexagonal íntegra.
```

