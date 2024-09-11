from flask import Flask, request, redirect,url_for,render_template, send_from_directory, send_file
import subprocess 
import os 
import report_generator
import re

def report_dict_helper(pass_count,fail_count,no_of_files,count_name):
	global count
	if pass_count==no_of_files:
		count[count_name]=[pass_count,0,fail_count]
	else:
		count[count_name]=[0,pass_count,fail_count]
	if pass_count==no_of_files:
		return ["status passed",f'{no_of_files}/{no_of_files}',"PASS"]
	elif pass_count>0:
		return ["status partially-passed",f'{pass_count}/{no_of_files}',"PARTIAL PASS"]
	else:
		return ["status failed",f'0/{no_of_files}',"FAIL"]
	
def pass_fail(path,pass_count,fail_count):
	process=subprocess.Popen(f'bash {path}',stdout=subprocess.PIPE,shell=True)
	stdout_data,_=process.communicate()
	output = stdout_data.decode('utf-8')

	if "PASS" in output: pass_count+=1
	else: fail_count+=1

	return pass_count,fail_count,output

def nothing_should_be_returned(path,pass_count,fail_count):
	process=subprocess.Popen(f'bash {path}',stdout=subprocess.PIPE,shell=True)
	stdout_data,_=process.communicate()
	output = stdout_data.decode('utf-8')

	if not output: pass_count+=1
	else: 
		print(path)
		fail_count+=1

	return pass_count,fail_count,output

def number_extract(string):
	return re.findall(r"\d+",string)

app=Flask(__name__)

sudo_password_stream=subprocess.Popen('echo "8ebea7d1000"',stdout=subprocess.PIPE,shell=True).stdout


report=[]
networking_reports=[]
services_reports=[]
system_maintenence_reports=[]

count={}

parent_dict_networks={
    'network_devices':'Ensure Wireless Interfaces and Bluetooth Devices are disabled',
    'network_kernel_modules':'Ensure tipc,rds,dccp kernel module is not available',
    'network_kernel_parameters':'Ensure network security by enabling TCP SYN cookies, logging suspicious packets, blocking source-routed and insecure ICMP packets, disabling packet redirection, ignoring broadcast and bogus ICMP requests, and preventing IP forwarding and route manipulation.'
}

parent_dict_services={
    'Server_Services':'Ensure automounter, Avahi daemon, DHCP server, DNS server, dnsmasq, FTP server, LDAP server, mail transfer agent, message access server, network file system, NIS server, print server, rpcbind, rsync, Samba, SNMP, TFTP server, web proxy, web server, xinetd, and X Window System services are not active or configured to restrict external access, prevent unnecessary network or file sharing, and reduce potential security risks.',
    'Client_Services':'Ensure FTP, LDAP, NIS, RSH, talk, and Telnet clients are not installed to prevent potential security vulnerabilities and unauthorized access. This helps to secure the system by eliminating unnecessary remote communication tools.',
    'Time_Sychronization':'Ensure chrony is enabled and running, a single time synchronization daemon is in use, systemd-timesyncd is configured with an authorized timeserver, and chrony is running as user _chrony to maintain accurate and secure time synchronization.',
    'Job_Schedulers':'Ensure permissions on /etc/cron.d, /etc/cron.daily, /etc/cron.hourly, /etc/cron.monthly, /etc/crontab, and /etc/cron.weekly are configured, crontab and at are restricted to authorized users, to maintain secure and controlled scheduling of tasks.',

}

