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
            # Ensure the log file exists so the container doesn't crash on start
            touch ${WORKSPACE}/app_access.log
            
            docker build -t security-app .
            docker stop app || true && docker rm app || true
            
            # Map the HOST log file into the CONTAINER log file path
           docker run -d --name app \
              -p 8000:8000 \
              -v ${WORKSPACE}/app_access.log:/app/app_access.log \
              -e ANTHROPIC_API_KEY=${CLAUDE_API_KEY} \
              -e PYTHONUNBUFFERED=1 \
              --restart always \
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
