from selenium import webdriver
import unittest
import page
import time

class TestSchedule(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.schedule_page = page.SchedulePage(self.browser)
        self.schedule_page.signInAndNavigate()

    def test_open_schedule(self):
        self.assertTrue(self.schedule_page.isOpened())

    def test_changing_schedule_period(self):
        self.assertTrue(self.schedule_page.hasPeriodChanged())

    def test_group_change(self):
        self.assertTrue(self.schedule_page.hasGroupChanged())

    def test_discipline_change(self):
        self.assertTrue(self.schedule_page.hasDisciplineChanged())

    def test_calendar_scroll(self):
        self.assertTrue(self.schedule_page.hasScrolled())

    def test_mobile_version(self):
        self.assertTrue(self.schedule_page.hasWentMobile())

    def test_events_change(self):
        self.assertTrue(self.schedule_page.hasEventChanged())

    def test_info_popup(self):
        self.assertTrue(self.schedule_page.hasInfoPoppedUp())

    def test_blog_navigation(self):
        self.assertTrue(self.schedule_page.hasNavigatedToBlog())

    def test_subject_info_popup(self):
        self.assertTrue(self.schedule_page.hasSubjectInfoPoppedUp())

    def test_schedule_period(self):
        self.assertTrue(self.schedule_page.isOnlyTwoWeeks())

    def tearDown(self):
        self.browser.close()

if __name__ == '__main__':

    unittest.main()
