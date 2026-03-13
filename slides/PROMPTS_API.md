# Prompt Version API

## Estrutura de Prompt

- Explicar o objetivo da fase.
- Definir as Diretrizes.
- Sugestoes de Desenvolvimento.
- Resultados esperados.
- Limitadores.


## Primeira Fase - Services

```

========================================
1. OBJETIVO DA FASE
========================================

Nesta fase do projeto, o objetivo é implementar apenas duas camadas do sistema:

- Service Layer (casos de uso)
- Messaging Layer (publicação de eventos NATS)

A arquitetura geral do sistema é baseada em separação de responsabilidades inspirada em Clean Architecture / DDD:

Controllers (FastAPI)  ← NÃO implementar nesta fase
        ↓
Service Layer (Use Cases)  ← IMPLEMENTAR
        ↓
Messaging Layer (NATS Publisher)  ← IMPLEMENTAR
        ↓
NATS Broker

Os controllers já existirão ou serão implementados em outra fase. Portanto, nesta etapa **não deve ser gerado código de controller**.

Os serviços devem assumir que irão receber dados já validados vindos dos controllers.

Responsabilidades da Service Layer:

- Receber dados vindos da camada de controller
- Converter os dados em payloads de eventos
- Delegar a publicação para a camada de messaging
- Representar cada operação como um caso de uso

Responsabilidades da Messaging Layer:

- Encapsular toda comunicação com NATS
- Publicar eventos usando a biblioteca `nats-py`
- Garantir serialização correta dos payloads

Os serviços **não devem falar diretamente com NATS**, mas sim através de uma abstração de publisher.

Fluxo esperado:

Controller → Service → NATSPublisher → NATS Broker

Controllers **não fazem parte desta fase** e **não devem ser implementados**.


========================================
2. DEFINIR AS DIRETRIZES
========================================

Implementar apenas estas camadas:

- services
- messaging
- models (apenas DTOs)

Não criar controllers.

Arquitetura obrigatória:

services/
    prompt_service.py

messaging/
    nats_publisher.py

models/
    prompt_models.py


Regras arquiteturais:

1. Cada operação do domínio deve ser implementada como um método de serviço.

2. Cada método do serviço deve publicar exatamente um evento NATS.

3. Os serviços devem depender de uma abstração de publisher:

NATSPublisher

4. Apenas a camada `messaging` pode importar ou utilizar `nats-py`.

5. Os serviços devem apenas:

- montar o payload
- definir o subject
- chamar o publisher

6. Os DTOs de entrada devem ser definidos na camada `models`.

7. Os payloads enviados para NATS devem corresponder exatamente aos eventos definidos pelo script de teste.


========================================
3. SUGESTÕES DE DESENVOLVIMENTO
========================================

Estrutura recomendada:

services/
    prompt_service.py

messaging/
    nats_publisher.py

models/
    prompt_models.py


DTOs devem representar as entradas que futuramente virão dos controllers.

Exemplo de DTO:

class CreatePromptRequest:
    name: str


Implementar um publisher responsável por encapsular o uso de NATS:

class NATSPublisher:

    def __init__(self, nc):
        self.nc = nc

    async def publish(self, subject: str, payload: dict):
        await self.nc.publish(
            subject,
            json.dumps(payload).encode()
        )


Os serviços devem depender dessa abstração.

Exemplo de implementação de serviço:

class PromptService:

    def __init__(self, publisher: NATSPublisher):
        self.publisher = publisher

    async def create_prompt(self, req: CreatePromptRequest):

        payload = {
            "name": req.name
        }

        await self.publisher.publish(
            "prompts.v1.commands.create_prompt",
            payload
        )


Padrão esperado para todos os métodos:

1. Receber DTO
2. Construir payload
3. Publicar evento NATS
4. Encapsular a lógica do caso de uso


========================================
4. RESULTADOS ESPERADOS
========================================

Ao final desta fase devem existir:

1. Implementação completa de `NATSPublisher` na camada messaging
2. Implementação do `PromptService` com todos os casos de uso
3. DTOs na camada `models`
4. Separação clara entre services e messaging

Os métodos de serviço devem publicar exatamente os mesmos eventos utilizados no script de testes.

Eventos esperados:


----------------------------------------
create_prompt
----------------------------------------

Subject:

prompts.v1.commands.create_prompt

Payload:

{
  "name": "smoke-test-prompt"
}


----------------------------------------
add_version
----------------------------------------

Subject:

prompts.v1.commands.add_version

Payload:

{
  "prompt_id": "<uuid>",
  "content": "Hello, world! Version 1"
}


----------------------------------------
update_content
----------------------------------------

Subject:

prompts.v1.commands.update_content

Payload:

{
  "prompt_id": "<uuid>",
  "content": "Hello, world! Version 2 — edited"
}


----------------------------------------
activate_version
----------------------------------------

Subject:

prompts.v1.commands.activate_version

Payload:

{
  "prompt_id": "<uuid>",
  "version_id": "<uuid>"
}


----------------------------------------
get_prompt_by_id
----------------------------------------

Subject:

prompts.v1.queries.get_prompt_by_id

Payload:

{
  "prompt_id": "<uuid>"
}


----------------------------------------
list_versions
----------------------------------------

Subject:

prompts.v1.queries.list_versions

Payload:

{
  "prompt_id": "<uuid>"
}


----------------------------------------
list_active_prompts
----------------------------------------

Subject:

prompts.v1.queries.list_active_prompts

Payload:

{
}


----------------------------------------
compare_versions
----------------------------------------

Subject:

prompts.v1.queries.compare_versions

Payload:

{
  "prompt_id": "<uuid>",
  "version_id_before": "<uuid>",
  "version_id_after": "<uuid>"
}


----------------------------------------
soft_delete_prompt
----------------------------------------

Subject:

prompts.v1.commands.soft_delete_prompt

Payload:

{
  "prompt_id": "<uuid>"
}


----------------------------------------
list_deleted_prompts
----------------------------------------

Subject:

prompts.v1.queries.list_deleted_prompts

Payload:

{
}


----------------------------------------
recover_prompt
----------------------------------------

Subject:

prompts.v1.commands.recover_prompt

Payload:

{
  "prompt_id": "<uuid>"
}


========================================
5. LIMITADORES
========================================

Restrições obrigatórias:

- NÃO implementar controllers
- Implementar apenas services, messaging e models
- Utilizar async/await
- Utilizar type hints
- Apenas a camada messaging pode usar nats-py
- Os serviços não devem depender diretamente do cliente NATS
- Todos os payloads devem ser serializados em JSON antes da publicação
- Cada método de serviço deve publicar exatamente um evento
- Não adicionar lógica de negócio fora da camada de services
```

