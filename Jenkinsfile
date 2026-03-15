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
            # 1. Fix permissions so Jenkins can touch/read the file
            sudo touch /home/ubuntu/Claude-Sentinel/app_access.log
            sudo chmod 666 /home/ubuntu/Claude-Sentinel/app_access.log
            
            # 2. Cleanup and Build
            docker stop app || true && docker rm app || true
            docker build -t security-app .
            
            # 3. Run Container
            docker run -d --name app \
              -p 8000:8000 \
              -v /home/ubuntu/Claude-Sentinel/app_access.log:/app/app_access.log \
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
