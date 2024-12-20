# FastAPI Starter

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Este é um projeto de inicialização para aplicações FastAPI com suporte a Docker e Docker Compose. Abaixo estão as etapas para rodar o projeto facilmente com Docker.

## Requirements

Para rodar este projeto, você precisará dos seguintes requisitos:

- **Python (3.10.\*)**: [Instalar Python](https://www.python.org/downloads/)
- **docker-compose**: [Instalar docker-compose](https://docs.docker.com/compose/install/)
- **Docker**: [Instalar Docker](https://docs.docker.com/desktop/mac/install/)

No entanto, **a maneira mais fácil de rodar este projeto é usando Docker**, que já contém todas as dependências e configurações necessárias.

## Como rodar

Para rodar a aplicação usando Docker, siga estas etapas:

1. **Clone o repositório para o diretório de sua escolha**:
   ```bash
   git clone https://github.com/INXE-Lainf-Labs/obd-trace-backend.git

2. **Renomeie o arquivo de exemplo de variáveis de ambiente**:
    ```bash
    O arquivo src/config/.env.example contém variáveis de ambiente padrão. Renomeie-o para .env para configurar o ambiente da aplicação.

3. **Suba os containers Docker**:

    Abra um terminal na pasta raiz do projeto e execute o comando abaixo. Ele irá subir os containers necessários para a aplicação.
    ```bash
    make docker-up
    ```
    O comando acima usará o docker-compose para configurar o ambiente completo, incluindo o backend e o banco de dados.

## Comandos úteis

1. **Subir os containers Docker**:

    Subir o Docker container principal:
    ```bash
    make docker-up
    ```
    Subir apenas o banco de dados em Docker:
    ```bash
    make docker-up-db
    ```

2. **Parar e limpar containers e imagens Docker**:

    Parar os containers e remover imagens e volumes:
    ```bash
    make docker-prune
    ```

3. **Reiniciar os containers Docker**:

    Limpa e sobe os containers novamente:
    ```bash
    make docker-reload
    ```

4. **Rodar testes da aplicação**:

    Instalar as dependências de testes:
    ```bash
    make test
    ```

5. **Verificar erros de lint**:

    Verificar se o código está de acordo com as PEPs:
    ```bash
    make lint
    ```

6. **Corrigir erros de lint automaticamente**:

    Ajusta o código para seguir o style guide da PEP-8:
    ```bash
    make lint-fix
    ```

7. **Instalar o virtualenv**:

    Caso queira rodar o projeto em um ambiente local sem Docker, você pode usar virtualenv. Para isso, execute o seguinte comando:
    ```bash
    python3 -m venv .venv
    ```

8. **Instalar os requirements**:

    Após configurar o ambiente virtual, instale as dependências do projeto com o comando:
    ```bash
    pip install -r requirements.txt
    ```



9. **Instalar o formatador de código Black no seu ambiente**:

    Para instalar o Black para formatar o código no seu ambiente local, execute:
    ```bash
    make install-code-formatter
    ```

## Documentation

O FastAPI gera automaticamente uma documentação interativa de todas as nossas rotas e modelos. Você pode acessá-la diretamente no seu navegador em http://localhost:8000/docs.