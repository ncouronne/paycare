pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'paycare-etl'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/ncouronne/paycare.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                // withPythonEnv('/usr/bin/python3') {
                sh '''python3 -m venv venv
                . venv/bin/activate
                venv/bin/python3 -m pip install -r requirements.txt'''}
            // }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''. venv/bin/activate
                pytest --junitxml=unit-tests.xml'''}
        
            post {
                always {
                    junit 'unit-tests.xml'  // Publish test results
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Create input data file dynamically
                    sh 'echo "employee_id,employee_name,salary\n101,Alice,5000\n102,Bob,7000" > input_data.csv'

                    // Run the Docker container with mounted input/output files
                    sh 'docker run --rm -v $(pwd)/input_data.csv:/app/input_data.csv -v $(pwd)/output_data.csv:/app/output_data.csv ${DOCKER_IMAGE}'
                }
            }
        }
    }

    post {
        success {
            echo 'ETL Pipeline completed successfully!'
            // Optionally send notification (Slack/Email)
        }
        failure {
            echo 'ETL Pipeline failed.'
            // Optionally send notification (Slack/Email)
        }
    }
}
