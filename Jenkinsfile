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
        echo 'Stopping old sentinel and starting new one...'
        sh '''
            # Kill the old process if it exists so we don't have 10 sentinels running
            pkill -f security_sentinel.py || true
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
                    docker stop app || true && docker rm app || true
                    # Pass the API key into the container
                    docker run -d --name app \
                      -p 8000:8000 \
                      -e ANTHROPIC_API_KEY=${CLAUDE_API_KEY} \
                      security-app
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
