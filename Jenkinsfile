pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-northeast-2'
        ECR_REGISTRY = credentials('ecr-registry')
        DISCORD_CI_WEBHOOK = credentials('ai-dev-discord-ci-webhook')
        DOCKER_TAG = 'prod'  // dev -> prod로 변경
        ENV_FILE = '/var/lib/jenkins/environments/.env.ai'
    }

    stages {
        stage('소스코드 체크아웃') {
            steps {
                script {
                    deleteDir()
                    git branch: 'develop',
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

                                        # .env 파일에서 환경변수를 추출하여 Jenkins 환경에 설정
                                        export OPENAI_API_KEY=\$(grep OPENAI_API_KEY .env | cut -d '=' -f2)
                                        export GH_TOKEN=\$(grep GH_TOKEN .env | cut -d '=' -f2)
                                        export HOST=\$(grep HOST .env | cut -d '=' -f2)
                                        export PORT=\$(grep PORT .env | cut -d '=' -f2)

                                        # 환경변수를 Jenkins 환경에 설정
                                        echo "OPENAI_API_KEY=\${OPENAI_API_KEY}" >> env.properties
                                        echo "GH_TOKEN=\${GH_TOKEN}" >> env.properties
                                        echo "HOST=\${HOST}" >> env.properties
                                        echo "PORT=\${PORT}" >> env.properties
                                    """

                                    // env.properties 파일을 Jenkins 환경변수로 로드
                                    def props = readProperties file: 'env.properties'
                                    env.OPENAI_API_KEY = props.OPENAI_API_KEY
                                    env.GH_TOKEN = props.GH_TOKEN
                                    env.HOST = props.HOST
                                    env.PORT = props.PORT
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

        # 빌드된 이미지의 환경변수 확인
                        echo "===== 이미지 환경변수 확인 ====="
                        docker run --rm ${imageTag} env | grep -E "OPENAI_API_KEY|GH_TOKEN|HOST|PORT"

                        docker push ${imageTag}
                    """
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