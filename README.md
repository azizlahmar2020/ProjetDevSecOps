# Projet Python DevOps Monolithique (Docker + Kind)

Application web Flask + MySQL avec pipeline CI/CD Jenkins déployant sur Kubernetes (Kind).

## Structure
- `app.py`: Backend Flask
- `templates/`: Frontend HTML
- `Dockerfile`: Configuration de l'image Docker
- `k8s/`: Manifestes Kubernetes
- `Jenkinsfile`: Pipeline CI/CD

## Prérequis
- Docker
- Kind (Kubernetes in Docker)
- Jenkins (avec accès à Docker et Kubectl)

## Installation Locale (Sans Docker)
Voir instructions précédentes ou utiliser `python app.py`.

## Deploiement via Jenkins
Le pipeline effectue les étapes suivantes :
1. **Checkout**: Récupère le code.
2. **Build Python**: Installe dépendances et vérifie la syntaxe.
3. **Build Docker Image**: Construit `my-python-app:latest`.
4. **Load Image**: Charge l'image dans le cluster Kind (`kind load`).
5. **Deploy**: Applique les manifestes Kubernetes (`kubectl apply`).

## Accès à l'application (Kind)
Une fois déployé :
```bash
kubectl get services
```
Si vous utilisez `NodePort` (par défaut), vous devrez peut-être faire un port-forwarding pour accéder depuis host :
```bash
kubectl port-forward service/python-app-service 8080:80
```
Accédez ensuite à `http://localhost:8080`.

## Base de Données dans K8s
Ce projet assume qu'un service MySQL est accessible via le nom d'hôte `mysql-service`.
Vous devez déployer MySQL dans votre cluster Kind séparément ou ajouter un manifeste pour MySQL dans `k8s/`.
