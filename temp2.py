from flask import Flask,render_template, request,redirect

app = Flask(__name__,template_folder="templates")

@app.route("/", methods=["POST","GET"])
def hello():
    if request.method=="POST":
        return redirect("/process")
    return render_template('temp.html')

@app.route('/process', methods=['POST','GET'])
def process():
    print(request.form.get('idk'))
    return "idk"

@app.route('/idk', methods=['POST','GET'])
def idk():
    return "the page after gettign daata"


if __name__ == '__main__':
    app.run(debug=True)