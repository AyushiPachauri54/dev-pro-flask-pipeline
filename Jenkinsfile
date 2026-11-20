pipeline {
    agent any

    environment {
        DEPLOY_DIR = 'deployment'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Installing Python dependencies'
                sh '''
                    python3 --version
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running Unit Tests'
                sh '.venv/bin/python -m pytest -v'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying Flask Application'
                sh '''
                    rm -rf "$DEPLOY_DIR"
                    mkdir -p "$DEPLOY_DIR"
                    cp app.py requirements.txt "$DEPLOY_DIR/"
                '''
            }
        }

        stage('Run Application') {
            steps {
                echo 'Starting Flask Application'
                sh '''
                    cd "$DEPLOY_DIR"
                    nohup ../.venv/bin/python app.py > app.log 2>&1 &
                    echo $! > app.pid
                    sleep 3
                    cat app.log
                '''
            }
        }

        stage('Test Application') {
            steps {
                echo 'Verifying deployed application'
                sh '''
                    python3 - <<'PY'
import time
import urllib.request

url = "http://127.0.0.1:5000/"

for attempt in range(10):
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            body = response.read().decode()
            assert response.status == 200
            assert "Flask application is running successfully" in body
            print("Application verification successful!")
            print("Status:", response.status)
            print("Response:", body)
            break
    except Exception:
        if attempt == 9:
            raise
        time.sleep(1)
PY
                '''
            }
        }
    }

    post {
        success {
            echo 'PIPELINE SUCCESS'
        }

        failure {
            echo 'PIPELINE FAILED - Check Console Output'
        }

        always {
            sh '''
                if [ -f "$DEPLOY_DIR/app.pid" ]; then
                    kill "$(cat "$DEPLOY_DIR/app.pid")" 2>/dev/null || true
                fi
            '''
            echo 'Pipeline execution completed'
        }
    }
}
