# Práctica 2 – Reconocimiento Facial con Functions-as-a-Service (OpenFaaS)

Sistema operativo utilizado: MacOS

## Despliegue de la plataforma OpenFaaS sobre Kubernetes (Minikube)

Esta práctica tiene como objetivo desplegar una plataforma Functions-as-a-Service (FaaS) usando **OpenFaaS sobre Kubernetes** mediante **Minikube**, y posteriormente crear y probar funciones de reconocimiento facial.

---

## Instalación de herramientas necesarias:

```bash
brew install kubectl
brew install minikube
brew install helm
brew install faas-cli
```

---

## Paso 1: Iniciar Minikube

Se ha iniciado el clúster de Kubernetes local con Docker como driver:

```bash
minikube start --driver=docker
```

---

## Paso 2: Instalar OpenFaaS con Helm

### 2.1. Añadir repositorio de OpenFaaS

```bash
helm repo add openfaas https://openfaas.github.io/faas-netes/
helm repo update
```

### 2.2. Crear los namespaces necesarios

```bash
kubectl create namespace openfaas
kubectl create namespace openfaas-fn
```


### 2.3. Desplegar OpenFaaS

```bash
helm upgrade openfaas openfaas/openfaas \
  --namespace openfaas \
  --set basic_auth=true \
  --set functionNamespace=openfaas-fn \
  --set generateBasicAuth=true \
  --install
```

---

## Paso 3: Acceder al portal de OpenFaaS

### 3.1. Hacer port-forward al servicio gateway

```bash
kubectl port-forward -n openfaas svc/gateway 8080:8080
```

### 3.2. Acceder desde el navegador

[OpenFaaS Portal](http://127.0.0.1:8080)

---

## Paso 4: Obtener credenciales de acceso

Usuario: ```admin```

Contraseña: ```Obtener a través del comando de abajo```
```bash
echo $(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode)
```
