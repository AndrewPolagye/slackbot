from flask import Flask
from flask_slack import Slack
from config import *
import parsely_slack
app = Flask(__name__)

slack = Slack(app)
apikey = ""
secret = ""
slackbot = parsely_slack.ParselySlack(apikey, secret)
@slack.command('parsely', 'DcJRP8Lr9NRcjrQqAFoNQm2K', 'T090APE76',
                ['POST']) 
def parsely(**kwargs):
    text = kwargs.get('text')
    commands = [word.strip() for word in text.strip().split(',')]
    if 'author' or 'post' or 'section' or 'tag' in commands[0]:
        slackbot.analytics(commands)
    elif shares:
        slackbot.shares(commands)
    elif referrers:
        slackbot.referrers(commands)
    elif realtime(commands):
        slackbot.realtime(commands)
    return slack.response("Sorry, didn't recognize the command!")

def analytics(command_list):
    slackbot.
    pass

def shares(command_list):
    # TODO
    pass

def referrers(command_list):
    # TODO
    pass

def realtime(command_list):
    # TODO
    pass

app.add_url_rule('/', view_func=slack.dispatch)


if __name__ == '__main__':
        app.run('0.0.0.0', 6000, debug=True)
