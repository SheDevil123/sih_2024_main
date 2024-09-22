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
	
def pass_fail(path,pass_count,fail_count,sudo=False):
	if sudo:
		process=subprocess.Popen(f'sudo -S bash {path}',stdin=sudo_password_stream,stdout=subprocess.PIPE,shell=True)
	else:
		process=subprocess.Popen(f'bash {path}',stdout=subprocess.PIPE,shell=True)
	stdout_data,_=process.communicate()
	output = stdout_data.decode('utf-8')

	if "PASS" in output: pass_count+=1
	else: fail_count+=1

	return pass_count,fail_count,output

def nothing_should_be_returned(path,pass_count,fail_count,sudo=False):
	if sudo:
		process=subprocess.Popen(f'sudo -S bash {path}',stdin=sudo_password_stream,stdout=subprocess.PIPE,shell=True)
	else:
		process=subprocess.Popen(f'bash {path}',stdout=subprocess.PIPE,shell=True)
	stdout_data,_=process.communicate()
	output = stdout_data.decode('utf-8')

	if not output: pass_count+=1
	else: 
		fail_count+=1

	return pass_count,fail_count,output

def number_extract(string):
	return re.findall(r"\d+",string)

app=Flask(__name__)

sudo_password_stream=subprocess.Popen('echo "password"',stdout=subprocess.PIPE,shell=True).stdout


report=[]
networking_reports=[]
services_reports=[]
system_maintenence_reports=[]
access_controls_reports=[]
host_firewall_reports=[]

count={}

processed_selection=[]

Process_Hardening_data={
    'addr_space_layout_randomization.sh':'Ensure address space layout randomization is enabled ',
    'p_trace_scope_restricted.sh':'Ensure ptrace_scope is restricted',
    'core_dump_restricted.sh':'Ensure core_dumps are restricted ',
    'prelink.sh':'Ensure prelink is not installed ',
    'auto_error_report_not_enabled.sh':'Ensure Automatic Error Reporting is not enabled '
}

GDM = {
	'gdm.sh' : 'Ensure GDM is removed',
	'auto_mount_rmmedia_disabled.sh' : 'Ensure GDM automatic mounting of removable media is disabled',
	'auto_mount_rmmedia_disabled_cant_override.sh' : 'Ensure GDM disabling automatic mounting of removable media is not overridden',
	'autorun_never.sh' : 'Ensure GDM autorun-never is enabled',
	'autorun_never_cant_override.sh' : 'Ensure GDM autorun-never is not overridden',
	'disable_user_list_opt.sh' : 'Ensure GDM disable-user-list option is enabled',
	'scrnlock.sh' : 'Ensure GDM screen locks when the user is idle',
	'scrnlock_cant_override.sh' : 'Ensure GDM screen locks cannot be overridden',
	'xdcmp.sh' : 'Ensure XDCMP is not enabled',
	'gdm_login_banner.sh' : 'Ensure GDM login banner is configured'
}
PAM = {
	'PAM_Arguments' : "Invalid PAM arguments are ignored and logged if the module allows.",
	'pam_auth_update_profiles' : "Permits configuring the central authentication policy for the system using pre-defined profiles",
	'PAM_Software_packages' : "Updated versions of PAM includes additional functionality"
}
usr_acc_env = {
	'root_sys_acc_env':'Configure root and system accounts and environment',
	'shadow_password_suite':'Use change command to effect changes to individual user IDs',
	'user_def_env':'Configure user default environment'
}
sshserver = {
	'SSH_Server':'Configure SSH Server'
}
priv_esc = {
	'Privilege_escalation' : 'Configure privilege escalation'
}

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

nftables = {
	'nftables' : 'Configure nftables'}
iptables = {
	'iptables' :'Configure iptables'}
ufw = {
	'ufw' : 'Configure UncomplicatedFirewall'
}

@app.route('/', methods=['GET', 'POST'])
def upload():
	
	return render_template("index.html")

@app.route('/result', methods=['POST','GET'])
def result():
	global report,count,networking_reports,services_reports,system_maintenence_reports,access_controls_reports,host_firewall_reports,processed_selection
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
	temp1+=access_controls_reports
	temp1+=host_firewall_reports
	print(services_reports)
	print(count) 
	report=[]
	networking_reports=[]
	services_reports=[]
	system_maintenence_reports=[]
	access_controls_reports=[]
	host_firewall_reports=[]
	count={}
	processed_selection=[]
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

