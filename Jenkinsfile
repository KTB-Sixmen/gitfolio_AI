pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-northeast-2'
        ECR_REGISTRY = credentials('ecr-registry')
        DISCORD_CI_WEBHOOK = credentials('ai-dev-discord-ci-webhook')
        DISCORD_CD_WEBHOOK = credentials('ai-dev-discord-cd-webhook')
        DOCKER_TAG = 'dev'
        ENV_FILE = '/var/lib/jenkins/environments/.env.ai'
    }

    stages {
        stage('소스코드 체크아웃') {
            steps {
                script {
                    deleteDir()
                    git branch: 'feature/ai-cicd',
                        url: 'https://github.com/KTB-Sixmen/gitfolio_AI.git'
                }
            }
        }

        stage('환경 설정') {
            steps {
                script {
                    // 환경 변수 파일 복사
                    if (fileExists(ENV_FILE)) {
                        sh """
                            cp ${ENV_FILE} .env
                            echo '환경 파일 복사 완료: ${ENV_FILE}'
                        """
                    } else {
                        error "환경 파일을 찾을 수 없습니다: ${ENV_FILE}"
                    }

                    // ECR 로그인
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                                    credentialsId: 'aws-credentials',
                                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                        sh """
                            aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                            echo 'ECR 로그인 완료'
                        """
                    }
                }
            }
        }

        stage('Docker 이미지 빌드 및 푸시') {
            steps {
                script {
                    def imageTag = "${ECR_REGISTRY}/gitfolio/ai:${DOCKER_TAG}"

                    sh """
                        docker build \
                            -f Dockerfile \
                            -t ${imageTag} \
                            --platform linux/amd64 \
                            --build-arg OPENAI_API_KEY=${env.OPENAI_API_KEY} \
                            --build-arg GH_TOKEN=${env.GH_TOKEN} \
                            --build-arg HOST=${env.HOST} \
                            --build-arg PORT=${env.PORT} \
                            .

                        docker push ${imageTag}
                    """
                }
            }
        }

        stage('EC2 배포') {
            steps {
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                                    credentialsId: 'aws-credentials',
                                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {

                        def instanceIds = sh(
                            script: """
                                aws ec2 describe-instances \
                                    --region ${AWS_REGION} \
                                    --filters 'Name=tag:Service,Values=ai' \
                                        'Name=tag:Environment,Values=dev' \
                                        'Name=tag:Type,Values=ec2' \
                                        'Name=instance-state-name,Values=running' \
                                    --query 'Reservations[].Instances[].InstanceId' \
                                    --output text
                            """,
                            returnStdout: true
                        ).trim()

                        if (instanceIds) {
                            // 먼저 .env 파일을 EC2로 복사하는 명령을 추가합니다
                            sh """
                                aws ssm send-command \
                                    --instance-ids "${instanceIds}" \
                                    --document-name "AWS-RunShellScript" \
                                    --comment "환경 파일 복사" \
                                    --parameters commands='
                                        cd /home/ec2-user
                                        cat > .env << 'EOL'
                                        $(cat ${ENV_FILE})
                                        EOL
                                        chmod 600 .env
                                    ' \
                                    --timeout-seconds 600 \
                                    --region ${AWS_REGION}
                            """

                        if (instanceIds) {
                            sh """
                                aws ssm send-command \
                                    --instance-ids "${instanceIds}" \
                                    --document-name "AWS-RunShellScript" \
                                    --comment "AI 서버 배포" \
                                    --parameters commands='
                                        cd /home/ec2-user
                                        export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
                                        export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
                                        export AWS_DEFAULT_REGION=${AWS_REGION}
                                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                                        docker-compose down -v --rmi all
                                        docker builder prune -f --filter until=24h
                                        docker image prune -f
                                        docker-compose pull
                                        docker-compose up -d
                                    ' \
                                    --timeout-seconds 600 \
                                    --region ${AWS_REGION}
                            """
                        } else {
                            error "실행 중인 AI 서비스 EC2 인스턴스를 찾을 수 없습니다."
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                sh """
                    docker builder prune -f --filter until=24h
                    docker image prune -f
                    rm -f .env
                """
            }
        }

    }



}