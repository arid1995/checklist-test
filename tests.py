from selenium import webdriver
import unittest
import page
import time

class TestSchedule(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.schedule_page = page.SchedulePage(self.browser)
        self.schedule_page.signInAndNavigate()

    def test_open_schedule(self):
        self.assertTrue(self.schedule_page.isOpened())

    def test_changing_schedule_period(self):
        origDate = self.schedule_page.getFirstDate()
        self.schedule_page.switchPeriod()
        changedDate = self.schedule_page.getFirstDate()
        self.assertNotEqual(origDate, changedDate)

    def test_group_change(self):
        self.assertTrue(self.schedule_page.hasGroupChanged())

    def test_discipline_change(self):
        self.assertTrue(self.schedule_page.hasDisciplineChanged())

    def test_calendar_scroll(self):
        self.schedule_page.scrollToBottomRight()
        origPosition = self.schedule_page.getWindowYCoordinates()
        self.schedule_page.clickCalendarDay()
        changedPosition = self.schedule_page.getWindowYCoordinates()
        self.assertNotEqual(origPosition, changedPosition)

    def test_mobile_version(self):
        self.schedule_page.switchToMobile()
        width = self.schedule_page.getScheduleWidth()
        self.assertEqual(width, '600px')

    def test_events_change(self):
        self.assertTrue(self.schedule_page.hasEventChanged())

    def test_info_popup(self):
        self.schedule_page.clickInfoIcon()
        self.assertTrue(self.schedule_page.hasInfoPoppedUp())

    def test_blog_navigation(self):
        self.schedule_page.clickBlogIcon()
        blogSection = self.schedule_page.getBlogSection()
        self.assertNotEqual(blogSection, None)

    def test_subject_info_popup(self):
        self.schedule_page.clickSchedulePill()
        self.assertTrue(self.schedule_page.hasSubjectInfoPoppedUp())

    def test_schedule_period(self):
        numberOfDays = self.schedule_page.getDisplayedDays()
        self.assertLess(numberOfDays, 15)

    def tearDown(self):
        self.browser.close()

if __name__ == '__main__':

    unittest.main()