@app.route('/process', methods=['GET','POST'])
def process():
	global sudo_password_stream
	password_string,version=request.form.get('idk'),request.form.get('version')
	sudo_password_stream=subprocess.Popen(f'echo "{password_string}"',stdout=subprocess.PIPE,shell=True).stdout
	return "anythign u wanna return to js code"

@app.route('/selection_processing', methods=['GET','POST'])
def selection_processing():
	global processed_selection
	string=request.form.get('idk')

	lst=string.split('\n')
	for i in lst:
		processed_selection.append(i[:3])
	print(processed_selection)

	return "anythign u wanna return to js code"

@app.route("/selection", methods=['GET','POST'])
def selection():
	return render_template("selection.html")

@app.route("/unavailable", methods=['GET','POST'])
def unavailable():
	return render_template("unavailable.html")

@app.route("/scan_running", methods=['GET','POST'])
def scan_running():
	global report,count,networking_reports,services_reports,system_maintenence_reports,host_firewall_reports,processed_selection

	
	
	#kernal modules
	if "1.1" in processed_selection:
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
	if "1.3" in processed_selection:
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
	
	#process hardening checks
	if "1.5" in processed_selection:
		pass_count=0
		fail_count=0
		for i in os.listdir("Additional Process Hardening"):
			process=subprocess.Popen(f'bash {os.path.join("Additional Process Hardening",i)}',stdout=subprocess.PIPE,shell=True)
			output_dict={}
			stdout_data,_=process.communicate()
			output = stdout_data.decode('utf-8')
			if i == 'core_dump_restricted.sh' and ("PASS" in output) and ("* hard core 0" in output):
				output_dict["pof"]=["status passed",'1/1',"PASS"]
				pass_count+=1	
			#pass or fail
			elif ((i == 'prelink.sh') or (i == 'auto_error_report_not_enabled.sh')) and not output:
				
				output_dict["pof"]=["status passed",'1/1',"PASS"]
				pass_count+=1
			elif ("PASS" in output):
				output_dict["pof"]=["status passed",'1/1',"PASS"]
				pass_count+=1
			else:
				
				output_dict["pof"]=["status failed",'0/1',"FAIL"]
				fail_count+=1
			#adding description 
			output_dict["desc"]=Process_Hardening_data[i]
			output_dict["title"]="Configure Additional Process Hardening"
			report.append(output_dict)
		count["ph"]=[pass_count,0,fail_count]

	#GNOME Display Manager checks
	if '1.7' in processed_selection:
		pass_count=0
		fail_count=0

		for i in os.listdir("GDM"):
			process=subprocess.Popen(f'bash {os.path.join("GDM",i)}',stdout=subprocess.PIPE,shell=True)
			output_dict={}
			stdout_data,_=process.communicate()
			output = stdout_data.decode('utf-8')
			#pass or fail
			if i == "gdm.sh":
				if not output:
					output_dict["pof"]=["status passed",'1/1',"PASS"]
					pass_count+=1
				else:
					output_dict["pof"]=["status failed",'0/1',"FAIL"]
					fail_count+=1
			elif i == 'scrnlock.sh':
				if int(output.split("\n")[0][7]) <= 5: 
					output_dict["pof"]=["status passed",'1/1',"PASS"]
					pass_count+=1
				else:
					output_dict["pof"]=["status failed",'0/1',"FAIL"]
					fail_count+=1
			elif i == 'xdcmp.sh':
				if not output:
					output_dict["pof"]=["status passed",'1/1',"PASS"]
					pass_count+=1
				else:
					output_dict["pof"]=["status failed",'0/1',"FAIL"]
					fail_count+=1
			else:
				if "PASS" in output:
					output_dict["pof"]=["status passed",'1/1',"PASS"]
					pass_count+=1
				else:
					output_dict["pof"]=["status failed",'0/1',"FAIL"]
					fail_count+=1
			
			#adding description 
			output_dict["desc"]=GDM[i]
			output_dict["title"]="Configure GNOME display manager"
			report.append(output_dict)
		count["gdm"]=[pass_count,0,fail_count]

	#next 3 if cases is for Networking section
	if "3.3" in processed_selection:
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
	
	if "3.2" in processed_selection:
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
	
	if "3.1" in processed_selection:
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
	if "2.2" in processed_selection:
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
	
	if "2.1" in processed_selection:
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
	
	if "2.4" in processed_selection:
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
	
	if "2.3" in processed_selection:
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

	#next 4 sections for Access Control
	#PAM
	if "5.3" in processed_selection:
		for selected in PAM.keys():
			pass_count=0
			fail_count=0
			no_of_files=len(os.listdir(f"Access_Control/PAM/{selected}"))
			output_dict={}

			for i in os.listdir(f"Access_Control/PAM/{selected}"):
				process=subprocess.Popen(f'bash {os.path.join(f"Access_Control/PAM/{selected}",i)}',stdout=subprocess.PIPE,shell=True)
				stdout_data,_=process.communicate()
				output = stdout_data.decode('utf-8')
				#PAM ARGUMENTS SECTION
				if i=="pam_unix_no_inc_remember.sh":
					if ("pam_unix.so nullok" in output):
						fail_count+=1
					else:
						pass_count+=1
				elif 'unix' in i:
					if ('use_authtok' in output) or ('sha512' in output) or ('yescrypt' in output) or ('remember' not in output):
						pass_count += 1
					else:
						fail_count += 1

				if i == 'passwd_failed_attempts.sh':
					if 'deny' in output and int(output[7]) <= 5:
						pass_count += 1
					else:
						fail_count+= 1
				if i == 'passwd_failed_attempts_lockout.sh':
					if ('even_deny_root' in output or 'root_unlock_time' in output) :
						try:
							time = int(''.join([char for char in output if char.isdigit()]))
						except ValueError:
							time = 0
						if time >= 60:
							pass_count += 1
						else:
							fail_count+=1
					else:
						fail_count += 1
				if i == 'passwd_unlock_time.sh':
					try:
						time = int(''.join([char for char in output if char.isdigit()]))
					except ValueError:
						time = 1
					if time == 0 or time >= 900:
						pass_count += 1
					else:
						fail_count += 1	
				if 'hist' in i:
					try:
						time = int(''.join([char for char in output if char.isdigit()]))
					except ValueError:
						time = 0
					if i == 'passwd_history.sh' and 'remember' in output and time >= 24:
						pass_count += 1
					elif i == 'passwd_hist_root.sh' and 'enforce_for_root' in output:
						pass_count += 1
					elif i == 'pam_pwhistory_authtok.sh' and 'use_authtok' in output:
						pass_count += 1
					else:
						fail_count += 1
				try:
					ints = int(''.join([char for char in output if char.isdigit()]))
				except ValueError:
					ints = 0
				if i in ['passwd_min_len.sh', 
						'passwd_max_seq_chars.sh', 
						'passwd_min_len.sh', 
						'passwd_num_changed.sh', 
						'passwd_quality_check.sh', 
						'passwd_quality_check_root.sh', 
						'passwd_same_consec_chars.sh',
						'passwd_dict_check.sh'
						]:
					if i == 'passwd_num_changed.sh' and ints >= 502:
						pass_count += 1
					elif i == 'passwd_min_len.sh' and ints >= 5014:
						pass_count += 1
					elif ('consec' in i or 'seq' in i) and 500 < ints <= 503:
						pass_count +=1
					elif ints == 0 or 'enforce_for_root' in output:
						pass_count += 1
					else: 
						fail_count += 1
				#ARGUMENTS SECTION ENDS
				#AUTH UPDATE PROFILES 
				if i in ['pam_faillock.sh','pam_pwhistory.sh','pam_pwquality.sh','pam_unix.sh']:
					if 'pam_faillock' in output or 'pam_pwhistory' in output or 'pam_pwquality' in output or 'pam_unix' in output:
						pass_count += 1
					else:
						fail_count += 1
				#AUTH UPDATE PROFILES ENDS
				#PAM_Software_packages install ok installed

				if i in ['latest_pam.sh','libpam_installed.sh','libpam_pwquality.sh']:
					if 'install ok installed' in output:
						pass_count += 1
					else:
						fail_count += 1


			output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,selected)
			output_dict["desc"]=PAM[selected]
			output_dict["title"]="Pluggable Authentication Modules"
			access_controls_reports.append(output_dict)
	#User Accounts and Environment
	if "5.4" in processed_selection:
		for selected in usr_acc_env.keys():
			pass_count=0
			fail_count=0
			no_of_files=len(os.listdir(f"Access_Control/User_acc_env/{selected}"))

			#checking if partition is available
			output_dict={}
				
			for i in os.listdir(f"Access_Control/User_acc_env/{selected}"):
				process=subprocess.Popen(f'sudo -S bash {os.path.join(f"Access_Control/User_acc_env/{selected}",i)}',stdin = sudo_password_stream, stdout=subprocess.PIPE,shell=True)
				stdout_data,_=process.communicate()
				output = stdout_data.decode('utf-8')
				#user_def_env
				if i == 'nologin_not_listed.sh':
					if not output:
						pass_count += 1
					else:
						fail_count += 1
				elif i in ['def_usr_shell_timeout.sh','def_usr_umask.sh']:
					if 'def_usr_shell_timeout.sh':
						print("grep dir not found is normal")
					if "PASS" in output:
						pass_count += 1
					else:
						fail_count += 1
				#root_sys_acc_env
				if 'umask' in i or 'valid' in i:
					if not output:
						pass_count += 1
					else:
						fail_count += 1
				elif i == 'root_path_integrity.sh':
					if "PASS" in output:
						pass_count += 1
					else:
						fail_count += 1
				else:
					if output == 'root' or output == 'root:0'  or output == 'User: "root" Password is set':
						pass_count += 1
					else:
						fail_count += 1
				#shadow_password_suite
				if i == 'strong_passwd_hash.sh':
					if 'yescrypt' in output or 'sha512' in output:
						pass_count += 1
					else:
						fail_count += 1
				else:
					if not output:
						pass_count += 1
					else:
						fail_count += 1
				
			output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,selected)
			output_dict["desc"]=usr_acc_env[selected]
			output_dict["title"]="User Accounts and Environment"
				
			access_controls_reports.append(output_dict)
	#ssh server config
	if "5.1" in processed_selection:
		no_of_files,pass_count,fail_count=22,0,0
		output_dict={}
		for i in os.listdir("Access_Control/SSH_Server"):
			if 'perms' in i:
				pass_count,fail_count,_=pass_fail(path=os.path.join(f"Access_Control/SSH_Server",i),
						pass_count=pass_count,
						fail_count=fail_count)
			elif i == 'sshd_maxstartups.sh':
				pass_count,fail_count,_=nothing_should_be_returned(path=f"Access_Control/SSH_Server/{i}",
					pass_count=pass_count,
					fail_count=fail_count,sudo=True)
			else:
				process=subprocess.Popen(f'sudo -S bash {os.path.join(f"Access_Control/SSH_Server/",i)}',stdin=sudo_password_stream,stdout=subprocess.PIPE,shell=True)
				stdout_data,_=process.communicate()
				output = stdout_data.decode('utf-8')
				if i == 'sshd_access.sh' :
					if 'allowusers' in output or 'allowgroups' in output or 'denyusers' in output or 'denygroups' in output:
						pass_count += 1
					else:
						fail_count += 1
				if i == 'sshd_banner.sh':
					if 'banner /etc/issue.net' in output:
						pass_count += 1
					else:
						fail_count += 1
				if i == 'sshd_cipher.sh':
					if '3des-cbc' in output or 'aes128-cbc' in output or 'aes192-cbc' in output or 'aes256-cbc' in output:
						fail_count += 1
					else:
						pass_count += 1
				if i == 'sshd_clientaliveinterval_countmax.sh':
					output = output.split("\n")
					try:
						time0 = int(''.join([char for char in output[0] if char.isdigit()]))
						time1 = int(''.join([char for char in output[1] if char.isdigit()]))
					except ValueError:
						time0, time1 = -1, -1
					if time0 >= 0 and time1 >= 0:
						pass_count += 1
					else:
						fail_count += 1
				if i == 'sshd_disableforwarding.sh' or i == 'sshd_ignorerhosts.sh' or i == 'sshd_usepam.sh':
					if 'yes' in output:
						pass_count += 1
					else:
						fail_count += 1
				if i=='sshd_gssapi.sh' or i == 'sshd_hostbasedauth.sh' or i == 'sshd_permitemptypasswords.sh' or i == 'sshd_permitrootlogin.sh' or i == 'sshd_permituserenv.sh':
					if 'no' in output:
						pass_count += 1
					else:
						fail_count += 1
				if i == 'sshd_kexalgo.sh':
					if 'diffie-hellman-group1-sha1' in output or 'diffie-hellman-group14-sha1' in output or 'diffie-hellman-group-exchange-sha1' in output:
						fail_count += 1
					else:
						pass_count += 1
				if i == 'sshd_logingracetime.sh':
					try:
						time = int(''.join([char for char in output if char.isdigit()]))
					except ValueError:
						time = 0
					if 1 <= time <= 60:
						pass_count += 1
					else:
						fail_count += 1
				if i == 'sshd_loglevel.sh':
					if 'VERBOSE' in output or 'INFO' in output:
						pass_count += 1
					else:
						fail_count += 1
				if i == 'sshd_macs.sh':
					forbidden = ['hmac-md5',
								'hmac-md5-96',
								'hmac-ripemd160',
								'hmac-sha1-96',
								'umac-64@openssh.com',
								'hmac-md5-etm@openssh.com',
								'hmac-md5-96-etm@openssh.com',
								'hmac-ripemd160-etm@openssh.com',
								'hmac-sha1-96-etm@openssh.com',
								'umac-64-etm@openssh.com',
								'umac-128-etm@openssh.com'
					]
					for i in forbidden:
						if i in output:
							fail_count += 1
							break
					else:
						pass_count += 1
				if i == 'sshd_maxauthtries.sh':
					try:
						time = int(''.join([char for char in output if char.isdigit()]))
					except ValueError:
						time = 5
					if time <= 4:
						pass_count += 1
					else:
						fail_count += 1
				if i == 'sshd_maxsessions.sh':
					try:
						time = int(''.join([char for char in output if char.isdigit()]))
					except ValueError:
						time = 11
					if time <= 10:
						pass_count += 1
					else:
						fail_count += 1
		output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,"sshserver")
		output_dict["title"]='SSH Server'
		output_dict["desc"]=sshserver['SSH_Server']
		
		access_controls_reports.append(output_dict)
	#privilage escalation
	if "5.2" in processed_selection:
		no_of_files,pass_count,fail_count=7,0,0
		output_dict={}
		for i in os.listdir("Access_Control/Privilege_escalation"):
			if i == 'passwd_req_for_privilege_esc.sh':
				pass_count,fail_count,_=nothing_should_be_returned(path=f"Access_Control/Privilege_escalation/{i}",
					pass_count=pass_count,
					fail_count=fail_count,sudo=True)
			else:
				process=subprocess.Popen(f'sudo -S bash {os.path.join(f"Access_Control/Privilege_escalation/",i)}',stdin=sudo_password_stream,stdout=subprocess.PIPE,shell=True)
				stdout_data,_=process.communicate()
				output = stdout_data.decode('utf-8')
				if i == 'sudo_installed.sh':
					if 'sudo is installed' in output and 'sudo-ldap is installed' in output:
						pass_count += 1
					else:
						fail_count += 1
				if i == 'sudo_uses_pty.sh':
					if 'use_pty' in output:
						pass_count += 1
					else:
						fail_count += 1
				if i == 'reauth_privilege_esc.sh' :
					if '!authenticate' in output:
						fail_count += 1
					else:
						pass_count += 1
				if i == 'su_access_restricted.sh':
					if 'auth required pam_wheel.so use_uid group' in output:
						pass_count += 1
					else:
						fail_count += 1
				if i == 'sudo_auth_timeout.sh':
					process=subprocess.Popen('sudo grep -roP "timestamp_timeout=\K[0-9]*" /etc/sudoers*',stdin=sudo_password_stream,stdout=subprocess.PIPE,shell=True)
					stdout_data,_=process.communicate()
					output = stdout_data.decode('utf-8')
					if not output:
						process=subprocess.Popen('sudo sudo -V | grep "Authentication timestamp timeout:"',stdin=sudo_password_stream,stdout=subprocess.PIPE,shell=True)
						stdout_data,_=process.communicate()
						output = stdout_data.decode('utf-8')
						time = int(''.join([char for char in output if char.isdigit()]))
						if time == 150:
							pass_count += 1
						else:
							fail_count += 1
					else:
						time = int(''.join([char for char in output if char.isdigit()]))
						if time <= 150:
							pass_count += 1
						else:
							fail_count += 1
				if i == 'sudo_log_exists.sh':
					if 'Defaults logfile="/var/log/sudo.log"' in output:
						pass_count += 1
					else:
						fail_count += 1
		output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,"priv_esc")
		output_dict["title"]='Privilege escalation'
		output_dict["desc"]=priv_esc['Privilege_escalation']
		
		access_controls_reports.append(output_dict)

	#System maintainance starts from here
	if "7.1" in processed_selection:
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
	if "7.2" in processed_selection:
		no_of_files,pass_count,fail_count=10,0,0
		output_dict={}
		for i in os.listdir("System_Maintenence/Local_UserGroupSetting"):
			process=subprocess.Popen(f'bash {os.path.join("System_Maintenence/Local_UserGroupSetting",i)}',stdout=subprocess.PIPE,shell=True)
			stdout_data,_=process.communicate()
			output = stdout_data.decode('utf-8')

			if i in ["7.2.10.sh","7.2.9.sh"]: # pass or fail
				pass_count,fail_count,_=pass_fail(path=os.path.join(f"System_Maintenence/Local_UserGroupSetting",i),
													pass_count=pass_count,
													fail_count=fail_count,sudo=True)
			else:#has errors
				pass_count,fail_count,_=nothing_should_be_returned(path=os.path.join(f"System_Maintenence/Local_UserGroupSetting",i),
																pass_count=pass_count,
																fail_count=fail_count,sudo=True)

		output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,"local_usr_grp")
		output_dict["title"]="Local User and Group Settings"
		output_dict["desc"]=parent_dict_system_maintenence["Local_UserGroupSetting"]

		system_maintenence_reports.append(output_dict)
	
	#Host Firewall starts from here
	if "4.2" in processed_selection:
		pass_count=0
		fail_count=0
		no_of_files=len(os.listdir(f"HostFirewall/nftables"))
		output_dict={}

		for i in os.listdir(f"HostFirewall/nftables"):
			process=subprocess.Popen(f'sudo -S bash {os.path.join(f"HostFirewall/nftables",i)}',stdin = sudo_password_stream,stdout=subprocess.PIPE,shell=True)
			stdout_data,_=process.communicate()
			output = stdout_data.decode('utf-8')
			if i == 'nftables.sh':
				if 'installed' in output:
					pass_count += 1
				else:
					fail_count += 1
			if i == 'ufwdisabled.sh':
				pass_count,fail_count,_=nothing_should_be_returned(path=f"HostFirewall/nftables/{i}",
					pass_count=pass_count,
					fail_count=fail_count)
			if i == 'nptablesexists.sh':
				if not output:
					fail_count += 1
				elif output[:5] == 'table':
					pass_count += 1
			if i == 'basechains.sh':
				if 'type filter hook input priority' in output and 'type filter hook forward priority' in output and 'type filter hook output priority' in output:
					pass_count += 1
				else:
					fail_count += 1
			if i  == 'lookbacktraffic.sh':
				if 'iif "lo" accept' in output and 'ip saddr' in output and 'ip6 saddr' in output and 'counter packets' in output:
					pass_count += 1
				else:
					fail_count += 1
			if i == 'denyfirewallpolicy.sh':
				for i in output.split("\n"):
					if output.count('drop') != 1:
						fail_count += 1
						break
				else:
					pass_count += 1
			if i == 'nftablesservices.sh':
				if 'enabled' in output:
					pass_count += 1
				else:
					fail_count += 1
			if i == 'rules.sh':
				ops = ['type filter hook input priority 0; policy drop',
						'ip protocol tcp ct state established accept',
						'ip protocol udp ct state established accept',
						'ip protocol icmp ct state established accept',
						'tcp dport ssh accept',
						'ip protocol tcp ct state established,related,new accept',
						'ip protocol tcp ct state established,related,new accept',
						'ip protocol udp ct state established,related,new accept',
						'ip protocol icmp ct state established,related,new accept',
						'type filter hook forward priority 0; policy drop;'
				]
				for i in ops:
					if i not in output:
						fail_count += 1
						break
				else:
					pass_count += 1
	
		output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,"nftables")
		output_dict["title"]='Host Firewall'
		output_dict["desc"]=nftables['nftables']
		
		host_firewall_reports.append(output_dict)

	if "4.3" in processed_selection:
		pass_count=0
		fail_count=0
		no_of_files=len(os.listdir(f"HostFirewall/iptables"))
		output_dict={}

		for i in os.listdir(f"HostFirewall/iptables"):
			process=subprocess.Popen(f'sudo -S bash {os.path.join(f"HostFirewall/iptables",i)}',stdin = sudo_password_stream,stdout=subprocess.PIPE,shell=True)
			stdout_data,_=process.communicate()
			output = stdout_data.decode('utf-8')
			if i == 'packages.sh':
				if 'installed' in output:
					pass_count += 1
				else:
					fail_count += 1
			if i == 'nftables.sh' or i == 'ufw.sh':
				pass_count,fail_count,_=nothing_should_be_returned(path=f"HostFirewall/iptables/{i}",
					pass_count=pass_count,
					fail_count=fail_count)
			if i == 'firewallpolicy.sh' or i == 'ip6tabledenyfirewall.sh':
				if 'Chain INPUT (policy DROP)' in output and 'Chain FORWARD (policy DROP)' in output and 'Chain OUTPUT (policy DROP)' in output:
					pass_count += 1
				else:
					fail_count += 1
			if i == 'lookbacktraffic.sh' or i == 'ip6lookbacktraffic.sh':
				output1 = output.split('\n')
				if len(output1) >= 6 and ('Chain INPUT (policy ACCEPT' in output1[0] or 'OUTPUT ' in output):
					pass_count += 1
				else:
					fail_count += 1
			if i  == 'firewallrules.sh' or i == 'ip6firewallpolicy.sh':
				output1 = output.split('\n')
				#'Netid  State   Recv-Q  Send-Q   Local Address:Port    Peer Address:Port Process'
				if len(output1) >= 4  and output1[0] == 'Netid  State   Recv-Q  Send-Q   Local Address:Port    Peer Address:Port Process' and 'Chain INPUT (policy ACCEPT' in output:
					pass_count += 1
				else:
					fail_count += 1
			
	
		output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,"iptables")
		output_dict["title"]='Host Firewall'
		output_dict["desc"]=iptables['iptables']
		
		host_firewall_reports.append(output_dict)
	if "4.1" in processed_selection:
		pass_count=0
		fail_count=0
		no_of_files=len(os.listdir(f"HostFirewall/UncomplicatedFirewall"))
		output_dict={}

		for i in os.listdir(f"HostFirewall/UncomplicatedFirewall"):
			process=subprocess.Popen(f'sudo -S bash {os.path.join(f"HostFirewall/UncomplicatedFirewall",i)}',stdin = sudo_password_stream,stdout=subprocess.PIPE,shell=True)
			stdout_data,_=process.communicate()
			output = stdout_data.decode('utf-8')
			if i == 'ufw.sh':
				if 'installed' in output:
					pass_count += 1
				else:
					fail_count += 1
			if i == 'iptables.sh':
				pass_count,fail_count,_=nothing_should_be_returned(path=f"HostFirewall/UncomplicatedFirewall/{i}",
					pass_count=pass_count,
					fail_count=fail_count)
			if i == 'ufw_service.sh':
				output = output.split('\n')
				ops = ['enabled', 'active', 'Status: active']
				if output == ops:
					pass_count += 1
				else:
					fail_count += 1
			if i == 'loopback.sh':
				ops = ['To                         Action      From', '--                         ------      ----', 'Anywhere on lo             ALLOW IN    Anywhere                  ', 'Anywhere                   DENY IN     127.0.0.0/8               ', 'Anywhere (v6) on lo        ALLOW IN    Anywhere (v6)             ', 'Anywhere (v6)              DENY IN     ::1                       ', '', 'Anywhere                   ALLOW OUT   Anywhere on lo            ', 'Anywhere (v6)              ALLOW OUT   Anywhere (v6) on lo ']
				for i in ops:
					if i not in output.split('\n'):
						fail_count += 1
						break
				else:
					pass_count += 1
			if i == 'openports.sh':
				if "FAIL" in output:
					fail_count += 1
				elif "Passed" in output:
					pass_count += 1
				else:
					fail_count += 1
			if i == 'firewallpolicy.sh':
				if 'allow' in output:
					fail_count += 1
				else:
					pass_count += 1
		output_dict["pof"]=report_dict_helper(pass_count,fail_count,no_of_files,"ufw")
		output_dict["title"]='Host Firewall'
		output_dict["desc"]=ufw['ufw']
		
		host_firewall_reports.append(output_dict)
	return redirect('/result')




