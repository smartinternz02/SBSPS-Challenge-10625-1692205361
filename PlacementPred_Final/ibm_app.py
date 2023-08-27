from flask import Flask, render_template, request
app=Flask(__name__)

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "T03d-j6LiE8YAeb6OweyWL2tIWh_3-8ca4HZfOd7eArr"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

API_KEY = "e35yQsgw11RBVLMxMePewQUhLQxBMa3Pl_0L4u5x7h-9"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


@app.route('/')
def render_index():
    return render_template('index.html')


@app.route('/cluster')
def render_cluster():
    return render_template('cluster.html')

    

@app.route('/display',methods=['GET','POST'])
def display():
    p=request.form['id']
    CGPA=request.form['cgpa']
    avg_tech=request.form['tas']
    domain_interest=request.form['di']
    if (domain_interest=='Networking'):
        domain_interest=0
    elif(domain_interest=='CloudComp'):
        domain_interest=1
    elif(domain_interest=='WebServices'):
        domain_interest=2
    elif(domain_interest=='DataAnalytics'):
        domain_interest=3
    elif(domain_interest=='QualityAssurance'):
        domain_interest=4
    else:
        domain_interest=5
    features1=[[float(CGPA),float(avg_tech),int(domain_interest)]]
    
    payload_scoring = {"input_data": [{"field": [[float(CGPA),float(avg_tech),int(domain_interest)]], "values": features1}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/8d7981c8-8ffb-42e1-a150-069bd46921ac/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print(response_scoring)
    predictions=response_scoring.json()
    output = predictions['predictions'][0]['values'][0][0]

    print(output)

    if (output==0):
        return render_template('index.html',y='The Student has lower chances of getting placed- Prediction : '+(str(output[0]))) 
    else:
        return render_template('index.html',y='Woah! The Student has higher chances of getting placed- Prediction : '+(str(output)))
    
   
@app.route('/cluster', methods=['GET', 'POST'])
def display_cluster():
    if request.method == 'POST':
        CGPA = request.form['cl_cgpa']
        avg_tech = request.form['cl_tas']
        domain_interest = request.form['cl_di']
        if domain_interest == 'Networking':
            domain_interest = 0
        elif domain_interest == 'CloudComp':
            domain_interest = 1
        elif domain_interest == 'WebServices':
            domain_interest = 2
        elif domain_interest == 'DataAnalytics':
            domain_interest = 3
        elif domain_interest == 'QualityAssurance':
            domain_interest = 4
        else:
            domain_interest = 5
        
        features2 = [[float(CGPA), float(avg_tech)]]
        
        payload_scoring = {"input_data": [{"field": [[float(CGPA), float(avg_tech)]], "values": features2}]}
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7d7e46d9-20c0-464e-952b-21fb5d3ace6c/predictions?version=2021-05-01', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print(response_scoring)
        predictions=response_scoring.json()
        result = predictions['predictions'][0]['values'][0][0]

        print(result)  
    
        return render_template('cluster.html', y=f'Student belongs to Cluster: {str(result)}\nScroll down below, to know more...')
           


if __name__ == '__main__':
    app.run(debug=True) 