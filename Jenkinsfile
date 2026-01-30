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
                echo 'Building Application Logic...'
                sh """
                # Nettoyage de l'environnement précédent (fix pour problème venv/bin/activate)
                rm -rf ${VENV_NAME}
                
                echo "Vérification de la version Python..."
                python3 --version || echo "python3 non trouvé"
                
                echo "Création de l'environnement virtuel..."
                if ! python3 -m venv ${VENV_NAME}; then
                    echo "ERREUR CRITIQUE: Échec de la création du venv."
                    echo "Assurez-vous que le paquet 'python3-venv' est installé sur l'agent Jenkins."
                    echo "Exemple: sudo apt-get install python3-venv"
                    exit 1
                fi
                
                echo "Activation et installation..."
                . ${VENV_NAME}/bin/activate
                pip install -r requirements.txt
                
                echo "Vérification du code..."
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
