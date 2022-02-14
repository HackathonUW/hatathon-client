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

def runProgram(testid: int, command: str, **kwargs) -> any:
    """
    Run the provided command, noting its test id.

    :param testid: The test id.
    :param command: The command to run.
    :param stdin: optional stdin to pass to the command.

    :return: The output of the command.
    """

    p = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    if ("stdin" in kwargs):
        #print(kwargs.get("stdin"))
        out, err = p.communicate(input=kwargs.get("stdin").encode())
    else:
        out, err = p.communicate()

    data = [testid, p.returncode, out.decode(), err]
    return data;

def setup_run(project_id: int, session_id: str) -> any:
    """
    Sets up the run
    
    Returns json object of project, or None on error.
    """

    email = "xuegeoff@gmail.com"

    try:
        r = requests.post('https://hatathon-backend.herokuapp.com/run', json={'uuid':session_id, 'projectid':project_id, 'email':email})

        if (r.status_code != 200):
            print(f"Server responded to SETUP RUN request for {session_id} with error code.")
            return None
        else:
            return r.status_code
    except:
        print("Error making request for setup run.")
        return None

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


def get_output(test) -> str:
    """Get the output for the test."""
    #https://hatathon-backend.herokuapp.com/static/{output}

    if ('output' not in test):
        print("Error: No file with expected output specified. Test must have an \"output\" field.")
    
    if (test['output'] is None):
        print("No output for test.")
        return None

    else:
        url = f"https://hatathon-backend.herokuapp.com{requests.utils.quote(test['output'])}"
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
            print(f"Server responded to request for {session_id} with error code {r.status_code}.")

    except:
        print("Error making request for project details.")

"""
Main function
"""
if __name__ == '__main__':
    print(Style.BRIGHT+"Crowd Code Test Runner"+Style.RESET_ALL)

    if (len(sys.argv) != 3 or '--help' in sys.argv or '-h' in sys.argv):
        print("Usage: runner.py <project_id> <session_id>")
        sys.exit(1)

    project_id = sys.argv[1]
    session_id = sys.argv[2]

    setup_run(project_id, session_id)

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

        testinput = get_input(test)
        testoutput = get_output(test)
        #print(testoutput)
        
        #print(f"Command: {test['command']}")
        #print("-----------------------------------------------------")
        #print(Style.BRIGHT+"INPUT"+Style.RESET_ALL+'\n'+get_input(test))
        #print("-----------------------------------------------------")
        #print(Style.BRIGHT+"EXPECTED OUTPUT"+Style.RESET_ALL+'\n'+get_output(test))
        #print("-----------------------------------------------------")

        run = {}
        if (testinput is not None):
            if (test['input'] is not None):
                run = runProgram(test['pid'], test['command'], stdin=test['input'])
            else:
                run = runProgram(test['pid'], test['command'])
        returncode = run[1]

        # send results to server
        if returncode == 0:
            if testoutput is not None:
                if run[2] == testoutput:
                    return_results(session_id, test['pid'], STATUS['SUCCESS'])
                    print("success")
                else:
                    #print(testoutput)
                    #print(run[2])
                    return_results(session_id, test['pid'], STATUS['FAIL'])
                    print("fail 2")
            else:
                return_results(session_id, test['pid'], STATUS['SUCCESS'])
                print("success")

        else:
            return_results(session_id, test['pid'], STATUS['FAIL'])
            print("fail")
