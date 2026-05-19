pipeline {
    agent any

    environment {
        APP_NAME   = 'calculator-app'
        VENV_DIR   = 'venv'
        DEPLOY_DIR = 'C:\\DeployedApps\\calculator-app'
        PYTHON     = 'C:\\Users\\lenovo\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        // --------------------------------------------------
        // STAGE 1: CHECKOUT
        // --------------------------------------------------
        stage('Checkout') {
            steps {
                echo '========================================'
                echo '  STAGE 1: Checkout from GitHub'
                echo '========================================'

                checkout scm

                script {
                    def commitId = bat(script: 'git rev-parse --short HEAD', returnStdout: true).trim().readLines().last()
                    def branch   = bat(script: 'git rev-parse --abbrev-ref HEAD', returnStdout: true).trim().readLines().last()
                    def author   = bat(script: 'git log -1 --format="%%an"', returnStdout: true).trim().readLines().last()

                    echo "Branch  : ${branch}"
                    echo "Commit  : ${commitId}"
                    echo "Author  : ${author}"
                }
            }
        }
        // --------------------------------------------------
        // STAGE 2: BUILD
        // --------------------------------------------------
        stage('Build') {
            steps {
                echo '========================================'
                echo '  STAGE 2: Build - Setting up Python env'
                echo '========================================'

                bat """
                    echo [BUILD] Python version:
                    "${PYTHON}" --version

                    echo [BUILD] Creating virtual environment...
                    "${PYTHON}" -m venv ${VENV_DIR}

                    echo [BUILD] Installing dependencies...
                    call ${VENV_DIR}\\Scripts\\activate.bat && python -m pip install -r requirements.txt

                    echo [BUILD] Installed packages:
                    call ${VENV_DIR}\\Scripts\\activate.bat && pip list

                    echo [BUILD] Running app to verify...
                    call ${VENV_DIR}\\Scripts\\activate.bat && python app\\calculator.py

                    echo [BUILD] Build completed successfully!
                """
            }
        }

        // --------------------------------------------------
        // STAGE 3: TEST
        // --------------------------------------------------
        stage('Test') {
            steps {
                echo '========================================'
                echo '  STAGE 3: Test - Running pytest suite'
                echo '========================================'

                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat && pytest tests/ --tb=short --html=test-report.html --self-contained-html -v
                    echo [TEST] Test run complete!
                """
            }

            post {
                always {
                    archiveArtifacts artifacts: 'test-report.html', allowEmptyArchive: true
                    echo '[TEST] Test report archived!'
                }
            }
        }

        // --------------------------------------------------
        // STAGE 4: DEPLOY
        // --------------------------------------------------
        stage('Deploy') {
            steps {
                echo '========================================'
                echo '  STAGE 4: Deploy - Deploying application'
                echo '========================================'

                bat """
                    echo [DEPLOY] Creating deployment directory...
                    if not exist "${DEPLOY_DIR}" mkdir "${DEPLOY_DIR}"

                    echo [DEPLOY] Copying application files...
                    xcopy /E /I /Y app "${DEPLOY_DIR}\\app"
                    copy /Y requirements.txt "${DEPLOY_DIR}\\requirements.txt"

                    echo [DEPLOY] Writing deployment manifest...
                    echo App Name : ${APP_NAME}     > "${DEPLOY_DIR}\\deployment-info.txt"
                    echo Build #  : ${BUILD_NUMBER} >> "${DEPLOY_DIR}\\deployment-info.txt"
                    echo Status   : DEPLOYED        >> "${DEPLOY_DIR}\\deployment-info.txt"

                    echo [DEPLOY] Manifest:
                    type "${DEPLOY_DIR}\\deployment-info.txt"

                    echo [DEPLOY] Running smoke test on deployed app...
                    call ${VENV_DIR}\\Scripts\\activate.bat && python "${DEPLOY_DIR}\\app\\calculator.py"

                    echo [DEPLOY] Deployment successful!
                """
            }
        }
    }

    post {
        success {
            echo """
            ================================================
             SUCCESS - PIPELINE PASSED
             App     : ${env.APP_NAME}
             Build # : ${env.BUILD_NUMBER}
            ================================================
            """
        }

        failure {
            echo """
            ================================================
             FAILED - Check logs above
             Build # : ${env.BUILD_NUMBER}
            ================================================
            """
        }

        always {
            echo '[CLEANUP] Cleaning up venv...'
            bat "if exist ${VENV_DIR} rmdir /S /Q ${VENV_DIR}"
            echo '[CLEANUP] Done.'
        }
    }
}
