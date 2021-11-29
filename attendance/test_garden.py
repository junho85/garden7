from unittest import TestCase

from attendance.garden import Garden


class TestGarden(TestCase):
    garden = Garden()

    def test_send_error_message(self):
        self.garden.send_error_message("테스트 에러 메시지")