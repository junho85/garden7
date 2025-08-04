# garden7
* 정원사들 시즌7 출석부입니다.
* slack #commit 채널에 올라온 메시지들을 수집해서 출석부를 작성합니다.
* [시즌7 출석부 바로가기 gogo](http://garden7.junho85.pe.kr/)
* [github](https://github.com/junho85/garden7)
* [wiki](https://github.com/junho85/garden7/wiki)

## Requirements
* Python 3.11.11
* MongoDB

## project

### Python 환경 설정
Python 3.11.11 설치 (macOS)
```
brew install python@3.11
```

가상환경 생성 및 활성화
```
python3.11 -m venv venv
source venv/bin/activate
```

패키지 설치
```
pip install --upgrade pip
pip install -r requirements.txt
```

### MongoDB 시작
```
docker start mymongo
```

### 개발 서버 실행
```
python manage.py migrate
python manage.py runserver
```

자세한 내용은 [docs](docs)의 내용을 참고합니다.

## 참고
* [garden6 github](https://github.com/junho85/garden6)
* [garden5 github](https://github.com/junho85/garden5)
* [garden4 github](https://github.com/junho85/garden4)