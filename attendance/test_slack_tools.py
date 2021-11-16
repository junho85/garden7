from unittest import TestCase

from attendance.slack_tools import SlackTools
from attendance.config_tools import ConfigTools
import re

class TestSlackTools(TestCase):
    slack_tools = SlackTools()
    config_tools = ConfigTools()

    def test_get_users(self):
        print(self.slack_tools.get_users())

    def test_get_user_names(self):
        print(self.slack_tools.get_user_names())

    def test_get_user_slacknames(self):
        print(self.config_tools.get_user_slacknames())

    '''
    slack에 있는 유저들 - users.yaml에 등록된 slack이름을 뺌. 거기다가 봇들 제외
    다 등록 되었으면 결과에 아무 유저가 나오면 안됨
    '''
    def test_user_diff(self):
        print(set(self.slack_tools.get_user_names())
              - set(self.config_tools.get_user_slacknames())
              - {"slackbot",
                 "garden7",
                 "github"})

    '''
    users.yaml에 등록된 slack이름 - slack에 있는 유저들
    '''
    def test_user_diff2(self):
        print(set(self.config_tools.get_user_slacknames())
              - set(self.slack_tools.get_user_names())
              )

    '''
    자기소개 방에 있는 유저들의 github 주소를 기준으로 slack name 구하기
    '''
    def test_get_users(self):
        p = re.compile('/github.com/(.*)/')

        # 자기소개방에서 github 주소가 있는 글 추출
        response = self.slack_tools.get_slack_client().conversations_history(
            channel="C02MA9HUSV9"
        )

        for message in response["messages"]:
            if "github.com" in message["text"]:
                github_id = p.findall(message["text"])[0]
                github_id = github_id.split("/")[0]
                # print(message["user"])
                response2 = self.slack_tools.get_slack_client().users_info(
                    user=message["user"]
                )
                print(github_id + ":")
                print("  slack: " + response2["user"]["name"])
                # print(message["text"])

    '''
    channel list 구하기.
     - 자기소개 channel id: C02MA9HUSV9
     - commit channel id: C02N0D83A3A
    '''
    def test_get_channels(self):
        result = self.slack_tools.get_slack_client().conversations_list()
        print(result)