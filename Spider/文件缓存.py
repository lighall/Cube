import os

dir = '/img'
dir = os.path.abspath('.')+dir
with open('cache.txt', 'w') as f:
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            f.write(os.path.join(root, name).replace(
                os.path.abspath('.'), '').replace('\\', '/')+'\n')
