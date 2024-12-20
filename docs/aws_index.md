# Deploy na AWS
## Exemplo da aplicação:
A aplicação está disponível no seguinte link: [Api App](http://a9081d685efb34ba0bd6b6340780caa3-1034918237.us-east-2.elb.amazonaws.com/)

<div class="warning" markdown>
!!! Warning "Aviso"
    A aplicação está hospedada em um ambiente de teste e pode ser desativada a qualquer momento.
</div>

<div class="info" markdown>
!!! Info "Instruções"
    Siga o passo a passo [aqui](local_index.md/#como-usar) para saber como utilizar a aplicação.
</div>

## Pré-requisitos:
- Conta na AWS
- AWS CLI
- EKSCTL

<div class="info" markdown>
??? info "Realizar o deploy por meio do CLI local"
    Caso você não tenha o AWS CLI e o EKSCTL instalados na sua máquina, siga os passos abaixo:
    Caso não tenha o AWS CLI instalado, siga o passo a passo [aqui](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/install-cliv2.html).

    Caso você não tenha o EKSCTL instalado, siga o passo a passo [aqui](https://eksctl.io/installation/).
</div>
<div class="info" markdown>
??? info "Realizar o deploy por meio do CloudShell"
    Para realizar o deploy por meio do CloudShell, acesse o console da AWS e procure por `CloudShell` no canto superior direito.
    Caso queira saber mais sobre o AWS CloudShell [acesse](https://docs.aws.amazon.com/pt_br/cloudshell/latest/userguide/welcome.html).

    Instale o [EKSCTL](https://eksctl.io/installation/). Sabemos que o CloudShell roda uma versão do Linux, então siga o passo a passo para instalar o EKSCTL em base Unix.
    Após isso, siga as instruções para deploy abaixo.
</div>

<div class="info" markdown>
??? tip "Dica Amiga"
    Utilize o CloudShell para realizar o deploy, pois ele é mais simples de instalar os pacotes.
</div>
## Passo a passo para o deploy:
Para realizar o deploy da aplicação na AWS, siga os passos abaixo:

1. Criar cluster EKS:
```bash
eksctl create cluster --name cloud-project-cluster --region us-east-2 --nodes 2
```
    - `--name` é o nome do cluster a ser criado.
    - `--region` é a região onde o cluster será criado, no nosso caso, us-east-2 (Ohio).
    - `--nodes` é a quantidade de nós que o cluster terá, 2 pois é como o mestre mandou.

2. Configurar o kubectl:
```bash
aws eks --region us-east-2 update-kubeconfig --name cloud-project-cluster
```
    - `--region` é a região onde o cluster foi criado.
    - `--update kubeconfig` é o comando para atualizar o arquivo de configuração do kubectl.
    - `--name` é o nome do cluster criado.

3. Criar arquivo app `app-deployment.yml`:
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
        - name: fastapi
          image: pedrodl/cloud_project1:latest
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              value: "postgresql://postgres:postgres@postgres:5432/ProjetoCloud"
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8000
  selector:
    app: fastapi
```
    - Faça as devidas modificações caso julgue necessário, contudo, o arquivo acima já está configurado para a aplicação. A única
    modificação obrigatória é a variável `image` que deve ser alterada para a sua imagem do Docker Hub.
4. Criar arquivo db `db-deployment.yml`:
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-db-cloud
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_USER
              value: "postgres"
            - name: POSTGRES_PASSWORD
              value: "postgres"
            - name: POSTGRES_DB
              value: "ProjetoCloud"
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  ports:
    - port: 5432
  selector:
    app: postgres
```

5. Aplicar os arquivos no cluster _(rode os comandos abaixo na pasta onde os arquivos `.yml` estão)_:
```bash
kubectl apply -f app-deployment.yml
kubectl apply -f db-deployment.yml
```

6. Acessar a aplicação:
```bash
kubectl get svc fastapi-service
```

## Vídeo demonstrativo

<div style="border: 1px solid #0540e3; padding: 3px; width: fit-content; margin: auto;">
    <iframe 
        width="670" 
        height="380" 
        src="https://www.youtube.com/embed/dqEOfnO3vWc" 
        title="Vídeo demonstrativo" 
        frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>