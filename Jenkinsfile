pipeline {
    agent any

    environment {
        VENV_NAME = "venv"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo 'Code récupéré depuis le repository'
            }
        }

        stage('Build Python App') {
            steps {
                echo 'Building Application Logic...'

                sh '''#!/bin/bash
                set -e

                echo "Nettoyage ancien venv..."
                rm -rf venv

                echo "Version Python :"
                python3 --version

                echo "Création du venv..."
                python3 -m venv venv

                echo "Activation du venv..."
                source venv/bin/activate

                echo "Installation des dépendances..."
                pip install --upgrade pip
                pip install -r requirements.txt

                echo "Vérification du code Python..."
                python -m py_compile app.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-python-app:latest .'
            }
        }

        stage('Load Image Into Kind') {
            steps {
                sh 'kind load docker-image my-python-app:latest --name kind'
            }
        }

        stage('Deploy to Kind') {
            steps {
                sh '''
                kubectl apply -f k8s/
                kubectl rollout restart deployment/python-app-deployment
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé.'
        }
        success {
            echo 'Succès du build !'
        }
        failure {
            echo 'Échec du build.'
        }
    }
}
