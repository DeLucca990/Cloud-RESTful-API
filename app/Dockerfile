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
