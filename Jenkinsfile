pipeline {
    agent any
    
    environment {
        CLAUDE_API_KEY = credentials('CLAUDE_API_KEY') 
    }
    
    stages {
        stage('Setup Workspace') {
            steps {
                sh '''
                    # Force remove any existing directory or file to prevent permission/type errors
                    rm -rf app_access.log
                    touch app_access.log
                    chmod 666 app_access.log
                '''
            }
        }
        
        stage('Docker Build & Deploy') {
            steps {
                sh '''
                    # Stop and remove existing container if it exists
                    docker stop app || true
                    docker rm app || true
                    
                    # Build the image
                    docker build -t security-app .
                    
                    # Run the container using $(pwd) for the volume mount
                    docker run -d --name app \
                      -p 8000:8000 \
                      -v $(pwd)/app_access.log:/app/app_access.log \
                      -e ANTHROPIC_API_KEY=${CLAUDE_API_KEY} \
                      -e PYTHONUNBUFFERED=1 \
                      security-app
                '''
            }
        }
    }
    
    post {
        always {
            sh 'docker image prune -f'
        }
    }
}
