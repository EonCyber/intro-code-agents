# Prompt Versioning Front End

- Tech Stack Utilizada
- Paleta de Cores (opcional)
- Fontes (opcional)
- Integrações (APIs, DB, GraphQL, Etc)
- Detalhes de componentes (Layout)
- Limitadores
- Objetivos esperados (qualidade)

# Primeira Etapa - Bootstraping e Componentização Inicial

``` 
Vamos gerar uma Aplicação para gerenciamento de prompts.

STACK

Utilize a seguinte stack:

- React + Vite
- TailwindCSS
- Axios para comunicação com a API


OBJETIVO DA APLICAÇÃO

Construir um dashboard que permita visualizar e gerenciar prompts e suas versões utilizando um backend exposto através de um API Gateway.

A tela principal deve exibir uma lista de prompts em formato de cards.

INTEGRAÇÃO COM API

Foi fornecido um arquivo de especificação da API no formato **Swagger / OpenAPI**.

Utilize essa especificação como fonte de verdade para:

- identificar os endpoints disponíveis
- estruturar as chamadas HTTP
- definir os payloads e respostas

A integração com o backend deve ser criada a partir dessa especificação.

Criar uma pequena camada de serviços utilizando Axios para encapsular as chamadas da API.

LAYOUT PRINCIPAL

A página principal deve conter:

- Um grid responsivo de cards
- Cards representando cada prompt existente
- Um botão flutuante "+" para adicionar novos prompts
- Interface limpa e responsiva usando TailwindCSS
- Um background geometrico

LISTA DE PROMPTS

- Deve ser uma lista centralizada
- De visualizacao vertical
- Com um input de busca (filtra a lista de prompts pelo nome)

CARDS DE PROMPT

Cada prompt deve ser exibido em um card contendo:

- Nome do prompt
- Indicação da versão ativa
- (Opcional) pequeno preview do conteúdo da versão ativa

Cada card deve possuir três ícones de ação:

1. Ícone de Timeline  
   - Levará para uma tela de linha do tempo do prompt  (nao criar o componente de timeline nessa iteração)

2. Ícone de Comparação  
   - Será usado para levar para um componente de seleção de versoes para comparacao (não criar componente nessa iteração)

3. Ícone de Detalhes  
   - Abre um modal com os detalhes completos do prompt  
   - Exibe conteúdo da versão ativa
   - Deve ter um botão para copiar o conteudo para a area de transferencia
   - Deve ter um botao de edicao que habilitar editar e salvar o conteudo (gerando uma nova versao)


BOTÃO FLUTUANTE DE CRIAÇÃO

Na lateral inferior da tela deve existir um botão flutuante "+".

Ao clicar neste botão deve abrir um modal com um formulário para criação de um novo prompt.


FORMULÁRIO DE CRIAÇÃO DE PROMPT

O formulário deve conter:

- Campo de input para "Nome"
- Campo de textarea para "Conteúdo"

Botões do formulário:

- Criar Prompt
- Cancelar

Ao submeter o formulário, deve ser feita uma chamada HTTP usando Axios para criar o prompt no backend.

E atualizar a lista dos prompts com um novo prompt.


LIMITADORES

- NÃO utilizar Supabase
- NÃO criar ou utilizar banco de dados local
- NÃO utilizar Firebase ou qualquer backend externo
- NÃO persistir dados localmente
- Todos os dados da aplicação devem vir exclusivamente da API fornecida
- Todas as operações (listar, criar, comparar, visualizar versões) devem utilizar chamadas HTTP via Axios
- criar APENAS os componentes explicitos nesse prompt


EXPERIÊNCIA DE USUÁRIO

A interface deve ser:

- Limpa
- Responsiva
- Conter Toasters de sucesso ou erros
- Ter opcoes de Dark Mode e Light Mode

CRITERIOS DE SUCESSO:
- A aplicacao se comunica com a api usando os endpoints corretos
- É funcional, responsiva, pronta para uso
- Utiliza dados reais da api e não mocados
- Implementa uma interface moderna
``` 

# Segunda Etapa - Componente de Comparacao de Prompts


```
Crie um componente de comparação de versões de prompts.

OBJETIVO

Criar uma interface semelhante à comparação de commits do GitHub, onde o usuário pode visualizar diferenças entre duas versões de um prompt.


FUNCIONALIDADE

O usuário deve conseguir:

1. Selecionar um prompt
2. Selecionar duas versões para comparação:
   - versão base (before)
   - versão comparada (after)

3. Visualizar a diferença entre os conteúdos
4. Acessar a funcionalidade a partir do card do prompt ou de um botão no navbar

API

Utilizar o endpoint de comparaçao ja configurado na aplicacao.

INTERFACE DE COMPARAÇÃO

Criar um componente visual inspirado no GitHub diff:

- Layout lado a lado (split view) OU inline (linha a linha)
- Mostrar claramente:

  - Adições → destaque em VERDE
  - Remoções → destaque em VERMELHO
  - Texto inalterado → padrão

Cada linha deve indicar:

- Conteúdo antigo vs novo
- Destaques visuais claros


REGRAS DE UI

- Fonte monoespaçada para o diff
- Scroll horizontal se necessário
- Destaque visual suave (não agressivo)

Sugestão de cores:

- Verde claro para adições
- Vermelho claro para remoções


COMPONENTES

Criar:

- VersionSelector (seleção de versões)
- DiffViewer (renderização do diff)
- ComparePage


EXPERIÊNCIA DO USUÁRIO

- Fácil seleção de versões
- Feedback visual imediato
- Loading state durante requisição
- Tratamento de erro caso comparação falhe


LIMITAÇÕES

- Não usar bibliotecas externas de diff pesadas (implementar versão simples ou leve)
- Não persistir dados localmente
- Sempre buscar dados da API
- Não usar banco de dados ou serviços externos


RESULTADO ESPERADO

Um componente funcional que:

- Permite selecionar duas versões
- Chama a API corretamente
- Renderiza um diff visual semelhante ao GitHub
- Mostra claramente o que mudou entre versões
- Temos dois prompts mockados, crie dua versoes desses mocks para poder testar visualmente.
```

## Terceira etapa - Linha do Tempo

```
Crie um componente de linha do tempo (timeline) para visualizar a evolução das versões de um prompt.

OBJETIVO

Exibir todas as versões de um prompt em ordem cronológica, inspirado em interfaces de Git (GitHub / Bitbucket).


FUNCIONALIDADE

- Listar versões de um prompt ao longo do tempo
- Cada item da timeline deve mostrar:
  - número da versão
  - data de criação
  - resumo do conteúdo
- Permitir clicar em uma versão para ver detalhes
- Permitir ação rápida para comparar com outra versão


INTEGRAÇÃO COM API

Usar o endpoint de get versions ja configurado na aplicacao


INTERFACE

- Layout vertical (timeline)
- Cada versão como um “node” conectado por uma linha
- Destaque visual para versão ativa
- Estilo inspirado em histórico de commits


UX

- Scroll vertical
- Loading state
- Feedback em caso de erro


LIMITAÇÕES

- Não usar banco de dados local
- Não usar serviços externos
- Todos os dados devem vir da API
```