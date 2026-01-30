pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        VENV_NAME = "venv"
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

                echo "📂 Vérification venv"
                ls -l venv/bin

                echo "⚡ Activation venv"
                source venv/bin/activate

                echo "⬆️ Upgrade pip"
                pip install --upgrade pip

                echo "📚 Installation dépendances"
                pip install -r requirements.txt

                echo "🔍 Vérification du code Python"
                python -m py_compile app.py
                '''
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
        export KUBECONFIG=/var/lib/jenkins/kubeconfig-kind
        export PATH=$PATH:/usr/local/bin  # <-- ajoute le chemin où Helm est installé
        echo "🌐 Vérification des nodes du cluster"
        kubectl get nodes
        echo "🚀 Déploiement Helm Chart"
        helm upgrade -i python-app ./python-app-helm
        '''
    }
}

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

} // <-- fermeture du pipeline
