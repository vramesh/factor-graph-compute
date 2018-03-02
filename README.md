# factor-graph-compute
## Setup
To set up:
1. install Pipenv: `pip install pipenv`
2. To install any new packages (for example, numpy): `pipenv install numpy`
3. To run a python script with all dependencies (for example: main.py): `pipenv run python main.py` 
4. You can view installed dependencies in `Pipfile`
5. To start pipenv shell: `pipenv shell`
6. To check your set up worked - running below commands should output python 3.6:
```  
pipenv shell
python --version
```

## Style Checking
1. If you are already in the pipenv shell (`pipenv shell`), just run: `pylint <file or directory>`
2. If you are not in the pipenv shell, you can run: `pipenv run pylint <file or directory>` 
