from hstest import FlaskTest, dynamic_test

from test.base import (
    test_get_request_on_first_stage
)


class ServerTest(FlaskTest):
    source = 'app'

    @dynamic_test
    def test(self):
        return test_get_request_on_first_stage(self)


if __name__ == '__main__':
    ServerTest().run_tests()
