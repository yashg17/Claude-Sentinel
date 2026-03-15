pipeline {
    agent any
    
    environment {
        CLAUDE_API_KEY = credentials('CLAUDE_API_KEY') 
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
                // Using JENKINS_NODE_COOKIE=dontKillMe prevents Jenkins from killing
                // the background process when the stage finishes.
                sh '''
                    export ANTHROPIC_API_KEY=${CLAUDE_API_KEY}
                    export JENKINS_NODE_COOKIE=dontKillMe
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

        stage('Cleanup') {
            steps {
                echo 'Cleaning up dangling Docker images and temporary files...'
                sh '''
                    # Remove unused Docker images to save disk space
                    docker image prune -f
                    
                    # Optional: Remove the virtual environment if you want a fresh start next time
                    # rm -rf venv
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Pipeline failed. Checking logs...'
        }
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
