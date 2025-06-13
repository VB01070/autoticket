from argparse import Namespace


class StartingInfoParsed:
    def __init__(self, page):
        self.page = page
        self.page.app_state = page.app_state
        self.args = None

    def get_basic_info_from_app(self):
        test_uuid = self.page.report_test_uuid_text_field.value
        service_name = self.page.service_type_dropdown.value
        test_start = self.page.start_test
        test_end = self.page.end_test

        self.args = Namespace(
            pentest=test_uuid,
            service=service_name,
            test_start=test_start,
            test_end=test_end
        )
