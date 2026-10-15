pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.12'
        VITE_API_BASE_URL = 'http://localhost:8000'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning and preparing the repository...'
            }
        }

        stage('Backend setup') {
            steps {
                dir('backend') {
                    sh 'python3 --version'
                    sh 'python3 -m pip install --upgrade pip'
                    sh 'python3 -m pip install -r requirements.txt'
                    sh 'python3 manage.py check'
                    sh 'python3 manage.py migrate --noinput'
                    sh 'python3 manage.py seed_listings --with-orders'
                }
            }
        }

        stage('Frontend setup') {
            steps {
                dir('frontend') {
                    sh 'npm install'
                    sh 'npm run build'
                }
            }
        }

        stage('Docker validation') {
            steps {
                sh 'docker compose build --no-cache'
            }
        }
    }

    post {
        always {
            echo 'CampusMart CI pipeline completed.'
        }
        success {
            echo 'Build and validation succeeded.'
        }
        failure {
            echo 'Build failed. Inspect logs for issues.'
        }
    }
}
