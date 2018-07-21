# Hermes
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

## To-Dos
1. Branch new_ui has stop_node that has the following error for thread 1-3.

```  
Exception in thread Thread-1:
Traceback (most recent call last):
  File "/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/threading.py", line 916, in _bootstrap_inner
    self.run()
  File "/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/threading.py", line 864, in run
    self._target(*self._args, **self._kwargs)
  File "/Users/antsai/Desktop/hermes/branch/factor-graph-compute/v1.0/redis_broker.py", line 43, in start_subscriber
    message = self.subscribers[subscriber_id]["redis_pubsub"].get_message() #this line is buggy?
  File "/usr/local/lib/python3.6/site-packages/redis/client.py", line 2513, in get_message
    response = self.parse_response(block=False, timeout=timeout)
  File "/usr/local/lib/python3.6/site-packages/redis/client.py", line 2426, in parse_response
    'pubsub connection not set: '
RuntimeError: pubsub connection not set: did you forget to call subscribe() or psubscribe()?
```
2. In progress, UI unintuitive, since users have to name a file a particular way and have manual input functions
3. Pipenv is probably out of date, make list of dependencies through virtualenv testing
4. get rid of manual countdown
5. Tearing down and bring server back up results have lag/fails first time?