# Segunda Fase - Controllers


```
========================================
1. OBJETIVO DA FASE
========================================

Nesta fase o objetivo é implementar a camada de Controllers utilizando FastAPI.

Na fase anterior já foram implementadas as seguintes camadas:

- models (DTOs)
- services (casos de uso)
- messaging (NATSPublisher)

Agora será criada a camada responsável por:

- Expor endpoints HTTP
- Receber requisições do cliente
- Validar dados usando DTOs da camada models
- Invocar os métodos da camada services

Os controllers NÃO devem conter lógica de negócio.

Toda a lógica de negócio e publicação de eventos NATS já está encapsulada em:

PromptService

Fluxo final esperado da aplicação:

HTTP Request
      ↓
FastAPI Controller
      ↓
PromptService (Service Layer)
      ↓
NATSPublisher (Messaging Layer)
      ↓
NATS Broker


========================================
2. DEFINIR AS DIRETRIZES
========================================

Implementar a camada de controllers utilizando FastAPI.

Estrutura esperada:

controllers/
    prompt_controller.py

main.py


Regras arquiteturais:

1. Controllers apenas recebem requisições HTTP.

2. Controllers devem usar DTOs da camada `models`.

3. Controllers devem invocar métodos do `PromptService`.

4. Controllers NÃO devem:
   - acessar NATS
   - criar payloads de eventos
   - conter lógica de domínio

5. Todos os endpoints devem ser agrupados em um router FastAPI.

6. O router deve ser registrado no servidor FastAPI no arquivo `main.py`.

7. A instância de `PromptService` deve ser inicializada e injetada nos controllers.

8. Os endpoints devem mapear diretamente para os casos de uso existentes no PromptService.


========================================
3. SUGESTÕES DE DESENVOLVIMENTO
========================================

Estrutura recomendada:

controllers/
    routes.py

services/
    prompt_service.py

messaging/
    nats_publisher.py

models/
    prompt_models.py

main.py


Criar um router no controller:

from fastapi import APIRouter

router = APIRouter(prefix="/prompts", tags=["Prompts"])


Os endpoints devem receber DTOs definidos em `models`.

Exemplo de endpoint:

POST /prompts

async def create_prompt(req: CreatePromptRequest)

Implementação esperada:

1. Receber DTO
2. Invocar PromptService
3. Retornar resposta


Exemplo de padrão esperado:

@router.post("/")
async def create_prompt(req: CreatePromptRequest):
    return await prompt_service.create_prompt(req)


Outro exemplo:

POST /prompts/{prompt_id}/versions

@router.post("/{prompt_id}/versions")
async def add_version(prompt_id: str, req: AddVersionRequest):
    return await prompt_service.add_version(prompt_id, req.content)


Os controllers devem usar async/await.


========================================
4. RESULTADOS ESPERADOS
========================================

Ao final desta fase devem existir:

1. Controller FastAPI para os endpoints de prompts
2. Router configurado e organizado
3. Integração direta com PromptService
4. Inicialização do servidor FastAPI no arquivo main.py
5. Registro do router no app


Endpoints esperados:


----------------------------------------
POST /prompts
----------------------------------------

Invoca:

PromptService.create_prompt()


----------------------------------------
POST /prompts/{prompt_id}/versions
----------------------------------------

Invoca:

PromptService.add_version()


----------------------------------------
PUT /prompts/{prompt_id}/content
----------------------------------------

Invoca:

PromptService.update_content()


----------------------------------------
POST /prompts/{prompt_id}/activate
----------------------------------------

Invoca:

PromptService.activate_version()


----------------------------------------
GET /prompts/{prompt_id}
----------------------------------------

Invoca:

PromptService.get_prompt_by_id()


----------------------------------------
GET /prompts/{prompt_id}/versions
----------------------------------------

Invoca:

PromptService.list_versions()


----------------------------------------
GET /prompts/active
----------------------------------------

Invoca:

PromptService.list_active_prompts()


----------------------------------------
POST /prompts/{prompt_id}/compare
----------------------------------------

Invoca:

PromptService.compare_versions()


----------------------------------------
DELETE /prompts/{prompt_id}
----------------------------------------

Invoca:

PromptService.soft_delete_prompt()


----------------------------------------
GET /prompts/deleted
----------------------------------------

Invoca:

PromptService.list_deleted_prompts()


----------------------------------------
POST /prompts/{prompt_id}/recover
----------------------------------------

Invoca:

PromptService.recover_prompt()



main.py deve:

1. Criar instância do FastAPI
2. Inicializar dependências necessárias
3. Instanciar PromptService
4. Registrar router


Exemplo de inicialização esperada:

app = FastAPI()

app.include_router(prompt_router)


========================================
5. LIMITADORES
========================================

Restrições obrigatórias:

- Controllers NÃO devem usar NATS diretamente
- Controllers NÃO devem conter lógica de negócio
- Controllers apenas orquestram requisições HTTP
- DTOs devem ser importados da camada models
- Services devem ser importados da camada services
- Todos os endpoints devem ser async
- O router deve ser registrado em main.py
- Não duplicar lógica que já existe no PromptService
```

