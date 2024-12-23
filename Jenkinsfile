pipeline {
    agent any

    environment {
        // 환경 설정을 위한 변수들
        ENV_FILE = '/var/lib/jenkins/environments/.env.ai'
        DOCKER_IMAGE = 'aida0/gitfolio_ai:prod'  // prod 태그로 변경
        AWS_REGION = 'ap-northeast-2'

        // Discord 웹훅 URL (credentials로 관리하는 것이 더 안전합니다)
        DISCORD_CI_WEBHOOK = credentials('ai-dev-discord-ci-webhook')
        DISCORD_CD_WEBHOOK = credentials('ai-dev-discord-cd-webhook')
    }

    stages {
        // 파이프라인 시작 알림
        stage('Pipeline Start Notification') {
            steps {
                script {
                    // Discord로 파이프라인 시작 알림 전송
                    def message = """
                    {
                        "embeds": [{
                            "title": "🚀 파이프라인 시작",
                            "description": "빌드 #${env.BUILD_NUMBER}가 시작되었습니다.\\n브랜치: ${env.GIT_BRANCH ?: 'feature/cicd'}\\n깃트폴리오 AI 서버 빌드 프로세스를 시작합니다.",
                            "color": 16776960,
                            "timestamp": "${new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'", TimeZone.getTimeZone('UTC'))}"
                        }]
                    }""".trim().replaceAll("\n\\s*", " ")

                    // Discord로 알림 전송
                    sh """
                        curl -H "Content-Type: application/json" \
                            -d '${message}' \
                            ${env.DISCORD_CI_WEBHOOK}
                    """
                }
            }
        }

        // 환경 변수 로드
        stage('Load Environment Variables') {
            steps {
                script {
                    // Discord로 환경 변수 설정 시작 알림
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

        // 소스 코드 체크아웃
        stage('Checkout') {
            steps {
                script {
                    // Discord로 체크아웃 시작 알림
                    def message = """
                    {
                        "embeds": [{
                            "title": "📥 소스 코드 체크아웃",
                            "description": "깃허브 저장소에서 소스 코드를 가져오고 있습니다.\\n저장소: KTB-Sixmen/gitfolio_AI\\n브랜치: develop",
                            "color": 65280,
                            "timestamp": "${new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'", TimeZone.getTimeZone('UTC'))}"
                        }]
                    }""".trim().replaceAll("\n\\s*", " ")

                    sh """
                        curl -H "Content-Type: application/json" \
                            -d '${message}' \
                            ${env.DISCORD_CI_WEBHOOK}
                    """

                    // Git 체크아웃 수행
                    git branch: 'feature/cicd',
                        url: 'https://github.com/KTB-Sixmen/gitfolio_AI.git'
                }
            }
        }

        // Docker 이미지 빌드
        stage('Docker Build & Push') {
            steps {
                script {
                    // Discord로 Docker 빌드 시작 알림
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

                    // Docker 빌드 및 푸시
                    withCredentials([usernamePassword(credentialsId: 'docker-credentials',
                                                    usernameVariable: 'DOCKER_USER',
                                                    passwordVariable: 'DOCKER_PASS')]) {
                        // Docker Hub 로그인
                        sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"

                        // Dockerfile 내용 생성 - 환경변수를 이미지에 포함
                        writeFile file: 'Dockerfile', text: """
                            FROM node:18

                            WORKDIR /app

                            COPY package*.json ./

                            RUN npm install

                            COPY . .

                            # 환경변수를 이미지에 포함
                            ENV OPENAI_API_KEY=${env.OPENAI_API_KEY} \\
                                GH_TOKEN=${env.GH_TOKEN} \\
                                HOST=${env.HOST} \\
                                PORT=${env.PORT}

                            EXPOSE ${env.PORT}

                            CMD ["npm", "start"]
                        """

                        // Docker 이미지 빌드 및 푸시
                        sh """
                            docker build -t ${DOCKER_IMAGE} .
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
                        // 빌드 성공 알림 전송
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
                        // 빌드 실패 알림 전송
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
                    // 작업 디렉토리 정리
                    cleanWs()

                    // Docker 이미지 정리
                    sh """
                        docker image prune -f
                        docker builder prune -f --filter until=24h
                    """
                }
            }
        }