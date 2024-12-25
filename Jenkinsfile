pipeline {
    agent any

    environment {
        // 환경 변수 파일 경로 설정
        ENV_FILE = '/var/lib/jenkins/environments/.env.ai'
        // Docker 이미지 정보
        DOCKER_IMAGE = '727646500036.dkr.ecr.ap-northeast-2.amazonaws.com/gitfolio/ai:dev'
        // AWS 리전
        AWS_REGION = 'ap-northeast-2'
    }

    stages {
        stage('Load Environment Variables') {
            steps {
                script {
                    // .env.ai 파일에서 환경 변수 로드
                    def envContent = readFile(ENV_FILE).trim()
                    envContent.split('\n').each { line ->
                        def (key, value) = line.split('=', 2)
                        env."${key}" = value
                    }
                }
            }
        }

        stage('Checkout') {
            steps {
                // Git 저장소 URL을 직접 지정하여 체크아웃
                git branch: 'develop',
                    url: 'https://github.com/KTB-Sixmen/gitfolio_AI.git'
            }
        }

        stage('Docker Build & Push') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-credentials',
                                                    usernameVariable: 'DOCKER_USER',
                                                    passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                            # Docker 이미지 빌드
                            docker build \
                                --build-arg OPENAI_API_KEY="$OPENAI_API_KEY" \
                                --build-arg GH_TOKEN="$GH_TOKEN" \
                                --build-arg HOST="$HOST" \
                                --build-arg PORT="$PORT" \
                                -t ${DOCKER_IMAGE} .

                            # Docker 이미지 푸시
                            docker push ${DOCKER_IMAGE}
                        '''
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                                    credentialsId: 'aws-credentials',
                                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {

                        // EC2 인스턴스 ID 조회
                        def instanceIds = sh(
                            script: """
                                aws ec2 describe-instances \
                                    --region ${AWS_REGION} \
                                    --filters 'Name=tag:Service,Values=ai' 'Name=instance-state-name,Values=running' \
                                    --query 'Reservations[].Instances[].InstanceId' \
                                    --output text
                            """,
                            returnStdout: true
                        ).trim()

                        if (instanceIds) {
                            // docker-compose.yaml 파일 인코딩
                            def dockerComposeContent = sh(
                                script: "base64 docker-compose.yaml | tr -d '\n'",
                                returnStdout: true
                            ).trim()

                            // SSM 명령 실행 - JSON 형식 수정
                            def commandId = sh(
                                script: """
                                    aws ssm send-command \
                                        --instance-ids "${instanceIds}" \
                                        --document-name "AWS-RunShellScript" \
                                        --comment "Deploying AI Server" \
                                        --parameters '{"commands":["cd /home/ec2-user","echo '\\''${dockerComposeContent}'\\'' | base64 -d > docker-compose.yaml","echo '\\''OPENAI_API_KEY=${env.OPENAI_API_KEY}'\\'' > .env","echo '\\''GH_TOKEN=${env.GH_TOKEN}'\\'' >> .env","echo '\\''HOST=${env.HOST}'\\'' >> .env","echo '\\''PORT=${env.PORT}'\\'' >> .env","chmod 600 .env","docker-compose down -v --rmi all","docker-compose pull","docker-compose up -d"]}' \
                                        --timeout-seconds 600 \
                                        --region ${AWS_REGION} \
                                        --output text \
                                        --query 'Command.CommandId'
                                """,
                                returnStdout: true
                            ).trim()

                            // 명령 실행 완료 대기
                            sh """
                                aws ssm wait command-executed \
                                    --command-id ${commandId} \
                                    --instance-id ${instanceIds} \
                                    --region ${AWS_REGION}
                            """

                            // 실행 결과 확인
                            sh """
                                aws ssm get-command-invocation \
                                    --command-id ${commandId} \
                                    --instance-id ${instanceIds} \
                                    --region ${AWS_REGION}
                            """
                        } else {
                            error "No running EC2 instances found with the specified tags"
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            // 작업 완료 후 정리
            cleanWs()
        }
    }
}