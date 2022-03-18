import os

from hstest import FlaskTest, dynamic_test, WrongAnswer

from test.base import (
    test_correct_request,
    test_bad_request,
    test_get_events,
    test_today_events
)


class ServerTest(FlaskTest):
    source = 'app'

    funcs = [
        test_correct_request,
        test_bad_request,
        test_get_events,
        test_today_events
    ]

    def generate(self):
        if os.path.exists('event.db'):
            try:
                os.remove('event.db')
            except Exception:
                raise WrongAnswer("Can't delete the database file before starting the tests!")
        return []

    @dynamic_test(data=funcs)
    def test_correct_request(self, func):
        return func(self)


if __name__ == '__main__':
    ServerTest().run_tests()
