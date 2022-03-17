import sys
import os

def move_to_github(options):

    SYS_DIV_SYM = os.path.join('@', '@')[1]
    
    def copy(copy_from, to_dir):
        path = copy_from
        if path.find(SYS_DIV_SYM) != -1:
            path = path.strip().split(SYS_DIV_SYM)[-1]
        print(f'Copying file {path} ...')
        with open(copy_from, 'r') as cf:
            with open(os.path.join(to_dir, path), 'w') as tar:
                tar.write(cf.read())

    def mkdir(dir):
        if not os.path.exists(dir):
            print(f'Creating directory {dir} ...')
            os.mkdir(dir)
        print(f'Directory {dir} already exists')

    # def copy(copy_from, to_dir):
    #     os.system(f'cp {copy_from} {to_dir}')

    # def mkdir(dir):
    #     print(os.path.isdir(dir))
        # os.system(f'mkdir {dir}')

    def run():
        for actions in options:
            mkdir(actions['to-dir'])

            for files in actions['copy-from']:
                copy(files, actions['to-dir'])
        print('Successfully moved to github repository!')

    run()


if __name__ == '__main__':
    move_to_github([
        {
            'copy-from': [
                'GetProblem.py',
                'IO.py',
                'main.py',
                'Msg.py'
            ],
            'to-dir': '/home/revival0728/code/local-testing-tool/src/'
        },
        {
            'copy-from': [
                'requirements.txt'
            ],
            'to-dir': '/home/revival0728/code/local-testing-tool/'
        }
    ])
