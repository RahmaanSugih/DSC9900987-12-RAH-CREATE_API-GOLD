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

#POST INPUT USER
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
# Baca data frame dari file CSV
abusive_df = pd.read_csv("abusive.csv")

# Ambil daftar kata-kata abusive dari kolom 'ABUSIVE'
abusive_words = set(abusive_df['ABUSIVE'].str.lower())  # Konversi ke huruf kecil

# Fungsi untuk mengganti karakter dengan tanda "*"
def mask_text(match):
    return '*' * len(match.group())

# Fungsi untuk mengganti kata-kata abusive dalam teks dengan tanda "*"
def mask_abusive_text(text):
    text = text.lower()  # Konversi teks ke huruf kecil
    for word in abusive_words:
        text = re.sub(r'\b' + re.escape(word) + r'\b', mask_text, text)
    return text

class UploadFile(Resource):
    def post(self):
        try:
            file = request.files['file']

            if file:
                # Simpan file yang diunggah dengan nama yang aman
                filename = secure_filename(file.filename)
                file.save(filename)

                # Baca isi file teks
                with open(filename, 'r') as text_file:
                    text = text_file.read()

                # Filter teks dengan mengganti kata-kata abusive
                masked_text = mask_abusive_text(text)

                # Simpan hasil ke file
                with open("masked_text.txt", "w") as output_file:
                    output_file.write(masked_text)

                return {"message": "File uploaded successfully and abusive words masked."}, 200
            else:
                return {"message": "No file provided in the request."}, 400
        except Exception as e:
            return {"message": str(e)}, 500

api.add_resource(UploadFile, '/upload')


if __name__ == '__main__':
    app.run(debug=True)
