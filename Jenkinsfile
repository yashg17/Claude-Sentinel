pipeline {
    agent any
    environment {
        CLAUDE_API_KEY = credentials('CLAUDE_API_KEY') 
    }
    stages {
        stage('Setup Environment') {
            steps {
                echo 'Skipping venv setup as we are moving to Docker...'
            }
        }
        
        // REMOVE THE OLD 'Security Analysis' STAGE COMPLETELY
        
        stage('Docker Build & Deploy') {
            steps {
                echo 'Packaging and running AI Sentinel in Docker...'
                sh '''
                    # Stop the old host process if it's still running
                    pkill -f security_sentinel.py || true
                    
                    docker build -t security-app .
                    docker stop app || true && docker rm app || true
                    
                    docker run -d --name app \
                    -p 8000:8000 \
                    -v /var/lib/jenkins/workspace/Claude-Sentinel/app_access.log:/app/app_access.log \
                    -e ANTHROPIC_API_KEY=${CLAUDE_API_KEY} \
                    security-app
                '''
            }
        }
        
        stage('Cleanup') {
            steps {
                sh 'docker image prune -f'
            }
        }
    }
}
