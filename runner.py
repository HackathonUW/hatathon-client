"""
Team Test Runner

Usage:
  runner.py <id> [--debug]
"""
import sys
import io
import tempfile
import json
import requests
import subprocess

def runProgram(testid: int, command: str, **kwargs) -> json:
    """
    Run the provided command, noting its test id.

    :param testid: The test id.
    :param command: The command to run.
    :param stdin: optional stdin to pass to the command.

    :return: The output of the command.
    """

    p = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    if ("stdin" in kwargs):
        print(kwargs.get("stdin"))
        out, err = p.communicate(input=kwargs.get("stdin").encode())
    else:
        out, err = p.communicate()

    data = {}
    data['test_id'] = testid
    data['returncode'] = p.returncode
    data['stdout'] = out
    data['stderr'] = err

    return data;


def get_project_by_id(id: int) -> json:
    """Get the project by id."""
    r = requests.post('https://hatathon-backend.herokuapp.com/get', json={'type':'testcases', 'proj_id':id})
    return r.json()

    
if __name__ == '__main__':
    if (len(sys.argv) != 2 or sys.argv[1] == '--help' or sys.argv[1] == '-h'):
        print("Usage: runner.py <id>")
        sys.exit(1)

    print(f"Running project {sys.argv[1]}")

    print(get_project_by_id(sys.argv[1]))

    testcases = []

    for 
    print(runProgram(1,"echo Hello World"))
    print(runProgram(2,"cat", stdin="Hello World"))


# get request to 




def test_url_from_id(id):
    return "https://demo.noguera.dev/api/{}".format(SERVER, id)

def get_by_id(id):
    response = requests.get(TESTURL)
    return response.json()

def parse_project(project):
    """Parse the project file."""

def parse_test(test):
    """Parse the test."""

def run(command):
    """Run the specified test or project."""
    subprocess = subprocess.Popen("echo Hello World", shell=True, stdout=subprocess.PIPE)
    subprocess_return = subprocess.stdout.read()
    print(subprocess_return)
    


