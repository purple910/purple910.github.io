import os

exclude = ['_media', '.git']

sidebar = '_sidebar.md'
navbar = '_navbar.md'

listFile = os.listdir(os.getcwd())

data = {}

for file in listFile:
    if os.path.isdir(file) and not exclude.count(file):
        lines = []
        # * [流媒体组件功能对接手册](app/流媒体组件功能对接手册.md)
        path = os.getcwd()+'\\'+file
        # if os.path.exists(path):
        #     with open(path, mode='r') as f:
        #         f.readline()
        # print(line)

        mds = os.listdir(path)
        with open(path+'\\'+sidebar, mode='w', encoding='utf-8') as f:
            for md in mds:
                if md != sidebar:
                    line = '* ['+md.replace('.md', '')+']('+file+'/'+md+')\n'
                    lines.append(line)
                    f.write(line)
        data[file] = lines


with open(os.getcwd()+'\\'+sidebar, mode='w', encoding='utf-8') as f:
    for item in data:
        if len(data[item]) > 0:
            f.write('* '+item+'\n')
            for line in data[item]:
                f.write('  '+line)
            f.write('\n\n')

with open(os.getcwd()+'\\'+navbar, mode='w', encoding='utf-8') as f:
    for item in data:
        if len(data[item]) > 0:
            f.write('* '+item+'\n')
            for line in data[item]:
                f.write('  '+line)
            f.write('\n\n')