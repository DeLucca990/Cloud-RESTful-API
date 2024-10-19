# Técnicas utilizadas para criação do container Docker

## Geração do container
Para a geração do container Docker, foi utilizado o arquivo Dockerfile, que contém as instruções necessárias para a criação da imagem e o arquivo docker-compose.yml, que contém as configurações necessárias para a execução do container.

<div class="warning" markdown>
!!! warning
    Os arquivos Dockerfile e docker-compose.yml devem estar presentes na raiz do projeto. Neste caso, está presente na pasta `app`. Execute o comando `cd app` para acessar a pasta do projeto.
</div>

Exemplo do `Dockerfile:`

```dockerfile
# Usar a imagem oficial do Python como base
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo requirements.txt para instalar as dependências
COPY requirements.txt .

# Instalar as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o conteúdo da aplicação para o diretório de trabalho
COPY . .

# Expor a porta onde a aplicação estará rodando
EXPOSE 8000

# Comando para iniciar a aplicação FastAPI usando o Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Exemplo do `docker-compose.yml:`

```yaml
name: cloud_project1

services:
  app:
    image: pedrodl/cloud_project1:latest
    container_name: fast_api_cloud
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/ProjetoCloud
    depends_on:
      - db
    volumes:
      - .:/app
  
  db:
    image: postgres
    container_name: postgres_db_cloud
    environment:
      - POSTGRES_USER=${POSTGRES_USER:-postgres}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
      - POSTGRES_DB=${POSTGRES_DB:-ProjetoCloud}
    # Expondo na porta 5430 para não conflitar com o postgres local
    ports:
      - "5430:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
volumes:
  postgres_data:
```

## Build da imagem
Para construir a imagem Docker, é necessário executar o comando `docker build -t <nome_da_imagem> .` no terminal, dentro da pasta `app` do projeto. O comando `docker build` cria a imagem Docker com base no Dockerfile presente no diretório atual e o parâmetro `-t` define o nome da imagem.

Exemplo de construção da imagem Docker:

```bash
docker build -t pedrodl/cloud_project1:latest .
```

## Build da imagem em ambas as arquiteturas (x86 e ARM)
Para construir a imagem Docker em ambas as arquiteturas (x86 e ARM), é necessário utilizar o comando `docker buildx build --platform linux/amd64,linux/arm64 -t <nome_da_imagem> .` no terminal, dentro da pasta `app` do projeto. O comando `docker buildx build` cria a imagem Docker com base no Dockerfile presente no diretório atual e o parâmetro `--platform` define as arquiteturas em que a imagem será construída.

Exemplo de construção da imagem Docker em ambas as arquiteturas:

```bash
# Ativar o buildx
docker buildx create --use

# Construir a imagem em ambas as arquiteturas
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

docker buildx build --platform linux/amd64,linux/arm64 -t pedrodl/cloud_project1:latest .
```

## Publicação da imagem no Docker Hub
Para publicar a imagem no Docker Hub, é necessário criar uma conta no site [Docker Hub](https://hub.docker.com/). Após criar a conta, é necessário logar no Docker Hub no terminal com o comando `docker login`. Após logar, é possível publicar a imagem no Docker Hub com o comando `docker push <nome_da_imagem>`.

Exemplo de publicação da imagem no Docker Hub:

```bash
docker push pedrodl/cloud_project1:latest
```

## Referências
- [Docker](https://www.docker.com/)
- [Docker Multi-Architecture Builds](https://docs.docker.com/build/building/multi-platform/)