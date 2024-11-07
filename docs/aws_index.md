# Deploy na AWS
## Exemplo da aplicação:
A aplicação está disponível no seguinte link: [Api App](http://a9081d685efb34ba0bd6b6340780caa3-1034918237.us-east-2.elb.amazonaws.com/)

<div class="warning" markdown>
!!! Warning
    A aplicação está hospedada em um ambiente de teste e pode ser desativada a qualquer momento.
</div>

<div class="info" markdown>
!!! Info
    Siga o passo a passo [aqui](local_index.md) para saber como utilizar a aplicação.
</div>

## Passo a passo para o deploy:
Para realizar o deploy da aplicação na AWS, siga os passos abaixo:

1. Criar cluster EKS:
```bash
eksctl create cluster --name cloud-project-cluster --region us-east-2 --nodes 2
```

2. Configurar o kubectl:
```bash
aws eks --region us-east-2 update-kubeconfig --name cloud-project-cluster
```

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

5. Aplicar os arquivos no cluster:
```bash
kubectl apply -f app-deployment.yml
kubectl apply -f app-service.yml
```

6. Acessar a aplicação:
```bash
kubectl get svc fastapi-service
```