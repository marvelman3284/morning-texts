# TODO: need to read gcal api and send message is bday is < 1 week away
# TODO: add bdays in gcal
# DONE: also need to use gcal api to tell todays events
# DONE: open weather api for weather
# TODO: add gym sched into gcal and read from it w api
# TODO: swap out (g)mail -> sms for textbelt free api
# NOTE: maybe switch to yahoo if textbelt is too slow

import yaml
import gcal
import weather
import requests

with open('config.yml', 'r') as f:
    conf = yaml.safe_load(f)


def text() -> None:
    # DONE: filter events based on dates less than 1 week away
    events = gcal.filter(gcal.get_events())
    events = "\n".join(events)
    week_weather = weather.get_weather(conf['API']['key'], conf['API']['lat'], conf['API']['lon'])

    week_weather = "\n".join(week_weather)

    message = f"This week you have:\n{events}. \n{week_weather}"

    print(message)

    # resp = requests.post('https://textbelt.com/text', {
    #   'phone': conf['Message']['number'],
    #   'message': message,
    #   'key': 'textbelt',
    # })
    # print(resp.json())

text()
