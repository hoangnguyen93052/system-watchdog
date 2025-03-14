import os
import subprocess
import json
import time
import yaml
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DevOpsAutomation:
    def __init__(self, project_name):
        self.project_name = project_name
        self.repo_url = ""
        self.branch_name = "main"
        self.build_logs = []

    def configure_repo(self, url, branch):
        self.repo_url = url
        self.branch_name = branch
        logging.info(f'Repository configured: {self.repo_url}, Branch: {self.branch_name}')

    def clone_repo(self):
        try:
            logging.info(f'Cloning repository {self.repo_url}...')
            subprocess.run(['git', 'clone', '-b', self.branch_name, self.repo_url], check=True)
            logging.info('Repository cloned successfully.')
        except subprocess.CalledProcessError as e:
            logging.error(f'Error cloning repository: {e}')
            raise

    def install_dependencies(self, requirements_file='requirements.txt'):
        try:
            logging.info(f'Installing dependencies from {requirements_file}...')
            subprocess.run(['pip', 'install', '-r', requirements_file], check=True)
            logging.info('Dependencies installed successfully.')
        except subprocess.CalledProcessError as e:
            logging.error(f'Error installing dependencies: {e}')
            raise

    def run_tests(self, test_command='pytest'):
        try:
            logging.info('Running tests...')
            result = subprocess.run(test_command.split(), check=True, capture_output=True)
            self.build_logs.append(result.stdout.decode())
            logging.info('Tests completed successfully.')
        except subprocess.CalledProcessError as e:
            logging.error(f'Tests failed: {e.stderr.decode()}')
            self.build_logs.append(e.stderr.decode())
            raise

    def build_project(self):
        try:
            logging.info('Building project...')
            result = subprocess.run(['python', 'setup.py', 'install'], check=True, capture_output=True)
            self.build_logs.append(result.stdout.decode())
            logging.info('Project built successfully.')
        except subprocess.CalledProcessError as e:
            logging.error(f'Build failed: {e.stderr.decode()}')
            self.build_logs.append(e.stderr.decode())
            raise

    def deploy(self, deployment_script='deploy.sh'):
        try:
            logging.info('Deploying project...')
            subprocess.run(['bash', deployment_script], check=True)
            logging.info('Project deployed successfully.')
        except subprocess.CalledProcessError as e:
            logging.error(f'Deployment failed: {e.stderr.decode()}')
            raise

    def log_build(self):
        log_file = f'build_log_{self.project_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        with open(log_file, 'w') as f:
            f.write("\n".join(self.build_logs))
        logging.info(f'Build log saved to {log_file}')

    def run_pipeline(self):
        self.clone_repo()
        self.install_dependencies()
        self.run_tests()
        self.build_project()
        self.deploy()
        self.log_build()

if __name__ == '__main__':
    # Example project configuration
    project = DevOpsAutomation('example_project')
    project.configure_repo('https://github.com/user/example_project.git', 'main')
    project.run_pipeline()