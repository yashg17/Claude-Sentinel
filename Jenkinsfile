pipeline {
    agent any
    
    environment {
        // Ensure this ID matches the ID you gave the credential in Jenkins
        CLAUDE_API_KEY = credentials('CLAUDE_KEY') 
    }

    stages {
        stage('Setup Environment') {
            steps {
                echo 'Preparing Python Virtual Environment...'
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install anthropic prometheus_client
                '''
            }
        }

        stage('Security Analysis') {
            steps {
                echo 'Running AI Sentinel...'
                // Running the script using the python inside the venv
                // We use & to run it in the background so the pipeline can finish
                sh '''
                    export ANTHROPIC_API_KEY=${CLAUDE_API_KEY}
                    nohup ./venv/bin/python3 security_sentinel.py > sentinel.log 2>&1 &
                '''
            }
        }

        stage('Docker Build & Deploy') {
            steps {
                echo 'Packaging application...'
                sh '''
                    docker build -t security-app .
                    docker stop app || true
                    docker rm app || true
                    docker run -d --name app -p 5000:5000 security-app
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
