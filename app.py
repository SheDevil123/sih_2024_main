from flask import Flask, request, redirect,url_for,render_template
import subprocess 
import os 


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
	"tmp":"Configure"
}

@app.route('/', methods=['GET', 'POST'])
def upload():
	global report,count
	if request.method == 'POST':
		kernal_modules=request.form.get("cramfs")
		partition_tmp=request.form.get("tmp")

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
				
				#adding discription 
				output_dict["disc"]=filesystem_check_data[i]
				output_dict["title"]="Configure Filesystem Kernel Modules"

				report.append(output_dict)

			count["km"]=[pass_count,0,fail_count]
	
		if partition_tmp:
			print("fml")
			pass_count=0
			fail_count=0

			#checking if partition is available
			process=subprocess.Popen(f'bash {os.path.join("partition_checks/tmp","tmp.sh")}',stdout=subprocess.PIPE,shell=True)
			output_dict={}
			stdout_data,_=process.communicate()
			output = stdout_data.decode('utf-8')

			#adding discription 
			output_dict["disc"]=partition_check_data["tmp"]
			output_dict["title"]="Configure Filesystem Partitions"
			if output:
				pass_count+=1
				for i in os.listdir("partition_checks/tmp"):
					if i!="tmp.sh":
						process=subprocess.Popen(f'bash {os.path.join("partition_checks/tmp",i)}',stdout=subprocess.PIPE,shell=True)
						stdout_data,_=process.communicate()
						output = stdout_data.decode('utf-8')
					else:
						continue
					
					#pass or fail
					if output:
						fail_count+=1
					else:
						pass_count+=1
					
					if pass_count==4:
						output_dict["pof"]=["status passed",'4/4',"PASS"]
					else:
						output_dict["pof"]=["status partially-passed",f'{pass_count}/4',"PARTIAL PASS"]
			else:
				output_dict["pof"]=["status failed",'0/4',"FAIL"]
				fail_count+=4
				
			report.append(output_dict)
			if pass_count==4:
				count["tmp"]=[pass_count,0,fail_count]
			else:
				count["tmp"]=[0,pass_count,fail_count]

		return redirect('/result')
	return render_template("index.html")

@app.route('/result', methods=['POST','GET'])
def result():
	global report,count,count
	no_of_pass=0
	no_of_fail=0
	no_of_partial=0

	print(count)
	for i in count.keys():
		no_of_pass+=count[i][0]
		no_of_fail+=count[i][2]
		no_of_partial+=count[i][1]
	print(report)
	total=no_of_fail+no_of_pass+no_of_partial
	temp1=list(report)
	report=[]
	count={}

	return render_template('p1.html',report=temp1,
						total=total,no_of_partial=no_of_partial,
						no_of_pass=no_of_pass,no_of_fail=no_of_fail)