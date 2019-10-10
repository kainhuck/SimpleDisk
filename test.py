import os
import shutil

path = "/SimpTestDir/testDir2/新建文件夹"

print(os.listdir(path))

try:
    os.removedirs(path)
except:
    shutil.rmtree(path)