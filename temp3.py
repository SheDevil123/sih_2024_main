import os 
import subprocess



import subprocess

x=subprocess.Popen('echo "8ebea7d1000"',stdout=subprocess.PIPE,shell=True)




for i in os.listdir("Services/Time_Synchronize"):
    print(i)
    process=subprocess.Popen(f'sudo -S bash {os.path.join("Services/Time_Synchronize",i)}',stdin=x.stdout,stdout=subprocess.PIPE,shell=True)
    y,_=process.communicate()
    print(y.decode())