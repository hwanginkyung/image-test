pipeline {
    agent any
    
    environment {
		#git 주소
    GITWEBADD = 'https://github.com/hwanginkyung/image-test.git'
		#git ssh주소
    GITSSHADD = 'git@github.com:hwanginkyung/image-test.git'
		#jenkins에 설정한 git자격증명
    GITCREDENTIAL = 'git_cre'
    
    ECR_REPO_URL = '970210524130.dkr.ecr.us-east-1.amazonaws.com/hik_test'
	  #jenkins에 설정한 aws 자격증명 
    ECR_CREDENTIAL = 'aws_cre'
}

        
    stages {
        #git에서 소스코드를 가져오는 stage
        stage('Checkout Github') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [],
                userRemoteConfigs: [[credentialsId: GITCREDENTIAL, url: GITWEBADD]]])
            }

            post {
                failure {
                    echo '리포지토리 복제 실패'
                }
                success {
                    echo '리포지토리 복제 성공'
                }
            }
        }
        #docker image build
        stage('image build') {
            steps {
                sh "docker build -t ${ECR_REPO_URL}:${currentBuild.number} ."
                sh "docker build -t ${ECR_REPO_URL}:latest ."
            }
        }
        #aws ecr에 로그인후, 생성된 docker image를 aws ecr에 push
        stage('image push') {
            steps {
                // AWS ECR에 로그인
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY', credentialsId: ECR_CREDENTIAL]]) {
                    script {
                        def ecrLogin = sh(script: "aws ecr get-login-password --region us-east-1", returnStdout: true).trim()
                        sh "docker login -u AWS -p ${ecrLogin} ${ECR_REPO_URL}"
                    }
                }

                // 이미지를 AWS ECR로 푸시
                sh "docker push ${ECR_REPO_URL}:${currentBuild.number}"
                sh "docker push ${ECR_REPO_URL}:latest"
            }
            
            post {
                failure {
                    echo 'AWS ECR로 이미지 푸시 실패'
                    sh "docker image rm -f ${ECR_REPO_URL}:${currentBuild.number}"
                    sh "docker image rm -f ${ECR_REPO_URL}:latest"
                }
                
                success {
                    echo 'AWS ECR로 이미지 푸시 성공'
                    sh "docker image rm -f ${ECR_REPO_URL}:${currentBuild.number}"
                    sh "docker image rm -f ${ECR_REPO_URL}:latest"
                }
            }
        }
    }
}