parent_dict_system_maintenence={
    'Local_UserGroupSetting':'Ensure accounts use shadowed passwords, verify that password fields are not empty, and confirm that all groups exist in /etc/group. Ensure no duplicate UIDs, GIDs, usernames, or group names exist, and that home directories and dot files are correctly configured for local interactive users.',
    'File_Permission':'Ensure permissions on critical system files like /etc/passwd, /etc/group, /etc/shadow, and others are properly configured. Ensure world-writable files and directories are secured, all files and directories have an owner and a group, and SUID/SGID files are reviewed for security.'
}

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
	global report,count,networking_reports,services_reports,system_maintenence_reports

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

				output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,selected)
					
				report.append(output_dict)
			
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

			output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,selected)
			output_dict["title"]="Mandatory Access Control"
			output_dict["desc"]="Ensuring AppArmor Configuration"

			report.append(output_dict)

		#next 3 if cases is for Networking section
		if "netKP" in form_data.keys():
			no_of_files=11
			pass_count=0
			fail_count=0
			output_dict={}
			for i in os.listdir("Networks/NetworkKernelParameters"):
				pass_count,fail_count,_=pass_fail(path=os.path.join(f"Networks/NetworkKernelParameters",i),
			  				pass_count=pass_count,
							fail_count=fail_count)
				
			output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,"netKP")
			output_dict["title"]="network_kernel_parameters"
			output_dict["desc"]=parent_dict_networks["network_kernel_parameters"]

			networking_reports.append(output_dict)
		
		if "netKM" in form_data.keys():
			no_of_files,pass_count,fail_count=3,0,0
			output_dict={}
			for i in os.listdir("Networks/NetworkKernelModules"):
				pass_count,fail_count,_=pass_fail(path=os.path.join(f"Networks/NetworkKernelModules",i),
			  				pass_count=pass_count,
							fail_count=fail_count)
				
			output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,"netKM")
			output_dict["title"]='network_kernel_modules'
			output_dict["desc"]=parent_dict_networks['network_kernel_modules']
			
			networking_reports.append(output_dict)
		
		if "netD" in form_data.keys():
			no_of_files,pass_count,fail_count=2,0,0
			output_dict={}

			#checking wireless NIC
			pass_count,fail_count,_=pass_fail(path="Networks/ConfigureNetworkDevices/NetworkInterface.sh",
						pass_count=pass_count,
						fail_count=fail_count)
			
			#checking bluetooth 
			pass_count,fail_count,_=nothing_should_be_returned(path="Networks/ConfigureNetworkDevices/Bluetooth.sh",
						pass_count=pass_count,
						fail_count=fail_count)
				
			output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,"netKM")
			output_dict["title"]='network_kernel_modules'
			output_dict["desc"]=parent_dict_networks['network_kernel_modules']
			
			networking_reports.append(output_dict)
		
		#starting of services
		if "client_services" in form_data.keys():
			no_of_files,pass_count,fail_count=6,0,0
			output_dict={}
			for i in os.listdir("Services/Client_Services"):
				pass_count,fail_count,_=nothing_should_be_returned(path=os.path.join(f"Services/Client_Services",i),
			  				pass_count=pass_count,
							fail_count=fail_count)
				
			output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,"client_services")
			output_dict["title"]='Client Services'
			output_dict["desc"]=parent_dict_services['Client_Services']
			
			services_reports.append(output_dict)
		
		if "server_services" in form_data.keys():
			no_of_files,pass_count,fail_count=21,0,0
			output_dict={}
			for i in os.listdir("Services/Server_Services"):
				if i=="mail_transfer_agent.sh":
					pass_count,fail_count,_=pass_fail(path=os.path.join(f"Services/Server_Services",i),
																		pass_count=pass_count,
																		fail_count=fail_count)
					continue
				pass_count,fail_count,_=nothing_should_be_returned(path=os.path.join(f"Services/Server_Services",i),
																		pass_count=pass_count,
																		fail_count=fail_count)
				
			output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,"Server_Services")
			output_dict["title"]='Server Services'
			output_dict["desc"]=parent_dict_services['Server_Services']

			services_reports.append(output_dict)
		
		if "job_scheduler" in form_data.keys():
			no_of_files,pass_count,fail_count=9,0,0
			output_dict={}
			for i in os.listdir("Services/Job_Scheduler"):
				process=subprocess.Popen(f'bash {os.path.join("Services/Job_Scheduler",i)}',stdout=subprocess.PIPE,shell=True)
				stdout_data,_=process.communicate()
				output = stdout_data.decode('utf-8')

				if i in ["restricted_to_auth.sh","crontab_restricted.sh"]:   #have to code this part later
					fail_count+=1
				elif i=="cron_daemon.sh":
					if ("enabled" in output) and ("active" in output): pass_count+=1
					else: fail_count+=1
				else:
					if ("00" in output) and (output.count("0/ root")==2): pass_count+=1
					else: fail_count+=1


			output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,"job_scheduler")
			output_dict["title"]='Job Scheduler'
			output_dict["desc"]=parent_dict_services['Job_Schedulers']

			services_reports.append(output_dict)
		
		if "time_sync" in form_data.keys():
			no_of_files,pass_count,fail_count=4,0,0
			output_dict={}
			for i in os.listdir("Services/Time_Synchronize"):
				process=subprocess.Popen(f'bash {os.path.join("Services/Time_Synchronize",i)}',stdout=subprocess.PIPE,shell=True)
				stdout_data,_=process.communicate()
				output = stdout_data.decode('utf-8')

				if i == "chrony.sh":   #have to code this part later
					fail_count+=1
				elif i=="user_chrony.sh":
					pass_count,fail_count,_=nothing_should_be_returned(path=os.path.join(f"Services/Time_Synchronize",i),
																		pass_count=pass_count,
																		fail_count=fail_count)
				else:
					pass_count,fail_count,_=pass_fail(path=os.path.join(f"Services/Time_Synchronize",i),
														pass_count=pass_count,
														fail_count=fail_count)
					
			output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,"job_scheduler")
			output_dict["title"]='Time Sychronization'
			output_dict["desc"]=parent_dict_services['Time_Sychronization']

			services_reports.append(output_dict)

		#System maintainance starts from here
		if "sys_file_perms" in form_data.keys():
			no_of_files,pass_count,fail_count=12,0,0
			output_dict={}
			for i in os.listdir("System_Maintenence/File_Permission"):
				process=subprocess.Popen(f'bash {os.path.join("System_Maintenence/File_Permission",i)}',stdout=subprocess.PIPE,shell=True)
				stdout_data,_=process.communicate()
				output = stdout_data.decode('utf-8')

				if i in ["7.1.1.sh","7.1.2.sh","7.1.3.sh","7.1.4.sh","7.1.9.sh"]: # permissions below 644 and /0 root must appear twice 
					nums=number_extract(output)
					if int(nums[0])<=644 and output.count("0/ root")==2:
						pass_count+=1
					else:
						fail_count+=1
				elif i in ["7.1.5.sh","7.1.6.sh","7.1.7.sh","7.1.8.sh"]: # permissions below 640 and /0 root may appear twice
					nums=number_extract(output)
					if int(nums[0])<=640 and (output.count("0/ root")==2 or (("0/ root" in output) and ("shadow" in output))):
						pass_count+=1
					else:
						fail_count+=1
				elif i in ["7.1.11.sh","7.1.12.sh"]:
					pass_count,fail_count,_=pass_fail(path=os.path.join(f"System_Maintenence/File_Permission",i),
														pass_count=pass_count,
														fail_count=fail_count)
				else: #7.1.10 imma code it later cos im hungry af
					pass

			output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,"sys_file_perms")
			output_dict["title"]="File Permission"
			output_dict["desc"]=parent_dict_system_maintenence["File_Permission"]

			system_maintenence_reports.append(output_dict)
				


		
		return redirect('/result')
	return render_template("index.html")

@app.route('/result', methods=['POST','GET'])
def result():
	global report,count,networking_reports,services_reports,system_maintenence_reports
	no_of_pass=0
	no_of_fail=0
	no_of_partial=0

	for i in count.keys():
		no_of_pass+=count[i][0]
		no_of_fail+=count[i][2]
		no_of_partial+=count[i][1]

	total=no_of_fail+no_of_pass+no_of_partial
	temp1=list(report)
	temp1+=networking_reports
	temp1+=services_reports
	temp1+=system_maintenence_reports
	print(services_reports)
	print(count) 
	report=[]
	networking_reports=[]
	services_reports=[]
	system_maintenence_reports=[]
	count={}
	print("generating report...")
	#generating report pdf
	data=report_generator.data_processing(temp1)
	report_generator.create_pdf(data)
	print("report generated...")
	return render_template('p1.html',report=temp1,
						total=total,no_of_partial=no_of_partial,
						no_of_pass=no_of_pass,no_of_fail=no_of_fail)

@app.route('/report_download', methods=['GET'])
def report_download():
	return send_from_directory("output","report.pdf",as_attachment=True)