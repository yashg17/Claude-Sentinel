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
        
stages {
        stage('Docker Build & Deploy') {
            steps {
                sh '''
                    # Clean up existing container
                    docker stop app || true && docker rm app || true
                    
                    # Build and Run
                    docker build -t security-app .
                    docker run -d --name app \
                      -p 8000:8000 \
                      -v /var/lib/jenkins/workspace/Claude-Sentinel/app_access.log:/app/app_access.log \
                      -e ANTHROPIC_API_KEY=${CLAUDE_API_KEY} \
                      -e PYTHONUNBUFFERED=1 \
                      security-app
                '''
            }
        }
    }
}
        
        stage('Cleanup') {
            steps {
                sh 'docker image prune -f'
            }
        }
    }
}
