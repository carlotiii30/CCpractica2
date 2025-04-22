# Práctica 2 – Reconocimiento Facial con Functions-as-a-Service (OpenFaaS)

Repo en GitHub: https://github.com/carlotiii30/CCpractica2

Sistema operativo utilizado: MacOS

## Despliegue de la plataforma OpenFaaS sobre Kubernetes (Minikube)

Esta práctica tiene como objetivo desplegar una plataforma Functions-as-a-Service (FaaS) usando **OpenFaaS sobre Kubernetes** mediante **Minikube**, y posteriormente crear y probar funciones de reconocimiento facial.

---

### Instalación de herramientas necesarias:

```bash
brew install kubectl
brew install minikube
brew install helm
brew install faas-cli
```

---

### Paso 1: Iniciar Minikube

Se ha iniciado el clúster de Kubernetes local con Docker como driver:

```bash
minikube start --driver=docker --addons=default-storageclass,storage-provisioner --extra-config=apiserver.enable-admission-plugins=""
```

---

### Paso 2: Instalar OpenFaaS con Helm

#### 2.1. Añadir repositorio de OpenFaaS

```bash
helm repo add openfaas https://openfaas.github.io/faas-netes/
helm repo update
```

#### 2.2. Crear los namespaces necesarios

```bash
kubectl create namespace openfaas
kubectl create namespace openfaas-fn
```


#### 2.3. Desplegar OpenFaaS

```bash
helm upgrade openfaas openfaas/openfaas \
  --namespace openfaas \
  --set basic_auth=true \
  --set functionNamespace=openfaas-fn \
  --set generateBasicAuth=true \
  --install
```

---

### Paso 3: Acceder al portal de OpenFaaS

#### 3.1. Hacer port-forward al servicio gateway

```bash
kubectl port-forward -n openfaas svc/gateway 8080:8080
```

#### 3.2. Acceder desde el navegador

[OpenFaaS Portal](http://127.0.0.1:8080)

---

### Paso 4: Obtener credenciales de acceso

Usuario: ```admin```

Contraseña: ```Obtener a través del comando de abajo```
```bash
echo $(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode)
```

## Despliegue de funciones ya existentes desde el catálogo de OpenFaaS
Antes de implementar nuestra función propia, también se han desplegado dos funciones existentes del catálogo de OpenFaaS como parte del análisis comparativo que solicita la práctica.

### Paso 1: Comprobar que Minikube está iniciado y OpenFaaS funcionando
```bash
minikube start --driver=docker --addons=default-storageclass,storage-provisioner --extra-config=apiserver.enable-admission-plugins=""
kubectl port-forward -n openfaas svc/gateway 8080:8080
```

### Paso 2: Desplegar las funciones
```bash
faas-cli store deploy face-detect-opencv
faas-cli store deploy face-detect-pigo
```

### Paso 3: Probar las funciones
```bash
curl -X POST \
     --data "https://upload.wikimedia.org/wikipedia/commons/3/37/Dagestani_man_and_woman.jpg" \
     http://127.0.0.1:8080/function/face-detect-opencv \
     --output resultado_opencv.jpg
```
```bash
curl -X POST \
     --data "https://upload.wikimedia.org/wikipedia/commons/3/37/Dagestani_man_and_woman.jpg" \
     http://127.0.0.1:8080/function/face-detect-pigo \
     --output resultado_pigo.jpg
```

## Despliegue de función de reconocimiento facial (Faces Detection)

### Paso 1: Entorno de ejecución

Se ha utilizado la plantilla oficial de OpenFaaS python3-flask-debian, que permite trabajar con dependencias como OpenCV, Flask y Numpy de forma sencilla y sin necesidad de definir un Dockerfile personalizado.

Esta plantilla proporciona una base Debian con soporte para Flask, ideal para funciones que necesitan devolver imágenes procesadas.

### Paso 2: Autenticarse para subir y desplegar funciones

#### 2.1. Hacer login en Docker.

```bash
docker login
```

#### 2.2. Hacer login en OpenFaaS

```bash
faas-cli login --gateway http://127.0.0.1:8080 --password $(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode)
```

### Paso 3: Construir, subir y desplegar la función

```bash
faas-cli up -f stack.yaml
```

### Paso 4: Acceder a la función

Desde [OpenFaaS Portal](http://127.0.0.1:8080) podemos ejecutar la función.


### Detalles de la implementación

La función ha sido implementada en Python utilizando la plantilla oficial python3-flask-debian de OpenFaaS. Utiliza OpenCV para detectar rostros en una imagen recibida mediante una URL.

**Mejoras respecto a funciones básicas**:

- Uso de Flask y Response: La función utiliza la respuesta nativa de Flask (flask.Response) para retornar directamente la imagen procesada como contenido binario (image/jpeg), en lugar de serializar los bytes como texto o base64, lo cual simplifica el consumo desde el cliente y mejora el rendimiento.

- Control de errores robusto: En caso de error (por ejemplo, si la URL no es válida o la imagen no puede descargarse/procesarse), se devuelve un mensaje con el código de error 500, incluyendo el motivo exacto del fallo. Esto mejora la trazabilidad frente a funciones que solo devuelven None o errores genéricos.

- Registro de la URL recibida: Se incluye un print() que muestra en logs qué URL se está procesando. Esto ha sido útil durante las pruebas para depurar errores.


### Testear la función

Test:

```bash
python3 facesdetection-python/handler_test.py
```

Probar desde terminal:
```bash
curl -X POST http://127.0.0.1:8080/function/facesdetection-python \
     -H "Content-Type: text/plain" \
     --data "https://upload.wikimedia.org/wikipedia/commons/3/37/Dagestani_man_and_woman.jpg" \
     --output resultado.jpg
```