# Terceira Fase - Tratamentos de Exceçoes 

```
========================================
1. OBJETIVO DA FASE
========================================

Nesta fase final de desenvolvimento, o objetivo é implementar os utilitários de infraestrutura e o sistema de tratamento de exceções da aplicação.

As camadas anteriores já foram implementadas:

- models (DTOs)
- messaging (NATSPublisher)
- services (casos de uso)
- controllers (FastAPI endpoints)

Agora é necessário adicionar mecanismos de suporte que garantam:

- tratamento consistente de erros
- propagação correta de exceções entre camadas
- respostas HTTP amigáveis para os clientes da API
- utilitários reutilizáveis para serialização, validação e logging

Um ponto importante é que os serviços publicam eventos para NATS. Caso ocorra algum erro na publicação ou no fluxo interno do serviço, essas exceções precisam ser capturadas, padronizadas e transformadas em respostas HTTP compreensíveis para o cliente.

Fluxo esperado de erro:

Service / Messaging Exception
        ↓
Custom Exception
        ↓
FastAPI Exception Handler
        ↓
HTTP Response amigável


========================================
2. DEFINIR AS DIRETRIZES
========================================

Criar uma camada de utilitários responsável por:

- tratamento de exceções
- serialização
- helpers comuns
- logging

Estrutura sugerida:

utils/
    exceptions.py
    error_handlers.py
    json_utils.py
    logger.py

Regras arquiteturais:

1. Não lançar exceções genéricas como Exception diretamente.

2. Criar exceções específicas de domínio e infraestrutura.

3. Todas as exceções devem herdar de uma base comum:

BaseAppException

4. Exceções devem carregar:

- message
- error_code
- http_status
- optional details

5. Os controllers não devem tratar erros manualmente. O tratamento deve ser centralizado usando FastAPI Exception Handlers.

6. Exceções que ocorram na camada de messaging ou service devem ser convertidas para exceções da aplicação.

7. O sistema deve retornar respostas JSON padronizadas para erros.

Formato esperado da resposta de erro:

{
  "error": {
    "code": "PROMPT_NOT_FOUND",
    "message": "Prompt não encontrado",
    "details": {}
  }
}


========================================
3. SUGESTÕES DE DESENVOLVIMENTO
========================================

Criar uma classe base de exceção:

class BaseAppException(Exception):

    def __init__(
        self,
        message: str,
        error_code: str,
        http_status: int = 400,
        details: dict | None = None
    ):
        self.message = message
        self.error_code = error_code
        self.http_status = http_status
        self.details = details or {}

Exemplos de exceções específicas:

PromptNotFoundException

VersionNotFoundException

PromptAlreadyDeletedException

NATSPublishException

InvalidVersionComparisonException


Exemplo:

class PromptNotFoundException(BaseAppException):

    def __init__(self, prompt_id: str):
        super().__init__(
            message=f"Prompt {prompt_id} não encontrado",
            error_code="PROMPT_NOT_FOUND",
            http_status=404
        )


Implementar captura de erros no publisher:

Caso a publicação no NATS falhe, lançar:

NATSPublishException


Exemplo:

try:
    await self.nc.publish(subject, payload)
except Exception as e:
    raise NATSPublishException(str(e))


Criar handlers globais de exceção no FastAPI.

Arquivo:

utils/error_handlers.py


Handler esperado:

async def app_exception_handler(request, exc: BaseAppException):

    return JSONResponse(
        status_code=exc.http_status,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


Registrar os handlers no main.py:

app.add_exception_handler(BaseAppException, app_exception_handler)


Também adicionar fallback para exceções não tratadas:

async def generic_exception_handler(request, exc):

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Erro interno do servidor"
            }
        }
    )


========================================
4. RESULTADOS ESPERADOS
========================================

Ao final desta fase devem existir:

1. Camada utils criada
2. Sistema de exceções padronizado
3. Exceções específicas de domínio
4. Tratamento de exceções centralizado no FastAPI
5. Conversão automática de exceções para respostas HTTP
6. Proteção contra falhas na publicação NATS
7. Respostas de erro padronizadas em JSON


Exemplo de resposta de erro:

HTTP 404

{
  "error": {
    "code": "PROMPT_NOT_FOUND",
    "message": "Prompt 123 não encontrado",
    "details": {}
  }
}


Exemplo de erro interno:

HTTP 500

{
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "Erro interno do servidor"
  }
}


========================================
5. LIMITADORES
========================================

Restrições obrigatórias:

- Não lançar Exception genérica nas camadas services ou messaging
- Todas as exceções devem herdar de BaseAppException
- Controllers não devem capturar exceções manualmente
- O tratamento de exceções deve ser centralizado em handlers do FastAPI
- Mensagens retornadas ao cliente devem ser amigáveis
- Stack traces não devem ser expostos nas respostas HTTP
- Todos os erros devem retornar JSON padronizado
- A camada messaging deve capturar falhas de publicação NATS
- O sistema deve continuar compatível com as camadas já implementadas
```

