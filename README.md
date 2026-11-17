# CommitAI

Gerador de mensagens de commit no padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/) usando IA. Você descreve o que mudou no código, e o CommitAI devolve a mensagem pronta.

```text
Descrição: resolvi um problema na validação das senhas de usuários
fix(auth): corrige validação de senhas de usuários
```

## Funcionalidades

- Recebe uma descrição em texto livre pelo terminal
- Envia a solicitação ao Gemini (Google) por meio da Interactions API
- Valida a resposta com Pydantic antes de exibir
- Gera `type`, `scope`, `description`, `body` e `breaking`
- Configuração (modelo, limite de tokens, nível de raciocínio) feita no `.env`, sem alterar o código

## Requisitos

- Python 3.13+
- [Poetry](https://python-poetry.org/)
- Uma chave de API do Gemini, gerada no [Google AI Studio](https://aistudio.google.com/)

## Instalação

```bash
git clone <url-do-repositorio>
cd <pasta-do-projeto>
poetry install
```

## Configuração

Copie o arquivo de exemplo e preencha:

```bash
# Linux/Mac
cp .env.example .env

# Windows
copy .env.example .env
```

| Variável | Descrição | Exemplo |
|---|---|---|
| `GOOGLE_API_KEY` | Chave da API (obrigatória) | `sua-chave` |
| `GOOGLE_MODELO` | Modelo do Gemini | `gemini-2.5-flash` |
| `GOOGLE_MAX_TOKENS` | Limite de tokens da resposta | `1000` |
| `GOOGLE_THINKING_LEVEL` | Nível de raciocínio (`low`, `medium`, `high`) | `low` |

> Nunca faça commit do `.env`. Ele já deve estar no `.gitignore`.

## Uso

```bash
poetry run poe exec
```

O programa pede a descrição e imprime a mensagem de commit:

```text
Bem-vindo ao CommitAI
Descreva as mudanças que você realizou no código para que o commit seja gerado
Descrição: criei um endpoint para listar os livros com paginação
feat(livros): adiciona endpoint de listagem com paginação
```

## Como funciona

1. **Entrada:** o usuário descreve a mudança no terminal.
2. **Solicitação:** a descrição é enviada ao modelo junto com um prompt de sistema que define as regras do Conventional Commits.
3. **Resposta estruturada:** o modelo devolve um JSON seguindo o esquema `CommitSchema`.
4. **Validação:** o JSON é validado com Pydantic (tipos permitidos, tamanho máximo da descrição).
5. **Apresentação:** a mensagem final é montada e exibida.

## Estrutura do projeto

```text
commitAI/
└── src/
    ├── core.py      # fluxo principal
    ├── schemas.py   # CommitSchema (Pydantic)
    └── ...          # prompt e configuração
pyproject.toml
.env.example
```

## Privacidade

O texto que você digita é enviado à API do Gemini (Google). Evite incluir senhas, chaves ou código sensível na descrição. A chamada usa `store=False` para não guardar a interação para consulta posterior.

## Limitações

- O modelo só conhece o que você escreveu. Descrições vagas ("mexi em umas coisas") geram mensagens genéricas.
- O escopo (`scope`) pode ser um palpite quando a descrição não diz onde a mudança ocorreu.
- Descrições com mais de um assunto podem virar um único commit. Nesses casos, considere dividir em commits menores.
- A mensagem é uma sugestão: revise antes de usar.

## Testes manuais

| Entrada | Resultado |
|---|---|
| resolvi um problema na validação das senhas de usuários | `fix(auth): corrige validação de senhas de usuários` |
| eu alterei o tempo do token e criei um path de refresh | `feat(auth): adiciona refresh token e altera tempo de expiracao` |
| mexi em umas coisas | `chore: atualiza arquivos do projeto` (mensagem genérica, ponto a melhorar) |


