pipeline {
    agent any

    // ========================================
    // Environment Variables
    // ========================================
    environment {
        APP_NAME    = 'calculator-app'
        PYTHON_CMD  = 'python3'
        VENV_DIR    = 'venv'
        DEPLOY_DIR  = '/tmp/deployed-apps/calculator-app'
        BUILD_REPORT = 'build-report.txt'
    }

    // ========================================
    // Pipeline Options
    // ========================================
    options {
        timestamps()                        // Show timestamp on each log line
        timeout(time: 15, unit: 'MINUTES') // Fail if pipeline takes > 15 min
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    // ========================================
    // STAGES
    // ========================================
    stages {

        // --------------------------------------------------
        // STAGE 1: CHECKOUT
        // Pull the latest code from GitHub
        // --------------------------------------------------
        stage('Checkout') {
            steps {
                echo '========================================'
                echo '  STAGE 1: Checkout from GitHub'
                echo '========================================'

                // Jenkins automatically checks out the repo
                // configured in the job settings.
                // We just log what was pulled.
                checkout scm

                script {
                    def commitId  = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    def branch    = sh(script: 'git rev-parse --abbrev-ref HEAD', returnStdout: true).trim()
                    def author    = sh(script: 'git log -1 --format="%an"', returnStdout: true).trim()
                    def message   = sh(script: 'git log -1 --format="%s"', returnStdout: true).trim()

                    echo "Branch  : ${branch}"
                    echo "Commit  : ${commitId}"
                    echo "Author  : ${author}"
                    echo "Message : ${message}"
                }
            }
        }

        // --------------------------------------------------
        // STAGE 2: BUILD
        // Create virtual environment and install dependencies
        // --------------------------------------------------
        stage('Build') {
            steps {
                echo '========================================'
                echo '  STAGE 2: Build - Setting up Python env'
                echo '========================================'

                sh """
                    echo "[BUILD] Python version:"
                    ${PYTHON_CMD} --version

                    echo "[BUILD] Creating virtual environment..."
                    ${PYTHON_CMD} -m venv ${VENV_DIR}

                    echo "[BUILD] Activating venv and installing dependencies..."
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt

                    echo "[BUILD] Installed packages:"
                    pip list

                    echo "[BUILD] Running app to verify it works..."
                    ${PYTHON_CMD} app/calculator.py

                    echo "[BUILD] Build completed successfully!"
                """
            }
        }

        // --------------------------------------------------
        // STAGE 3: TEST
        // Run all pytest unit tests and generate HTML report
        // --------------------------------------------------
        stage('Test') {
            steps {
                echo '========================================'
                echo '  STAGE 3: Test - Running pytest suite'
                echo '========================================'

                sh """
                    . ${VENV_DIR}/bin/activate

                    echo "[TEST] Discovering and running tests..."
                    pytest tests/ \
                        --tb=short \
                        --html=test-report.html \
                        --self-contained-html \
                        -v \
                        | tee test-output.txt

                    echo "[TEST] Test run complete!"
                """
            }

            post {
                always {
                    // Archive the HTML test report as a build artifact
                    archiveArtifacts artifacts: 'test-report.html', allowEmptyArchive: true

                    script {
                        if (fileExists('test-output.txt')) {
                            def testOutput = readFile('test-output.txt')
                            if (testOutput.contains('passed')) {
                                echo "[TEST] ✅ All tests PASSED!"
                            } else {
                                echo "[TEST] ❌ Some tests FAILED!"
                            }
                        }
                    }
                }
            }
        }

        // --------------------------------------------------
        // STAGE 4: DEPLOY
        // Simulate deployment - copy app to a deploy directory
        // --------------------------------------------------
        stage('Deploy') {
            steps {
                echo '========================================'
                echo '  STAGE 4: Deploy - Deploying application'
                echo '========================================'

                sh """
                    echo "[DEPLOY] Creating deployment directory..."
                    mkdir -p ${DEPLOY_DIR}

                    echo "[DEPLOY] Copying application files..."
                    cp -r app/        ${DEPLOY_DIR}/
                    cp requirements.txt ${DEPLOY_DIR}/

                    echo "[DEPLOY] Writing deployment manifest..."
                    BUILD_TIME=\$(date '+%Y-%m-%d %H:%M:%S')
                    COMMIT_ID=\$(git rev-parse --short HEAD)

                    cat > ${DEPLOY_DIR}/deployment-info.txt << EOF
App Name   : ${APP_NAME}
Build #    : ${BUILD_NUMBER}
Commit     : \${COMMIT_ID}
Deployed At: \${BUILD_TIME}
Branch     : \$(git rev-parse --abbrev-ref HEAD)
Status     : DEPLOYED ✅
EOF

                    echo "[DEPLOY] Deployment manifest:"
                    cat ${DEPLOY_DIR}/deployment-info.txt

                    echo ""
                    echo "[DEPLOY] Running smoke test on deployed app..."
                    ${PYTHON_CMD} ${DEPLOY_DIR}/app/calculator.py

                    echo "[DEPLOY] ✅ Deployment successful!"
                    echo "[DEPLOY] App is live at: ${DEPLOY_DIR}"
                """
            }

            post {
                success {
                    archiveArtifacts artifacts: 'test-report.html', allowEmptyArchive: true
                    echo "✅ Pipeline completed — ${env.APP_NAME} deployed successfully!"
                }
            }
        }
    }

    // ========================================
    // POST - Runs after ALL stages finish
    // ========================================
    post {

        success {
            echo """
            ================================================
             ✅  PIPELINE SUCCEEDED
            ================================================
             App      : ${env.APP_NAME}
             Build #  : ${env.BUILD_NUMBER}
             Branch   : ${env.GIT_BRANCH}
             Duration : ${currentBuild.durationString}
            ================================================
            """
        }

        failure {
            echo """
            ================================================
             ❌  PIPELINE FAILED
            ================================================
             Check the logs above to identify the issue.
             Build # : ${env.BUILD_NUMBER}
            ================================================
            """
        }

        always {
            echo "[CLEANUP] Cleaning up workspace..."
            sh "rm -rf ${VENV_DIR}"
            echo "[CLEANUP] Done."
        }
    }
}
