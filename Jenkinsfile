pipeline {
    agent any

    environment {
        // Définition de l'environnement virtuel
        VENV_NAME = "venv"
    }

    stages {
        stage('Checkout') {
            steps {
                // Le checkout est souvent implicite, mais bonnes pratiques de s'assurer du clean
                checkout scm
                echo 'Code récupéré depuis le repository'
            }
        }

        stage('Build Python App') {
             steps {
                // Pour l'instant on fait juste un print, l'install est faite dans le Dockerfile
                // Mais on pourrait vouloir lancer des tests unitaires ici avant de build l'image
                echo 'Building Application Logic...'
                sh """
                if [ ! -d "${VENV_NAME}" ]; then
                    python3 -m venv ${VENV_NAME}
                fi
                . ${VENV_NAME}/bin/activate
                pip install -r requirements.txt
                python3 -m py_compile app.py
                """
             }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t my-python-app:latest .'
                }
            }
        }

        stage('Load Image Into Kind') {
            steps {
                script {
                    // Supposons que le cluster s'appelle 'kind' (par défaut)
                    sh 'kind load docker-image my-python-app:latest --name kind'
                }
            }
        }

        stage('Deploy to Kind') {
            steps {
                script {
                    sh 'kubectl apply -f k8s/'
                    // Force le rollout restart pour prendre en compte la nouvelle image si tag latest
                    sh 'kubectl rollout restart deployment/python-app-deployment'
                }
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
