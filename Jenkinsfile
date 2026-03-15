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
        sh '''
            # Create the file if it doesn't exist (no sudo needed for workspace files)
            # We point to the local workspace file instead of /home/ubuntu to avoid permission walls
            touch app_access.log
            chmod 666 app_access.log
            
            # Stop and remove old container
            docker stop app || true && docker rm app || true
            
            # Build and Run
            docker build -t security-app .
            docker run -d --name app \
              -p 8000:8000 \
              -v $(pwd)/app_access.log:/app/app_access.log \
              -e ANTHROPIC_API_KEY=${CLAUDE_API_KEY} \
              -e PYTHONUNBUFFERED=1 \
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
