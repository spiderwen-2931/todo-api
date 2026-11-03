pipeline {
    agent any

    environment {
        VENV_DIR = '.venv'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Checking out source code from GitHub...'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo '🐍 Creating virtual environment and installing dependencies...'
                bat '''
                    python -m venv %VENV_DIR%
                    call %VENV_DIR%\\Scripts\\activate.bat
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                echo '🔍 Running linter (flake8)...'
                bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat
                    pip install flake8 --quiet
                    flake8 app/ --max-line-length=100 --ignore=E501,W503
                '''
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running pytest with coverage...'
                bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat
                    pytest tests/ -v --tb=short --cov=app --cov-report=xml --cov-report=term
                '''
            }
        }

        stage('Build Verification') {
            steps {
                echo '✅ Verifying app can be imported...'
                bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat
                    python -c "from app.main import app; print('App import: OK')"
                '''
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline PASSED — All stages completed successfully!'
        }
        failure {
            echo '❌ Pipeline FAILED — Check logs above for errors.'
        }
        always {
            cleanWs()
        }
    }
}

