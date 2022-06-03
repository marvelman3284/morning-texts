import yaml
import gcal
import weather
import requests


def text() -> None:
    '''Get the needed information and send a text message'''

    # Read and load the config file
    with open('config.yml', 'r') as f:
        conf = yaml.safe_load(f)

    # Get the calender events for today and the next day
    events = gcal.filter(gcal.get_events())
    events = "\n".join(events)

    # Get todays weather
    week_weather = weather.get_weather(conf['API']['key'], conf['API']['lat'], conf['API']['lon'])
    week_weather = week_weather[0]

    # Combine all the information into one string
    message = f"Upcoming you have:\n{events}.\nToday's weather is: \n{week_weather}"

    # Send the text message using textbelt    
    resp = requests.post('https://textbelt.com/text', {
        'phone': conf['Message']['number'],
        'message': message,
        'key': 'textbelt',
    })
    print(resp.json())

text()
