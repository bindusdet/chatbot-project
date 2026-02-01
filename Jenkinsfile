pipeline{
    agent any
    
    environment{
        IMAGE_NAME = "chatbot-bindu:${GIT_COMMIT}"
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
                    docker run -it -d --name chatbot-container-b -p 9002:8501 ${IMAGE_NAME}
                ''' 
            }
        } 
    }
}