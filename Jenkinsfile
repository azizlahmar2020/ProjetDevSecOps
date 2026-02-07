pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        VENV_NAME = "venv"
        // Pas de commentaire ici, ou utilise /* ... */
        scannerHome = tool('SonarQube Scanner')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo '✅ Code récupéré'
            }
        }

        stage('Build Python App') {
            steps {
                echo '🐍 Building Application Logic...'

                sh '''#!/bin/bash
                set -e

                echo "🧹 Nettoyage ancien venv"
                rm -rf venv

                echo "🐍 Version Python"
                python3 --version

                echo "📦 Création du virtualenv"
                python3 -m venv venv

                echo "⬆️ Upgrade pip"
                ./venv/bin/pip install --upgrade pip

                echo "📚 Installation dépendances"
                ./venv/bin/pip install -r requirements.txt

                echo "🔍 Vérification du code Python"
                ./venv/bin/python -m py_compile app.py
                '''
            }
        }

        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('SonarQube Server') {
                    sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=mon-projet -Dsonar.sources=."
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Build Docker image'
                sh 'docker build -t my-python-app:latest .'
            }
        }

        stage('Load Image Into Kind') {
            steps {
                echo '📦 Load image into kind'
                sh 'kind load docker-image my-python-app:latest --name kind'
            }
        }

        stage('Deploy Helm Chart To kind') {
            steps {
                sh '''
                export PATH=$PATH:/snap/bin
                export KUBECONFIG=/var/lib/jenkins/kubeconfig-kind
                echo "🌐 Vérification des nodes du cluster"
                kubectl get nodes
                echo "🚀 Déploiement Helm Chart"
                helm upgrade -i python-app ./python-app-helm
                '''
            }
        }

    } // fermeture stages

    post {
        success {
            echo '✅ Pipeline terminé avec succès'
        }
        failure {
            echo '❌ Échec du pipeline'
        }
        always {
            echo '🏁 Fin du pipeline'
        }
    }

} // fermeture pipeline
