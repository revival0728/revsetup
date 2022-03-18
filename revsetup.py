import os
import sys
import json
import requests

def setup(username, repo):

    print(f'Setting up {username}/{repo} ...')

    class SetupSytanxErrors(Exception): pass

    githubRawUrl = f'https://raw.githubusercontent.com/{username}/{repo}/master'

    def processPath(gitPath):
        gra = GRAMMER['@File']['#Path']
        if gitPath[0:len('@Repo')] != '@Repo':
            if gitPath[0] == '/':
                gitPath = '/revsetup' + gitPath
            else:
                gitPath = '/revsetup/' + gitPath
        for keyword in gra:
            gitPath = gitPath.replace(keyword, gra[keyword])
        return gitPath

    def getFile(gitPath):
        return requests.get(githubRawUrl+processPath(gitPath)).text

    def AtGet(path, gitPath):
        content = getFile(gitPath)
        print(f'Getting file {processPath(gitPath)} ...')
        name = gitPath.strip().split('/')[-1]
        with open(os.path.join(path, name), 'w') as f:
            f.write(content)

    def AtNew(path, gitPath):
        print(f'Creating file {gitPath} ...')
        name = gitPath.strip().split('/')[-1]
        with open(os.path.join(path, name), 'w') as f:
            f.write('\n')

    def AtFile(nowPath, fileConfig):
        for code in fileConfig[1:]:
            if not code in GRAMMER['@File']:
                raise SetupSytanxErrors
            if code == '@Get':
                AtGet(nowPath, fileConfig[0])
            if code == '@New':
                AtNew(nowPath, fileConfig[0])


    def recurPathTree(nowPath, config):
        if '@File' in config:
            for fileConfig in config['@File']:
                AtFile(nowPath, fileConfig)
        for dir in config:
            if dir == '@File':
                continue
            nextPath = os.path.join(nowPath, dir)
            if not os.path.exists(nextPath):
                print(f'Creating directory {nextPath} ...')
                os.mkdir(nextPath)
            print(f'Directory {nextPath} already exists.')
            recurPathTree(nextPath, config[dir])

    def getSetupJson():
        return json.loads(requests.get(githubRawUrl+'/revsetup/revsetup.json').text)

    GRAMMER = {
        '@File': {
            '@Get': AtGet,
            '@New': AtNew,
            '#Path': {
                '@Repo': ''
            }
        }
    }

    configFile = getSetupJson()

    for dir in configFile:
        if dir[0] != '@':
            recurPathTree(dir, configFile[dir])
            break

    print(f'Successfully setup {username}/{repo}!')

if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) != 1:
        print('Argument Error')
        exit(1)
    setup(*argv[0].strip().replace('https://github.com/', '').split('/'))