## Testagem Unitária

```
========================================
1. OBJETIVO DA FASE
========================================
Criar testes unitários com pytest para os componentes já implementados do sistema:

- models
- messaging
- services
- controllers
- utils

Os testes devem validar o comportamento das unidades de forma isolada.

========================================
2. DIRETRIZES
========================================

Criar estrutura:

tests/
    services/
    messaging/
    controllers/
    utils/

Utilizar:

- pytest
- pytest-asyncio
- unittest.mock ou pytest-mock

Regras:

- Não usar NATS real
- Mockar NATSPublisher
- Testar unidades de forma isolada

========================================
3. ESCOPO DOS TESTES
========================================
Services:
Verificar se os métodos publicam os eventos corretos.

Messaging:
Testar NATSPublisher.publish mockando o cliente NATS.

Controllers:
Usar FastAPI TestClient e mockar PromptService.

Utils:
Testar exceções e handlers de erro.

========================================
4. RESULTADO ESPERADO
========================================

Testes unitários cobrindo:

- principais métodos dos services
- publicação de eventos no messaging
- endpoints dos controllers
- exceções e handlers

========================================
5. LIMITAÇÕES
========================================
- Não conectar em serviços externos
- Usar mocks para dependências externas
- Testes devem rodar com:
    pytest
```

