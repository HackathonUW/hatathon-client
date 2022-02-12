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

import random # for mockup

# Colored terminal text
from colorama import init, Style, Fore
init()

# uuid, project id, email

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


def get_project(session_id: str) -> any:
    """
    Get the project by session id.
    
    Returns json object of project, or None on error.
    """
    try:
        r = requests.post('https://hatathon-backend.herokuapp.com/get', json={'type':'results', 'uuid':session_id})

        if (r.status_code != 200):
            print(f"Server responded to request for {session_id} with error code.")
            return None
        else:
            return r.json()
    except:
        print("Error making request for project details.")
        return None
'''
def get_testcases(project: json):
    """
    Get the testcases by id.
    
    param project: The json representation of the project to get the testcases from.
    Returns json object of test cases, or None on error.
    """
    proj_id = None

    first_test = json.loads(project)[0]
    proj_id: int = first_test['project']
    try:
        pass
    except:
        print("Cannot extract project id from empty project.")
        return None

    try:
        assert proj_id is not None;
        r = requests.post('https://hatathon-backend.herokuapp.com/get', json={'type':'testcases', 'proj_id':proj_id})
        print(json.dumps(r, indent=4, sort_keys=True))
        if (r.status_code != 200):
            print(f"Server responded to request for {session_id} with error code.")
            return None
        else:
            return r.json()
    except:
        print("Error making request for project details.")
        return None
'''

def get_input(test) -> str:
    """Get the input for the test."""
    #https://hatathon-backend.herokuapp.com/static/{input}

    if ('input' not in test):
        print("Error: No input file specified. Test must have an \"input\" field.")
    
    if (test['input'] is None):
        print("No input for test.")
        return ""
    else:
        url = f"https://hatathon-backend.herokuapp.com{requests.utils.quote(test['input'])}"
        r = requests.get(url)

        if (r.status_code != 200):
            print(f"Server responded to request for {session_id} with error code.")
            return None
        
        return r.content.decode()

def get_input(test) -> str:
    """Get the input for the test."""
    #https://hatathon-backend.herokuapp.com/static/{input}

    if ('input' not in test):
        print("Error: No input file specified. Test must have an \"input\" field.")
    
    if (test['input'] is None):
        print("No input for test.")
        return None
    
    else:
        url = f"https://hatathon-backend.herokuapp.com{requests.utils.quote(test['input'])}"
        r = requests.get(url)

        if (r.status_code != 200):
            print(f"Server responded to request for {session_id} input with error code {r.status_code}.")
            return None
        
        return r.content.decode()

def get_output(test) -> str:
    """Get the output for the test."""
    #https://hatathon-backend.herokuapp.com/static/{output}

    if ('output' not in test):
        print("Error: No file with expected output specified. Test must have an \"output\" field.")
    
    if (test['output'] is None):
        print("No output for test.")
        return None

    else:
        url = f"https://hatathon-backend.herokuapp.com{requests.utils.quote(test['input'])}"
        r = requests.get(url)

        if (r.status_code != 200):
            print(f"Server responded to request for {session_id} expected output with error code {r.status_code}.")
            return None
        
        return r.content.decode()

STATUS = {
    "SUCCESS": 0,
    "FAIL": 1,
    "RUNNING": 2,
    "WAITING": 3,
}

def return_results(session_id: str, test_id: int, status: int):
    """
    Send results for a given test to the server.
    """
    try:
        r = requests.post('https://hatathon-backend.herokuapp.com/edit', json={'type':'res', 'uuid':session_id, 'testid':test_id, 'status':status})

        if (r.status_code != 200):
            print(f"Server responded to request for {session_id} with error code.")

    except:
        print("Error making request for project details.")

"""
Main function
"""
if __name__ == '__main__':
    print(Style.BRIGHT+"Crowd Code Test Runner"+Style.RESET_ALL)

    if (len(sys.argv) != 2 or '--help' in sys.argv or '-h' in sys.argv):
        print("Usage: runner.py <session_id>")
        sys.exit(1)

    session_id = sys.argv[1]

    project = get_project(session_id)
    if (project is None):
        print(f"Fatal error getting project {session_id}, exiting.")
        exit(1)

    print(f"Loaded project {session_id}.")

    
    #print(json.dumps(project, indent=4, sort_keys=True))
    #print(f"Loaded project {project['name']}")

    #testcases = get_testcases(project)

    # iterate all tests with test_iterator(project)
    print(f"Running {len(project)} tests.")

    print('\n'+Style.BRIGHT+"===== TEST CASES ====="+Style.RESET_ALL)

    for test in iter(project):
        if (test['disabled']):
            continue
        return_results(session_id, test['pid'], STATUS['RUNNING'])

        print(f"{'['+str(test['pid'])+']':<6}{test['command']}\t{test['author']}")
        #print(f"Command: {test['command']}")
        print("-----------------------------------------------------")
        print(Style.BRIGHT+"INPUT"+Style.RESET_ALL+'\n'+get_input(test))
        print("-----------------------------------------------------")
        print(Style.BRIGHT+"EXPECTED OUTPUT"+Style.RESET_ALL+'\n'+get_output(test))
        print("-----------------------------------------------------")

        return_results(session_id, test['pid'], STATUS['FAIL'])


        # get input for test

        # run test

        # diff output against expected output

        # send result to server
        
    #for testcase in testcases:
    #    runProgram()
    #print(runProgram(1,"echo Hello World"))
    #print(runProgram(2,"cat", stdin="Hello World"))


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
    


