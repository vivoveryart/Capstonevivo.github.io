from flask import Flask, request, render_template
import requests
from requests.structures import CaseInsensitiveDict
from flask import json
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_data = False

    #mengambil Data dari HTML
    if request.method == 'POST':
        print(request.form['nama_sekolah'])
        print(request.form['npsn'])
        print(request.form['jenjang'])
        print(request.form['status'])
        print(request.form['guru'])
        print(request.form['pegawai'])
        print(request.form['r_kelas'])
        print(request.form['r_lab'])
        print(request.form['r_perpus'])
        nama_sekolah_value = request.form['nama_sekolah']
        npsn_value = request.form['npsn']
        jenjang_value = request.form['jenjang']
        status_value = request.form['status']
        guru_value = request.form['guru']
        pegawai_value = request.form['pegawai']
        r_kelas_value = request.form['r_kelas']
        r_lab_value = request.form['r_lab']
        r_perpus_value = request.form['r_perpus']

        access_token = get_access_token()

        prediction_value = get_prediction(
            access_token,
            nama_sekolah_value, npsn_value, jenjang_value, 
            status_value, guru_value, pegawai_value, r_kelas_value, 
            r_lab_value, r_perpus_value
        )

        prediction_data = prediction_value
    return render_template('index.html', prediction = prediction_data)

# Untuk mendapatkan token dari IBM Cloud
def get_access_token():
    url = "https://iam.cloud.ibm.com/oidc/token"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    data = "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=iuAuOectxTy7VvY0YIjQkzLvD85MoSYtshNkmc6Llrf1"
    resp = requests.post(url, headers=headers, data=data)
    if resp.status_code == 200:
        json_resp = resp.json()
        return json_resp.get('access_token')
    else:
        return None

#Mengirim data dari HTML ke Model Machine Learning
def get_prediction(access_token, *input_values):
    url = "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/b7a555e4-ff84-4092-8131-88fc7e037463/predictions?version=2021-05-01"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + access_token

    data = {
        "input_data": [
            {
                "fields": [
                    "Nama Sekolah", "NPSN", "Jenjang", "Status", "Guru", "Pegawai",
                    "R. Kelas", "R. Lab", "R. Perpus"
                ],
                "values": [list(input_values)]
            }
        ]
    }

    resp = requests.post(url, headers=headers, json=data)

    if resp.status_code == 200:
        predictions = resp.json()
        prediction_value = predictions['predictions'][0]['values'][0][0]
        output = json.loads(resp.text)
        print("output >>", output)
        return prediction_value
    else:
        return None