# Modificacoes
- Outputs de Retorno
``` 
Objetivo
Adaptar o API Gateway para que, em respostas HTTP de sucesso (200 OK), ele retorne os objetos estruturados produzidos pelo Core Service em vez de retornar apenas uma string.

Contexto Atual
O API Gateway atualmente recebe respostas do serviço core (via evento ou chamada interna) e devolve apenas uma mensagem textual simples.

Novo Requisito
O Gateway deve mapear e devolver exatamente os outputs estruturados produzidos pelo Core Service.

Cada endpoint deve serializar e retornar o objeto de resposta correspondente ao evento executado.

Outputs disponíveis no Core

activate_version
Retorna:

PromptResponse(
    id=prompt.id,
    name=prompt.name.value,
    status=prompt.status.value,
    active_version_id=prompt.active_version_id,
    created_at=prompt.created_at,
    updated_at=prompt.updated_at,
)

add_version
Retorna:

PromptVersionResponse(
    id=version.id,
    prompt_id=version.prompt_id,
    version_number=version.version_number.value,
    content=version.content.value,
    created_at=version.created_at,
    is_active=version.is_active,
)

compare_versions
Retorna:

VersionDiffResponse(
    prompt_id=diff.prompt_id,
    version_id_before=diff.version_id_before,
    version_id_after=diff.version_id_after,
    version_number_before=diff.version_number_before,
    version_number_after=diff.version_number_after,
    lines=tuple(
        DiffLineResponse(
            kind=line.kind.value,
            content=line.content,
            line_number_before=line.line_number_before,
            line_number_after=line.line_number_after,
        )
        for line in diff.lines
    ),
    has_changes=diff.has_changes,
)

create_prompt
Retorna:

PromptResponse(
    id=prompt.id,
    name=prompt.name.value,
    status=prompt.status.value,
    active_version_id=prompt.active_version_id,
    created_at=prompt.created_at,
    updated_at=prompt.updated_at,
    content=version.content.value,
)

get_prompt_by_id
Retorna:

PromptDetailResponse(
    id=prompt.id,
    name=prompt.name.value,
    status=prompt.status.value,
    active_version_id=prompt.active_version_id,
    created_at=prompt.created_at,
    updated_at=prompt.updated_at,
    versions=versions,
)

list_active_prompts
Retorna lista de PromptResponse

list_deleted_prompts
Retorna lista de PromptResponse

list_versions
Retorna lista de PromptVersionResponse

recover_prompt
Retorna PromptResponse

soft_delete_prompt
Retorna PromptResponse

update_content
Retorna PromptVersionResponse

# Observacao importante

Os eventos retornam num wrapper:

ex:
class ApiWrapper(BaseModel):
    ok: bool
    data: PromptResponse

- adapte a serializacao para sempre buscar dentro de data a resposta
- crie um wrapper generico que possa ser adaptado a todos os outputs vindo dos eventos

Comportamento esperado no API Gateway

1. Para cada endpoint HTTP que execute uma ação no Core:
   - Receber o objeto retornado pelo Core
   - Acessar o wrapper
   - Serializar o objeto para JSON
   - Retornar como response body com status HTTP 200

2. Remover qualquer retorno textual genérico como:
   "success"
   "operation completed"
   ou similares.

3. O response HTTP deve refletir exatamente a estrutura dos DTOs retornados pelo Core.

Exemplo esperado

Antes:

HTTP 200

   "prompt created successfully"


Depois:

HTTP 200
{
  "id": "...",
  "name": "...",
  "status": "...",
  "active_version_id": "...",
  "created_at": "...",
  "updated_at": "...",
  "content": "..."
}

Requisitos de implementação

- Utilizar os DTOs de response retornados pelo Core como contrato da API.
- Garantir serialização correta de:
  - UUID
  - datetime
  - enums
- Preservar nomes de campos exatamente como definidos nos objetos.
- Para endpoints de listagem, retornar arrays JSON.

Boas práticas

- Não duplicar lógica de transformação de domínio no Gateway.
- Gateway apenas transporta e serializa os objetos retornados.
- Manter separação clara entre camada de transporte (HTTP) e domínio.
``` 