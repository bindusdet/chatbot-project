pipeline{
    agent any
    
    environment{
        IMAGE_NAME = "bindu65/chatbot-bindu:${GIT_COMMIT}"
        AWS_REGION   = "us-east-1"
        CLUSTER_NAME = "bindu-cluster"
        NAMESPACE    = "bindu"
        
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

        stage('Cluster-Update') {
    steps {
        withCredentials([
            [$class: 'AmazonWebServicesCredentialsBinding',
             credentialsId: 'aws-creds']
        ]) {
            sh '''
              aws sts get-caller-identity
              aws eks update-kubeconfig \
                --region ${AWS_REGION} \
                --name ${CLUSTER_NAME}
            '''
            }
        }
    }

        stage('Deploying to EKS clsuter') {
            steps {
                withKubeConfig(
                    caCertificate: '',
                    clusterName: 'bindu-cluster',
                    contextName: '',
                    credentialsId: 'kube',
                    namespace: 'bindu',
                    restrictKubeConfigAccess: false,
                    serverUrl: 'https://60E78979056985109A5B28A630624F42.gr7.us-east-1.eks.amazonaws.com'
                ) {
                    sh "sed -i 's|replace|${IMAGE_NAME}|g' Deployment.yaml"
                    sh "kubectl apply -f Deployment.yaml -n ${NAMESPACE}"
                }
            }
        }
        stage('Verify the deployment') {
            steps {
                withKubeConfig(
                    caCertificate: '',
                    clusterName: 'itkannabindudigaru-cluster',
                    contextName: '',
                    credentialsId: 'kube',
                    namespace: 'bindu',
                    restrictKubeConfigAccess: false,
                    serverUrl: 'https://60E78979056985109A5B28A630624F42.gr7.us-east-1.eks.amazonaws.com'
                ) {
                    sh "kubectl get pods -n ${NAMESPACE}"
                    sh "kubectl get svc -n ${NAMESPACE}"
                }
         
            }
        }
    }
}
