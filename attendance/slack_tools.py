import configparser
from datetime import date, timedelta, datetime
import slack
import os
import re

class SlackTools:
    def __init__(self):
        config = configparser.ConfigParser()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(BASE_DIR, 'config.ini')
        config.read(path)

        slack_api_token = config['DEFAULT']['SLACK_API_TOKEN']

        self.slack_client = slack.WebClient(token=slack_api_token)
        self.channel_id = config['DEFAULT']['CHANNEL_ID']

    def get_slack_client(self):
        return self.slack_client

    def get_channel_id(self):
        return self.channel_id

    def send_no_show_message(self, members):
        message = "[미출석자 알림]\n"
        for member in members:
            message += "@%s " % member

        self.slack_client.chat_postMessage(
            channel='#gardening-for-100days',
            text=message,
            link_names=1
        )

    def get_users(self):
        return self.slack_client.users_list()

    def get_user_names(self):
        return [user["name"] for user in self.get_users()["members"]]

    def get_messages(self):
        today = datetime.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        oldest = yesterday.timestamp()
        latest = tomorrow.timestamp()

        response = self.slack_client.conversations_history(
            channel=self.channel_id,
            latest=str(latest),
            oldest=str(oldest),
            count=1000
        )

        return response

    def get_author_name_from_commit_message(self, message):
        p = re.compile("by (.*)")
        github_id = p.findall(message)[0]
        return github_id

    def test_slack(self):
        # self.slack_client.chat_postMessage(
        #     channel='#junekim', # temp
        #     text='@junho85 test',
        #     link_names=1
        # )
        response = self.slack_client.users_list()
        print(response)
