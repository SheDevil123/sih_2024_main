from flask import Flask,render_template

app=Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload():
    return render_template('report.html', report="hello world")


if __name__ == '_main_':
	app.run(debug=True)
