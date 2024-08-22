import os 
import subprocess



process=subprocess.Popen(f'bash {os.path.join("partition_checks/tmp","tmp.sh")}',stdout=subprocess.PIPE,shell=True)
output_dict={}
stdout_data,_=process.communicate()
output = stdout_data.decode('utf-8')

print(bool(output))