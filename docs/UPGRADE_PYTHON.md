# Python 3.7.5 → 3.11.11 업그레이드 변경사항

## 주요 변경사항

### 1. Python 버전 업그레이드
- Python 3.7.5 → 3.11.11
- `.python-version` 파일 추가

### 2. Django 및 패키지 업데이트
- Django 3.0.3 → 4.2+ (requirements.txt 참조)
- 모든 주요 패키지를 Python 3.11 호환 버전으로 업데이트

### 3. Django 설정 변경 (settings.py)
- `os.path` → `pathlib.Path` 사용
- `BASE_DIR` 정의 방식 변경
- `DEFAULT_AUTO_FIELD` 설정 추가
- `USE_L10N` 설정 제거 (Django 4.0+에서 deprecated)

## 마이그레이션 가이드

1. **백업**
   ```bash
   pip freeze > requirements_backup.txt
   ```

2. **새 가상환경 생성**
   ```bash
   python3.11 -m venv venv_new
   source venv_new/bin/activate
   ```

3. **패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **데이터베이스 마이그레이션**
   ```bash
   python manage.py migrate
   ```

5. **테스트 실행**
   ```bash
   python manage.py test
   ```

## 주의사항

- 기존 가상환경(venv)은 Python 3.8로 설정되어 있으므로 새로운 가상환경 생성 필요
- MongoDB 연결 설정 확인 필요
- Slack 관련 설정 파일들의 호환성 확인 필요

## 롤백 방법

문제 발생 시:
1. `requirements_backup.txt` 사용하여 이전 패키지 버전으로 복원
2. settings.py의 변경사항 되돌리기
3. Python 3.7 환경으로 돌아가기