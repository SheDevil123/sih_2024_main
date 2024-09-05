from flask import Flask, request, redirect,url_for,render_template, send_from_directory, send_file
import subprocess 
import os 
import report_generator

def report_dict_helper(pass_count,fail_count,no_of_files):
	if pass_count==no_of_files:
		return ["status passed",f'{no_of_files}/{no_of_files}',"PASS"]
	elif pass_count>0:
		return ["status partially-passed",f'{pass_count}/{no_of_files}',"PARTIAL PASS"]
	else:
		return ["status failed",f'0/{no_of_files}',"FAIL"]



app=Flask(__name__)

sudo_password_stream=subprocess.Popen('echo "8ebea7d1000"',stdout=subprocess.PIPE,shell=True).stdout


report=[]

count={}
filesystem_check_data={
    'cramfs.sh':'Ensure cramfs kernel module is not available',
    'freevxfs.sh':'Ensure freevxfs kernel module is not available',
    'hfs.sh':'Ensure hfs kernel module is not available ',
    'hfsplus.sh':'Ensure hfsplus kernel module is not available',
    'jffs2.sh':'Ensure jffs2 kernel module is not available ',
    'squashfs.sh':'Ensure squashfs kernel module is not available ',
    'udf.sh':' Ensure udf kernel module is not available ',
    'usbstorage.sh':' Ensure usb-storage kernel module is not available '
}


partition_check_data={
	"tmp":"ensure tmp is separate partition and nodev, nosuid, noexec options are set",
	"devshm":"ensure /dev/shm is separate partition and nodev, nosuid, noexec options are set",
	"home":"ensure home is separate partition and nodev, nosuid options are set",
	"var":"ensure var is separate partition and nodev, nosuid options are set",
	"vartmp":"ensure /var/tmp is separate partition and nodev, nosuid, noexec options are set",
	"varlog":"ensure /var/log is separate partition and nodev, nosuid, noexec options are set",
	"varlogaudit":"ensure /var/log/audit is separate partition and nodev, nosuid, noexec options are set",
}

AppArmor={
    'install_check':'Ensure AppArmor is installed',
    'bootloader_configuration':'Ensure AppArmor is enabled in the bootloader configuration',
    'complain_enforcing':'Ensure all AppArmor Profiles are in enforce or complain mode and AppArmor Profiles are enforcing ',
}

@app.route('/', methods=['GET', 'POST'])
def upload():
	global report,count
	if request.method == 'POST':
		kernal_modules=request.form.get("cramfs")
		form_data=dict(request.form.items())
		print(form_data)

		if kernal_modules:
			pass_count=0
			fail_count=0

			for i in os.listdir("filesystem_checks"):
				process=subprocess.Popen(f'bash {os.path.join("filesystem_checks",i)}',stdout=subprocess.PIPE,shell=True)
				output_dict={}
				stdout_data,_=process.communicate()
				output = stdout_data.decode('utf-8')

				#pass or fail
				if "PASS" in output:
					output_dict["pof"]=["status passed",'1/1',"PASS"]
					pass_count+=1
				else:
					output_dict["pof"]=["status failed",'0/1',"FAIL"]
					fail_count+=1
				
				#adding description 
				output_dict["desc"]=filesystem_check_data[i]
				output_dict["title"]="Configure Filesystem Kernel Modules"

				report.append(output_dict)

			count["km"]=[pass_count,0,fail_count]

		#partition checking
		for selected in partition_check_data.keys():
			if selected in form_data.keys():
				pass_count=0
				fail_count=0
				no_of_files=len(os.listdir(f"partition_checks/{selected}"))

				#checking if partition is available
				process=subprocess.Popen(f'bash {os.path.join(f"partition_checks/{selected}",f"{selected}.sh")}',stdout=subprocess.PIPE,shell=True)
				output_dict={}
				stdout_data,_=process.communicate()
				output = stdout_data.decode('utf-8')

				#adding description 
				output_dict["desc"]=partition_check_data[selected]
				output_dict["title"]="Configure Filesystem Partitions"
				if output:
					pass_count+=1
					
					for i in os.listdir(f"partition_checks/{selected}"):
						if i!=f"{selected}.sh":
							process=subprocess.Popen(f'bash {os.path.join(f"partition_checks/{selected}",i)}',stdout=subprocess.PIPE,shell=True)
							stdout_data,_=process.communicate()
							output = stdout_data.decode('utf-8')
						else:
							continue
						
						#pass or fail
						if output:
							fail_count+=1
						else:
							pass_count+=1
				else:
					fail_count=no_of_files

				output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files)
					
				report.append(output_dict)
				if pass_count==no_of_files:
					count[selected]=[pass_count,0,fail_count]
				else:
					count[selected]=[0,pass_count,fail_count]
			
		#apparmor
		if "apparmor" in form_data.keys():
			no_of_files=3
			pass_count=0
			fail_count=0
			output_dict={}

			for i in os.listdir(f"apparmor"):
				if i=="complain_enforcing.sh":
					process=subprocess.Popen(f'sudo -S bash {os.path.join("apparmor",i)}',stdin=sudo_password_stream,stdout=subprocess.PIPE,shell=True)
					stdout_data,_=process.communicate()
					output = stdout_data.decode('utf-8')
					output=output.split('\n')
					print(output)
					#unconfined profiles
					temp=0
					for j in output:
						if ("processes are unconfined" in j):
							num=[int(k) for k in j.split() if k.isdigit()][0] 
							temp+=num
							print("temp",temp)

						if ("kill mode" in j) or ("unconfined mode") in j:
							temp+=[int(k) for k in j.split() if k.isdigit()][0]
							print("temp",temp)
					if temp==0:
						pass_count+=1
					else:
						fail_count+=1

				elif i=="install_check.sh":
					process=subprocess.Popen(f'bash {os.path.join(f"apparmor",i)}',stdout=subprocess.PIPE,shell=True)
					stdout_data,_=process.communicate()
					output = stdout_data.decode('utf-8')
					output=output.count("installed")

					if output==2:
						pass_count+=1
					else:
						fail_count+=1
					
				else:
					process=subprocess.Popen(f'bash {os.path.join(f"apparmor",i)}',stdout=subprocess.PIPE,shell=True)
					stdout_data,_=process.communicate()
					output = stdout_data.decode('utf-8')

					if output:
						fail_count+=1
					else:
						pass_count+=1

			output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files)
			output_dict["title"]="Mandatory Access Control"
			output_dict["desc"]="Ensuring AppArmor Configuration"

			report.append(output_dict)

			if pass_count==no_of_files:
				count[selected]=[pass_count,0,fail_count]
			else:
				count[selected]=[0,pass_count,fail_count]

		return redirect('/result')
	return render_template("index.html")

@app.route('/result', methods=['POST','GET'])
def result():
	global report,count,count
	no_of_pass=0
	no_of_fail=0
	no_of_partial=0

	for i in count.keys():
		no_of_pass+=count[i][0]
		no_of_fail+=count[i][2]
		no_of_partial+=count[i][1]

	total=no_of_fail+no_of_pass+no_of_partial
	temp1=list(report)
	print(count)
	report=[]
	count={}

	#generating report pdf
	data=report_generator.data_processing(temp1)
	report_generator.create_pdf(data)
	
	return render_template('p1.html',report=temp1,
						total=total,no_of_partial=no_of_partial,
						no_of_pass=no_of_pass,no_of_fail=no_of_fail)

@app.route('/report_download', methods=['GET'])
def report_download():
	return send_from_directory("output","report.pdf",as_attachment=True)