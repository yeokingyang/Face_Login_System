# FaceLockDjango
Python 3.9.7

Pre-requisite:
1. Install Python https://www.python.org/downloads/ --> Preferably 3.9.7
        Tick Install to path (so that we can use the command in cmd)
        Choose the default installation
        Remove the MAX_PATH limit
2. Open cmd and check python version
	      python --version
3. Install pip env
	      pip3 install pipenv
4. Download Visual Code from https://code.visualstudio.com/
    	  Search and install Python (ms-python.python, created by Microsoft, has IntelliSense (Pylance)...) Extension in the VS Code

How to install:
1. Clone repo to a new folder
2. Open CMD in the new folder
3. Create an Django environment
	      pipenv install django
4. Get the environment folder
        pipenv --venv
        Copy the result path
5. Open the folder directly to VS Code from CMD
	      code .
6. Search for interpreter --> Enter interpreter path...
	      Paste the result path --> append "\bin\python" --> Enter
7. Search for interpreter again --> Select pipenv with the same name as the Project Directory
