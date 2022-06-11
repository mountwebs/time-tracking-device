import os
import sys
import argparse
from dotenv import load_dotenv
import yaml
import toggl_api
from toggl_api import TogglApi

load_dotenv()
TOGGL_API_KEY = os.getenv('TOGGL_API_KEY')

togglApi = TogglApi(TOGGL_API_KEY)



def getConfig (configPath):
    with open(configPath, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            if (not config or not config['projects']): return False
            return config
        except yaml.YAMLError as exc:
            print(exc)
            return false

def getProject (config, projectNum):
    if(projectNum >= len(config['projects'])): 
        raise ValueError("Project number is not valid")
    return config['projects'][projectNum] 

class TogglCli:

    def __init__(self):
        self.config = getConfig('toggl-projects.yaml')

        parser = argparse.ArgumentParser(
            description='Toggl Cli',
            usage='''<command> [<args>]
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()


    def start(self):
        parser = argparse.ArgumentParser(
            description='Start project')
        parser.add_argument("project", help="Add the number of the project you want to start",
                    type=int)
        args = parser.parse_args(sys.argv[2:])
        togglApi.startProject(getProject(self.config, args.project))

    def stop(self):
        togglApi.stop()
    
    def workspaces(self):
        togglApi.getWorkspaces()

    def projects(self):
        parser = argparse.ArgumentParser(
            description='Get project info')
        parser.add_argument("workspace", help="Workspace id",
                    type=int)
        args = parser.parse_args(sys.argv[2:])
        togglApi.getProjects(args.workspace)


if __name__ == '__main__':
    TogglCli()    
