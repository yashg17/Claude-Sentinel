pipeline {
    agent any
    environment {
        CLAUDE_API_KEY = credentials('CLAUDE_KEY') 
    }
    stages {
        stage('Build & Deploy') {
            steps {
                sh 'docker build -t security-app .'
                sh 'docker stop app || true && docker rm app || true'
                sh 'docker run -d --name app -p 5000:5000 -v $(pwd):/app security-app'
            }
        }
    }
}
