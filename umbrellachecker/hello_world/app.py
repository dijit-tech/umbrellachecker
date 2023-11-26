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
