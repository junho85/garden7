from attendance.garden import Garden
from datetime import date, datetime, timedelta

garden = Garden()

today = datetime.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

oldest = yesterday.timestamp()
latest = tomorrow.timestamp()

try:
    garden.collect_slack_messages(oldest, latest)
except Exception as err:
    garden.send_error_message("[모니터링] 출석부 수집 에러발생!\n" + str(err))
    raise err

