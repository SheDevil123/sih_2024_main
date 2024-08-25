from flask import Flask, request, redirect,url_for,render_template, send_from_directory, send_file
import subprocess 
import os 
import report_generator


app=Flask(__name__)


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
# partition_check_data={
# 	"tmp":"Configure",
# 	"devshm":"devshm desc",
# 	"home":"home desc",
# 	"var":"var desc",
# 	"vartmp":"vartmp desc",
# 	"varlog":"varlog desc",
# 	"varlogaudit":"varlogaudit desc",
# }

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
				no_of_files=1

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
							no_of_files+=1
						else:
							continue
						
						#pass or fail
						if output:
							fail_count+=1
						else:
							pass_count+=1
						
					if pass_count==no_of_files:
						output_dict["pof"]=["status passed",f'{no_of_files}/{no_of_files}',"PASS"]
					else:
						output_dict["pof"]=["status partially-passed",f'{pass_count}/{no_of_files}',"PARTIAL PASS"]
				else:
					output_dict["pof"]=["status failed",f'0/{no_of_files}',"FAIL"]
					fail_count+=no_of_files
					
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