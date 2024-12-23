pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-northeast-2'
        ECR_REGISTRY = credentials('ecr-registry')
        DISCORD_CI_WEBHOOK = credentials('ai-dev-discord-ci-webhook')
        DOCKER_IMAGE = 'aida0/gitfolio_ai:prod'  // prod 태그로 변경
        ENV_FILE = '/var/lib/jenkins/environments/.env.ai'
    }

    stages {
        // 파이프라인 시작 알림
        stage('Pipeline Start Notification') {
            steps {
                script {
                    def message = """
                    {
                        "embeds": [{
                            "title": "🚀 파이프라인 시작",
                            echo "ECR Registry: ${ECR_REGISTRY}",
                            echo "Docker Image Tag: ${DOCKER_IMAGE}",
                            "description": "빌드 #${env.BUILD_NUMBER}가 시작되었습니다.\\n브랜치: feature/ai-cicd\\n깃트폴리오 AI 서버 빌드 프로세스를 시작합니다.",
                            "color": 16776960,
                            "timestamp": "${new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'", TimeZone.getTimeZone('UTC'))}"
                        }]
                    }""".trim().replaceAll("\n\\s*", " ")

                    sh """
                        curl -H "Content-Type: application/json" \
                            -d '${message}' \
                            ${env.DISCORD_CI_WEBHOOK}
                    """
                }
            }
        }

        stage('소스코드 체크아웃') {
            steps {
                script {
                    def message = """
                    {
                        "embeds": [{
                            "title": "📥 소스 코드 체크아웃",
                            "description": "깃허브 저장소에서 소스 코드를 가져오고 있습니다.\\n저장소: KTB-Sixmen/gitfolio_AI\\n브랜치: feature/ai-cicd,
                            "color": 65280,
                            "timestamp": "${new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'", TimeZone.getTimeZone('UTC'))}"
                        }]
                    }""".trim().replaceAll("\n\\s*", " ")

                    sh """
                        curl -H "Content-Type: application/json" \
                            -d '${message}' \
                            ${env.DISCORD_CI_WEBHOOK}
                    """

                    deleteDir()
                    git branch: 'feature/ai-cicd',
                        url: 'https://github.com/KTB-Sixmen/gitfolio_AI.git'
                }
            }
        }
        stage('환경 설정') {
                    steps {
                        script {
                            def message = """
                            {
                                "embeds": [{
                                    "title": "⚙️ 환경 변수 설정",
                                    "description": "환경 설정 파일을 로드하고 있습니다...",
                                    "color": 65280,
                                    "timestamp": "${new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'", TimeZone.getTimeZone('UTC'))}"
                                }]
                            }""".trim().replaceAll("\n\\s*", " ")

                            sh """
                                curl -H "Content-Type: application/json" \
                                    -d '${message}' \
                                    ${env.DISCORD_CI_WEBHOOK}
                            """

                            // 환경 변수 파일에서 변수들을 읽어와 설정
                            def envContent = readFile(ENV_FILE).trim()
                            envContent.split('\n').each { line ->
                                if (line.trim()) {
                                    def (key, value) = line.split('=', 2)
                                    env."${key}" = value
                                }
                            }
                        }
                    }
                }

                stage('Docker 이미지 빌드 및 푸시') {
                    steps {
                        script {
                            def message = """
                            {
                                "embeds": [{
                                    "title": "🐳 도커 이미지 빌드",
                                    "description": "도커 이미지 빌드 작업을 시작합니다.\\n이미지: ${DOCKER_IMAGE}",
                                    "color": 65280,
                                    "timestamp": "${new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'", TimeZone.getTimeZone('UTC'))}"
                                }]
                            }""".trim().replaceAll("\n\\s*", " ")

                            sh """
                                curl -H "Content-Type: application/json" \
                                    -d '${message}' \
                                    ${env.DISCORD_CI_WEBHOOK}
                            """

                            // Docker Hub 로그인 및 빌드/푸시
                            withCredentials([usernamePassword(credentialsId: 'docker-credentials',
                                                            usernameVariable: 'DOCKER_USER',
                                                            passwordVariable: 'DOCKER_PASS')]) {
                                sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"

                                // Docker 이미지 빌드 - 환경변수를 build-arg로 전달
                                sh """
                                    docker build \
                                        -f Dockerfile \
                                        -t ${DOCKER_IMAGE} \
                                        --platform linux/amd64 \
                                        --build-arg OPENAI_API_KEY=${env.OPENAI_API_KEY} \
                                        --build-arg GH_TOKEN=${env.GH_TOKEN} \
                                        --build-arg HOST=${env.HOST} \
                                        --build-arg PORT=${env.PORT} \
                                        .

                                    docker push ${DOCKER_IMAGE}
                                """
                            }
                        }
                    }
                }
                }

                    // 파이프라인 완료 후 작업
                    post {
                        success {
                            script {
                                def message = """
                                {
                                    "embeds": [{
                                        "title": "✅ 빌드 성공",
                                        "description": "빌드 #${env.BUILD_NUMBER}가 성공적으로 완료되었습니다.\\n깃트폴리오 AI 서버 빌드가 정상적으로 완료되었습니다.",
                                        "color": 65280,
                                        "timestamp": "${new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'", TimeZone.getTimeZone('UTC'))}",
                                        "fields": [
                                            {
                                                "name": "빌드 번호",
                                                "value": "#${env.BUILD_NUMBER}",
                                                "inline": true
                                            },
                                            {
                                                "name": "이미지",
                                                "value": "${DOCKER_IMAGE}",
                                                "inline": true
                                            }
                                        ]
                                    }]
                                }""".trim().replaceAll("\n\\s*", " ")

                                sh """
                                    curl -H "Content-Type: application/json" \
                                        -d '${message}' \
                                        ${env.DISCORD_CI_WEBHOOK}
                                """
                            }
                        }

                        failure {
                            script {
                                def message = """
                                {
                                    "embeds": [{
                                        "title": "❌ 빌드 실패",
                                        "description": "빌드 #${env.BUILD_NUMBER}가 실패했습니다.\\nJenkins 로그를 확인해주세요.",
                                        "color": 16711680,
                                        "timestamp": "${new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'", TimeZone.getTimeZone('UTC'))}",
                                        "fields": [
                                            {
                                                "name": "실패 단계",
                                                "value": "${currentBuild.result}",
                                                "inline": true
                                            }
                                        ]
                                    }]
                                }""".trim().replaceAll("\n\\s*", " ")

                                sh """
                                    curl -H "Content-Type: application/json" \
                                        -d '${message}' \
                                        ${env.DISCORD_CI_WEBHOOK}
                                """
                            }
                        }

                        always {
                            cleanWs()
                            sh """
                                docker builder prune -f --filter until=24h
                                docker image prune -f
                            """
                        }
                    }
                }