# coding=utf-8
from selenium import webdriver
import unittest

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver

import page
import os


class TestSchedule(unittest.TestCase):
    def setUp(self):
        browser = os.environ.get("BROWSER")
        capability = {}
        if browser == "CHROME":
            capability = DesiredCapabilities.CHROME
        else:
            capability = DesiredCapabilities.FIREFOX
        self.browser = WebDriver(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=capability)
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
        group1 = 'BALinux-11'
        group2 = 'DevAppiOS-11'
        self.schedule_page.switchPeriod()
        self.schedule_page.changeGroup(group1)
        self.assertTrue(self.schedule_page.isGroupPresent(group1))
        self.schedule_page.changeGroup(group2)
        self.assertTrue(self.schedule_page.isGroupPresent(group2))

    def test_discipline_change(self):
        discipline1 = 'Разработка приложений на iOS '
        discipline2 = 'Программирование на Python'
        self.schedule_page.switchPeriod()
        self.schedule_page.changeDiscipline(discipline1)
        self.assertTrue(self.schedule_page.isDisciplinePresent(discipline1))
        self.schedule_page.changeDiscipline(discipline2)
        self.assertTrue(self.schedule_page.isDisciplinePresent(discipline2))

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
        event1 = 'Лекция'
        event2 = 'Семинар'
        self.schedule_page.switchPeriod()
        self.schedule_page.changeEvent(event1)
        self.assertTrue(self.schedule_page.isEventPresent(event1))
        self.schedule_page.changeEvent(event2)
        self.assertTrue(self.schedule_page.isEventPresent(event2))

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
        self.browser.quit()

if __name__ == '__main__':
    unittest.main()
