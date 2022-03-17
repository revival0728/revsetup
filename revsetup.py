import os
import sys
import json
import github

def setup(username, repo):

    print(f'{username}/{repo}')

    class SetupSytanxErrors(Exception): pass

    git = github.Github()

    rep = git.get_repo(f'{username}/{repo}')
        

    def processPath(gitPath):
        gra = GRAMMER['@File']['#Path']
        if gitPath[0:len('@Repo')] != '@Repo':
            if gitPath[0] == '/':
                gitPath = '/revsetup' + gitPath
            else:
                gitPath = '/revsetup/' + gitPath
        for keyword in gra:
            gitPath = gitPath.replace(keyword, gra[keyword])
        print(gitPath)
        return gitPath

    def getFile(gitPath):
        return rep.get_contents(processPath(gitPath))

    def AtGet(path, gitPath):
        content = getFile(gitPath)
        name = gitPath.strip().split('/')[-1]
        with open(os.path.join(path, name), 'w') as f:
            f.write(content.decoded_content.decode('utf-8'))

    def AtNew(path, gitPath):
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
                os.mkdir(nextPath)
            recurPathTree(nextPath, config[dir])

    def getSetupJson():
        return json.loads(rep.get_contents('/revsetup/revsetup.json')
                .decoded_content
                .decode('utf-8')
        )

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

    print(configFile)

    for dir in configFile:
        if dir[0] != '@':
            recurPathTree(dir, configFile[dir])
            break

if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) != 1:
        print('Argument Error')
        exit(1)
    try:
        setup(*argv[0].strip().replace('https://github.com/', '').split('/'))
    except github.GithubException.UnknownObjectException:
        print('revsetup.json passed the wrong arguments')
        exit(1)
