import json
import os
path = "./temp/"

f = os.listdir(path)

n = 0
for i in f:
    old_name = path+f[n];
    new_name = path+'test'+str(n+1)+'.json'
    os.rename(old_name,new_name)
    print(old_name,'======>',new_name)
    n+=1
