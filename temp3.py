import os 
import subprocess



import subprocess

x=subprocess.Popen('echo "8ebea7d1000"',stdout=subprocess.PIPE,shell=True)




for i in os.listdir("Access_Control/User_acc_env/root_sys_acc_env"):
    print(i)
    process=subprocess.Popen(f'sudo -S bash {os.path.join("Access_Control/User_acc_env/root_sys_acc_env",i)}',stdin=x.stdout,stdout=subprocess.PIPE,shell=True)
    y,_=process.communicate()
    print(y.decode())