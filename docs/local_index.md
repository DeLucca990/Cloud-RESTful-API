# API REST com FastAPI e PostgreSQL

## Visão Geral
Esta API permite que os usuários realizem o registro, login e consultem dados sobre a probabilidade de origem de um nome, indicando qual país a pessoa pode ter nascido com base no nome fornecido. A API é construída usando FastAPI e PostgreSQL, e é executada em containers Docker.

## Tecnologias
- FastAPI
- PostgreSQL
- Docker
- Docker Compose

## Links úteis
- [Repositório no Docker Hub](https://hub.docker.com/repository/docker/pedrodl/cloud_project1/general)
- [Repositório no Github](https://github.com/DeLucca990/Cloud-RESTful-API)

## Endpoints
- **POST /register**: Registra um novo usuário
- **POST /login**: Realiza o login do usuário
- **GET /consultar**: Retorna a probabilidade de origem de um nome

## Instalação
Baixe o arquivo `compose.yml`:

<a href="https://raw.githubusercontent.com/DeLucca990/Cloud-RESTful-API/main/app/compose.yml" id="downloadLink">Compose.yml</a>

<script>
document.getElementById('downloadLink').addEventListener('click', function(event) {
    event.preventDefault();
    const url = this.href;
    const fileName = 'compose.yml';

    fetch(url)
    .then(response => response.blob())
    .then(blob => {
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = fileName;
        link.click();
    })
    .catch(() => alert('Falha ao baixar o arquivo.'));
});
</script>

## Como usar

1. Acesse a documentação da API em:

    Você irá utilizar o Swagger (nativo do FastAPI) para testar a API. Para isso, siga os passos abaixo:
    ```bash
    http://localhost:8000
    ```

2. Crie um novo usuário acessando o endpoint **POST /register** e informando os dados necessários;
    
    Para essa etapa você precisa informar os seguintes dados no formato JSON:
    ```json
    {
        "nome": "seu_nome",
        "email": "seu_email",
        "senha": "sua_senha"
    }
    ```
    Se o usuário for criado com sucesso, você receberá uma mensagem de confirmação com um token JWT no seguinte formato:
    ```json
    {
        "jwt": "seu_token"
    }
    ```
    Copie o token gerado

3. _(Opcional caso você tenha acabado de realizar o cadastro)_ Acesse o endpoint **POST /login** e informe o email e senha cadastrados no passo anterior;
    
    Para essa etapa você precisa informar os seguintes dados no formato JSON:
    ```json
    {
        "email": "seu_email",
        "senha": "sua_senha"
    }
    ```
    Se o login for realizado com sucesso, você receberá uma mensagem de confirmação com um token JWT no seguinte formato:
    ```json
    {
        "jwt": "seu_token"
    }
    ```
    Copie o token gerado

4. Acesse o endpoint **GET /consultar** e informe o nome que deseja consultar a origem;

    Para essa etapa você precisa informar o nome que deseja consultar e o token JWT gerado no passo anterior;
    
    Para adicionar o token JWT, clique no cadeado onde está escrito Authorize no canto superior direito da página do Swagger e cole o token no campo "Value" e clique em "Authorize";

    Em seguida, informe o nome que deseja consultar no campo "nome" e clique em "Execute";

    Exemplo: Para o nome _Ventura_ você receberá a seguinte resposta:
    ```json
    {
    "count": 93808,
    "name": "Ventura",
    "country": [
        {
        "country_id": "Guatemala",
        "probability": 0.0778645843473412
        },
        {
        "country_id": "Dominican Republic",
        "probability": 0.06733259445061568
        },
        {
        "country_id": "Portugal",
        "probability": 0.06602045473537535
        },
        {
        "country_id": "El Salvador",
        "probability": 0.04476210258091573
        },
        {
        "country_id": "United States",
        "probability": 0.04369474023158603
        }
    ]
    }
    ```

5. Para finalizar, execute o comando abaixo (em outro terminal) para parar os containers::
    ```bash
    docker compose down
    ```
<div class="result" markdown>
!!! tip
    O token JWT gerado é válido por 30 minutos. Após esse tempo, você precisará realizar o login novamente para obter um novo token.
</div>

## Vídeo demonstrativo

<div style="border: 1px solid #0540e3; padding: 3px; width: fit-content; margin: auto;">
    <video controls>
        <source src="../video/demosntracao_cloud.mp4" type="video/mp4">
    </video>
</div>

## Referências
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Swagger](https://swagger.io/)