pipeline{
    agent any
    
    environment{
        IMAGE_NAME = "bindu65/chatbot-bindu:${GIT_COMMIT}"
        
    }

    stages{
        stage('git-checkout'){
            steps{
                git url: 'https://github.com/bindusdet/chatbot-project.git' , branch: 'main'  
            }
        }
        stage('build'){
            steps{
                sh '''
                    printenv
                    docker build -t ${IMAGE_NAME} .
                ''' 
            }
        } 
        stage('Testing-stage'){
            steps{
                sh '''
                    docker kill chatbot-container-08
                    docker rm chatbot-container-08
                    docker run -it -d --name chatbot-container-08 -p 9002:8501 ${IMAGE_NAME}
                ''' 
            }
        } 
        stage('Login to Docker hub'){
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-hub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                }
        } 
    }
    stage('Push to Docker Hub'){
        steps{
            sh '''
                docker push ${IMAGE_NAME}
            ''' 
        }
    }
    
}