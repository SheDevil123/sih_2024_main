from flask import Flask,render_template, request,redirect

app = Flask(__name__,template_folder="templates")

@app.route("/")
def hello():
    return render_template('temp.html')

@app.route('/process', methods=['POST','GET'])
def process():
    data = request.form.get('idk')
    print(data)
    # process the data using Python code
    result = data.upper()
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)