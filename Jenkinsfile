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
            # 1. Create the log file on the host if it doesn't exist
            touch ${WORKSPACE}/app_access.log
            
            # 2. Build the image
            docker build -t security-app .
            
            # 3. Stop/Remove old container
            docker stop app || true && docker rm app || true
            
            # 4. Run with VOLUME MOUNT and PORT MAPPING
            docker run -d --name app \
              -p 8000:8000 \
              -v ${WORKSPACE}/app_access.log:/app/app_access.log \
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
