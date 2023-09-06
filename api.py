#flask API, Swagger UI

import pandas as pd
import re
from flask import request, Flask, jsonify

from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from


app = Flask(__name__)
#########################################################################################
app.json_encoder = LazyJSONEncoder

swagger_template = {
	"swagger":"2.0",
	"info":{
		"title": "API Documentation for Data Processing and Modelling",
		"description": "Dokumentasi API untuk Data Processing dan Modelling",
		"version": "1.0.0"
	}
}

swagger_config = {
	"headers" : [],
	"specs" : [
		{
			"endpoint" : 'docs',
			"route" : '/docs.json'
            "rule_filter" : lambda rule: True,
		}
	],
	"static_url_path" : '/flasgger_statis',
	"swagger_ui" : True,
	"specs_route" : "/docs/"
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)

#########################################################################################################

POST INPUT USER
@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text_processing', methods=['POST'])
def text_processing():
    text = request.form.get('text')
    print(text)
    json_response = { 
        'status_code':200, 
        'description':'teks yang sudah diproses', 
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', text)
        }

    response_data = jsonify(json_response)
    return response_data

#POST INPUT FILE
@swag_from("docs/post_upload.yml",methods=['POST'])
@app.route('/upload', methods=['POST'])
def uploadFile():
    final=[]
    file = request.files['file']
    try:
        data = pd.read_csv(file, encoding='iso-8859-1',on_bad_lines='skip')
    except: 
        data = pd.read_csv(file, encoding='iso-8859-1',on_bad_lines='skip')

    response_data = jsonify({"message": "File uploaded successfully"})
    return response_data, 200

# @swag_from("docs/post_upload.yml", methods=['POST'])
# @app.route('/upload', methods=['POST'])
# def uploadFile():
#     final = []
#     file = request.files['file']
#     try:
#         data = pd.read_csv(file, encoding='iso-8859-1', on_bad_lines='skip')
#         # Lakukan operasi lain dengan data CSV di sini
#         return 'Upload berhasil', 200
#     except Exception as e:
#         return 'Terjadi kesalahan: ' + str(e), 500


if __name__ == '__main__':
    app.run(debug=True)
