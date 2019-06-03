pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                echo 'Testing ...'
                tox
            }
        }
        stage('Build') {
            steps {
                echo 'Building package ...'
                export HTTP_PROXY=http://proxy.meteoswiss.ch:8080
                export HTTPS_PROXY=https://proxy.meteoswiss.ch:8080
                export TWINE_REPOSITORY_URL=http://nexus.meteoswiss.ch:8081/repository/python-mch/
                export TWINE_USERNAME=python-mch
                export TWINE_PASSWORD=pwd4python-mch
                python3 setup.py bdist_wheel
                twine upload dist/*
            }
        }
    }
}
