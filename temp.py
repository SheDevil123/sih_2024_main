from flask import Flask, request, redirect,url_for,render_template
import subprocess 

app=Flask(__name__)

report=""

@app.route('/', methods=['GET', 'POST'])
def upload():
	global sheet_path, form_data
	if request.method == 'POST':
		kernal_modules=request.form.get("kernal_modules")
		if kernal_modules:
			process=subprocess.Popen('echo "hello"',shell=True)
			stdout_data,_=process.communicate()
			output = stdout_data.decode('utf-8')
			report= report + "\n" +output
		return redirect('/result')
		
	return render_template("index.html")

@app.route('/result', methods=['POST','GET'])
def result():
    return render_template('result_page.html')
			