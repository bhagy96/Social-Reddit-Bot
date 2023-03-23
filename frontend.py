import redditbot
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/result',methods=['POST', 'GET'])


def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]
    action_lst = request.form.getlist('option')
    print(name)
    action_completed, pcomment = redditbot.generate_response(output["bot"], name, output["keyw"],
                                                    action_lst, output["prompt"], int(output["lookno"]))
    return render_template('index.html', name = name, pcomment=pcomment, action_completed= action_completed)
if __name__ == "__main__":
    app.run(debug=True, port=5001)

