from __future__ import unicode_literals
import datetime as dt
import json
import requests
import slackbot
'''
user can set alerts in command line as follows:

threshold: pageviews in last 5 minutes

channel: webhook

if pageview threshold goes above set threshold, notify channel.

'''

class SlackAlert(object):

    def __init__(self, slackbot):
        self.slackbot = slackbot
        # {url: timestamp} dict
        self.sent_notifications = {}

    def send_alert(self, attachments, channel):
        ''' send list of attachments to Slack as an alert '''

        payload = {
            'channel': channel,
            'username': 'Parselybot',
            'text': 'The following posts have broken the pageview threshold',
            'attachments': attachments}

        headers={'Content-type': 'application/json'}

        try:
            webhook_url = self.slackbot.config['webhook_url']
            print requests.post(webhook_url, headers=headers, json=payload).content
        except (requests.exceptions.MissingSchema, AttributeError):
            print(
                'The webhook URL appears to be invalid. '
                'Are you sure you have the right webhook URL?')

    def find_breaking_posts(self):
        ''' check if any URLs have exceeded pageview threshold, if so return breaking posts
        and header text'''
        time_period = slackbot.TimePeriod()
        time_period.minutes = 5
        top_posts = self.slackbot._client.realtime(aspect="posts", per=time_period, limit=100)
        # unlike custom commands, webhook has text param so header_text should be blank here
        header_text = ""
        # find breaking posts we haven't notified about
        breaking_posts = []
        now = dt.datetime.now()
        for post in top_posts:
            if post.hits >= self.slackbot.config['threshold']:
               last_notified = self.sent_notifications.get(post.url)
               if not last_notified or last_notified < now - dt.timedelta(hours=1):
                    self.sent_notifications[post.url] = now
                    breaking_posts.append(post)
        return breaking_posts, header_text

    def run(self):
        last_check = None
        while True:
            if self.slackbot.config.get('threshold') > 0 and self.slackbot.config.get('channels'):
                now = dt.datetime.now()
                if not last_check or last_check < now - dt.timedelta(seconds=30):
                    last_check = now
                    breaking_posts, header_text = self.find_breaking_posts()
                    if breaking_posts:
                        attachments = self.slackbot.build_meta_attachments(breaking_posts, header_text)
                        for channel in self.slackbot.config['channels']:
                            self.send_alert(attachments, channel)




