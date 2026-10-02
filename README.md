# k8s-minikube-demo

## Запуск

```sh
minikube start --driver=docker
docker build -t my-app:1.0 .
minikube image load my-app:1.0
kubectl apply -f k8s/
kubectl port-forward service/my-app 8080:80
```

Приложение: <http://localhost:8080>
