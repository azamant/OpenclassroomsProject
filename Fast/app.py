from flask import Flask, render_template, jsonify, request
import json
import requests

app = Flask(__name__)

AZURE_API_URL = "https://projet9armandzamant.azurewebsites.net/api/HttpExample?name="

@app.route('/', methods=['GET'])
def Liste():
    return render_template("recomm.html")

@app.route('/', methods =['POST'])
def predictAPI():
    numero = request.form['Client_id']
    response = requests.get(AZURE_API_URL + numero)
    content = json.loads(response.content.decode('utf-8'))
    
    if response.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'La requête à l\'API météo n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(content['message'])
        }), 500
    print(type(content))
    print(content['data'])
    ToReturn = []
    for ligne in content['data']:
        ToReturn.append(ligne['article_id'])
    return render_template("recomm.html", prediction=ToReturn)

if __name__ == "__main__":
    app.run(debug=True)