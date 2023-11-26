Building a Serverless Weather API with AWS SAM CLI and Lambda in Python
Welcome to this step-by-step guide on creating a serverless API using AWS SAM CLI and Lambda, designed for beginners. Our goal is to build an API that determines whether an umbrella is needed based on the zip code, using Python.
Prerequisites
Before diving in, ensure you have the following installed:
AWS CLI
AWS SAM CLI
A preferred code editor (like VSCode)
Installing AWS SAM CLI
For MacOS/Linux: Run the following in your terminal:
bash
Copy code
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/aws/aws-sam-cli/master/installer/pyinstaller/install.sh)"


For Windows: Download and run the installer.
Step 1: Initialize Your SAM Application
Create a new SAM application:
bash
Copy code
sam init

Select "AWS Quick Start Templates", choose Python as the runtime, and select the "Hello World Example".
Step 2: Setup the APIs
For this example we will use Accuweather APIs. Signup for a free account and get your API key here. We will use 2 APIs
Get the location id - AccuWeather APIs | Postal Code Search
Use the location id to get the forecast - AccuWeather APIs | 1 Day of Daily Forecasts

Once you register, create a new app and get your api key.



Step 3: Implementing the Lambda Function
I use VSCode for development.  Fire up a terminal window and get started with creating a virtual environment and activate it.

python3 -m venv venv  
venv\Scripts\activate

Next we install the dependencies. In the helloworld folder you will find the requirements.txt


pip install -r <path to the requirements.txt>



In app.py, write the logic for your Lambda function:

import json
import requests




def lambda_handler(event, context):
    try:
        #get zip code from the request
        zipcode = event["zipcode"]
        #get the location key from the api
        locationapi_url = "http://dataservice.accuweather.com/locations/v1/postalcodes/search?details=true&apikey=TGjfbl4wl1GLIEeID2GeTHfE2P0hKnnj&q={}".format(zipcode)
        response = requests.request("GET", locationapi_url)


        location_response = json.loads(response.text)
        locationkey = location_response[0]['Details']['Key']


        #get the forecast for the location key
        forecastapi_url = "http://dataservice.accuweather.com/forecasts/v1/daily/1day/{}?apikey=TGjfbl4wl1GLIEeID2GeTHfE2P0hKnnj&details=true".format(locationkey)


        response = requests.request("GET", forecastapi_url)
        forecast_response = json.loads(response.text)
       
        rainprobablity = forecast_response['DailyForecasts'][0]['Day']['RainProbability']


        #return the response if the probability is more than 5
        if rainprobablity > 5:
            umbrella_checker_response = "You will need an umbrella tomorrow"
        else:
            umbrella_checker_response = "You dont need an umbrella tomorrow"
    except requests.RequestException as e:
         # Send some context about this error to Lambda Logs
         print(e)


         raise e


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": umbrella_checker_response
        }),
    }



Step 4: Change the timeout
Lambda has a default timeout of 3 seconds. Since we are calling 2 external APIs we need to increase this to 10 seconds

Step 5: Deploying Your API
Deploy your application:
sam deploy --guided

Follow the instructions to complete the deployment. Make sure you allow sam cli to create roles
Allow SAM CLI IAM role creation [Y/n]: y

Step 6: Testing the lambda
Log into the AWS console and navigate to the lambda. Click on the umbrellachecker lambda that was just created. Click on “Test”. Paste the following json in the Event JSON window.

{
  "zipcode": "23233"
}

Click on the  button. If everything is well. You should see the following window on the top


Conclusion
You've successfully created a serverless API using AWS Lambda and API Gateway in Python. This API checks the weather for a given zip code and advises on whether an umbrella is needed. As you get more comfortable, you can expand this project by integrating more features or APIs. 
Happy coding in the world of serverless applications!
(Note: This blog is for educational purposes, and the instructions should be adapted for your specific project needs.)

Reference : 
