# Quick automation demo 

Here’s a Python script for the demo:

    hw_test.py

Login to Jenkins and install:

- Git Plugin (to clone repositories).
- Python Plugin or ensure Python is installed on the system.
- Pipeline Plugin (for Jenkins pipelines).

Ensure your Python test script is in a version control system (e.g., GitHub). On your Jenkins machine install pytest:

    sudo apt update && sudo apt install python3-venv  # 
    python3 -m venv ~/entorno       # Create a virtual environment
    source ~/entorno/bin/activate   # Activate the environment
    pip install pytest              # Install in the virtual environment

## Create a Jenkins job

Add a Build Step > Execute Shell.
Use this script to set up the virtual environment and run the tests:

    #!/bin/bash
    source ~/python-env/bin/activate
    pip install -r requirements.txt  # Install dependencies 
    pytest tests/  # Run tests in the tests/ directory

### Pipeline configuration

    pipeline {
        agent any
        stages {
            stage('Clone Repository') {
                steps {
                    git 'https://github.com/your-repo.git'
                }
            }
            stage('Setup Python Environment') {
                steps {
                    sh '''
                    source ~/python-env/bin/activate
                    pip install -r requirements.txt
                    '''
                }
            }
            stage('Run Tests') {
                steps {
                    sh '''
                    source ~/python-env/bin/activate
                    pytest tests/
                    '''
                }
            }
        }
    }

## Automate builds

Go to Build Triggers in the job configuration and enable options **Poll SCM**: Automatically pull changes from the repository.

### Prepare Your Docker Environment

Run Jenkins and tests in a containerized environment for consistency

    # Use an official Python image as a base
    FROM python:3.9-slim

    # Set working directory
    WORKDIR /app

    # Copy application and install dependencies
    COPY . /app
    RUN pip install --no-cache-dir -r requirements.txt

    # Default command for the container
    CMD ["pytest", "tests/"]

Build the Docker image locally to verify it works:

    docker build -t firmware-tests .
    docker run firmware-tests

### Pipeline Configuration

    pipeline {
        agent {
            docker {
                image 'python:3.9-slim'  // Base Docker image
            }
        }
        stages {
            stage('Clone Repository') {
                steps {
                    checkout scm  // Clone the repository
                }
            }
            stage('Build Docker Image') {
                steps {
                    script {
                        // Build the Docker image
                        sh 'docker build -t firmware-tests .'
                    }
                }
            }
            stage('Run Tests in Docker') {
                steps {
                    script {
                        // Run tests in the container
                        sh 'docker run --rm firmware-tests'
                    }
                }
            }
        }
    }
