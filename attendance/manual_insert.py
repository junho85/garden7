from datetime import datetime

from garden import Garden

from attendance.mongo_tools import MongoTools

import pprint
import requests

from urllib.parse import urlparse

mongo_tools = MongoTools()

garden = Garden()

mongo_collection = mongo_tools.get_collection()

def get_commit(commit_url):
    parse_result = urlparse(commit_url)
    # print(parse_result)
    (_, user, repo, commit, sha) = parse_result.path.split("/")

    api_url = 'https://api.github.com/repos/%s/%s/commits/%s' % (user, repo, sha)

    r = requests.get(api_url)

    # pprint(r)
    # print(r.json())
    commit_json = r.json()

    ts_datetime = datetime.strptime(commit_json["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%S%z")
    commit_message = commit_json["commit"]["message"]
    ts = str(ts_datetime.timestamp())
    return {
        "user": user,
        "ts": ts,
        "ts_datetime": ts_datetime,
        "sha": sha,
        "sha_short": sha[:8],
        "message": commit_message,
        }


def manual_insert(commit_url):
    commit = get_commit(commit_url)
    print("commit:")
    print(commit)
    print("user:" + commit["user"])
    print("sha:" + commit["sha"])
    print("sha_short:" + commit["sha_short"])
    print("ts:" + commit["ts"])
    print("ts_datetime:" + str(commit["ts_datetime"]))
    print("ts_datetime %Y-%m-%d:" + commit["ts_datetime"].strftime("%Y-%m-%d"))
    print("message:" + commit["message"])

    today = datetime.today().strftime("%Y-%m-%d")
    fallback = '*manual insert %s by june.kim* - commit by %s' % (today, commit["user"])
    text = '`<%s|%s>` - %s' % (commit_url, commit["sha_short"], commit["message"])

    user = 'U02LXDBJZRV'
    message = {'attachments':
        [{
            'fallback': fallback,
            'text': text
        }],
        'author_name': commit["user"],
        'ts': commit["ts"],
        'ts_for_db': commit["ts_datetime"],
        'type': 'message',
        'user': user
    }

    pprint.pprint(message)
    # exit(-1)

    try:
        result = mongo_collection.insert_one(message)
        pprint.pprint(result)
        print(message)
    except Exception as e:
        print(e)

commit_urls = [
    # 오스카
    # 'https://github.com/lunaticfoxy/TIL/commit/295f8bfa02a1d65794eacb95dec3ca05d08bd7bb', # 11.15
    # genie-youn
    # 'https://github.com/genie-youn/TIL/commit/c3e59e5dfdf02347808e4cf167324b33970c08ef', # 11.15
    # 클로이
    # 'https://github.com/chloeeekim/TIL/commit/567d40daf425dc79365835b9196789c510084392',  # 11.15
    # 최혜원
    # 'https://github.com/xizsmin/TIL/commit/15e8bd79dfd821f2344e4dbd59f6af569fcc65b6',  # 11.15
    # 샐리
    # 'https://github.com/sally-yeom/TIL/commit/0780869aa43301d8d5627b28623f6e26fc82393c',  # 11.15
    # 김희라_sage
    # 'https://github.com/lallaheeee/TIL/commit/806efe4cc6d6b5730ea3f5abb417b682bea0423c',  # 11.15
    # 강지혜
    # 'https://github.com/wwisdom46/TIL/commit/e35e4705abd639c51290e2e2457f43571ada5aa6',  # 11.15
    # 김규태
    # 'https://github.com/gyutae100/TIL/commit/31081cf844ec792ab8227942ef4eace5de9d0250',  # 11.15
    # InseobJeon
    # 'https://github.com/InseobJeon/the-gardeners-7th-inseob/commit/33c894daa863e1d57cec19c0bf4dad565a84ad60',
    # junho85
    # jiyeoon
    # 'https://github.com/jiyeoon/TIL/commit/32f605c8e46fb207fc9299846c9fd532520f983a', # 11.15
    # 노찬우
    # 'https://github.com/rajephon/TIL/commit/58f3275cd1c2f13ff3a42c1d720c7996d750ee3b',  # 11.15
    # 미카
    # 'https://github.com/lumiamitie/TIL/commit/76d2d1bd716fde1851ddd96f5505e5f4af5d0ee3', # 11.15
    # 'https://github.com/lumiamitie/TIL/commit/c6169c3a7f1121e4d51815727cc8c8e51327ccd0', # 11.15
    # 최준우
    # 'https://github.com/mike6321/TIL/commit/53dee824e2a87c6131d6fbca813593096bfcbaf5', # 11.15
    # 'https://github.com/mike6321/TIL/commit/e3edbe45aa30b5174b2794e58953a4872f09bde8', # (16일)
    # 'https://github.com/mike6321/TIL/commit/c42b813ba927a1bd4e96aeda74f2874fa88b47d2', # (17일)
    # 'https://github.com/mike6321/TIL/commit/6a1e1e146e0762e9cff0622172e9e9b720e7da45', # (18일)
    # 'https://github.com/mike6321/TIL/commit/108081254525a7e37835b2cfa52d67e5ff4de268', # (19일)
    # 'https://github.com/mike6321/TIL/commit/9e33b27b3c052654040753e2f249ef25dc65163d', # (20일)
    # 지나
    # 'https://github.com/koyrkr/TIL/commit/47c2f18728af3e0cc6935d079ad2383e6f388cd7',  # 11.15 - 11.16 00:57
    # 김도담
    # 'https://github.com/dodam-kim/TIL/commit/d833e75e67485d0438ce0c84f3bdf4f47e99b9c2',  # 11.15
    # codingbowoo
    # 고언약
    # 'https://github.com/brave-people/Dev-Event/commit/3e4fe876c29e9cd386c06f604cdcce7aec1dcef6', # 11.15 repo가 다르지만 처음이라 인정. author_name 수작업 필요
    'https://github.com/KoEonYack/0x01/commit/38e82a4eb736da7a146529ca07588fc86d343593', # 02.22
    # estellechoi
    # DS-DavGu
    # bloomspes
    # 'https://github.com/bloomspes/hackerrank/commit/82ea28ab73e37c662668c151e436c215a522332e', # 22
    # 'https://github.com/bloomspes/hackerrank/commit/62bc8fd3751615751fea7ad443e87f547ff11bae', # 22
    # 'https://github.com/bloomspes/hackerrank/commit/543a397898113f7066c89ee43a142f5c7ee45cf7', # 18
    # 'https://github.com/bloomspes/hackerrank/commit/74f709fe8f9eef052a8436ec8c678d9d67664fa5', # 18
    # heejour
]

for commit_url in commit_urls:
    manual_insert(commit_url)
