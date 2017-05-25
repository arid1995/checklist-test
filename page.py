# coding=utf-8
import os
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver

from elements import *


class BasePage(object):
    DEFAULT_WAIT_TIME = 10
    ELEMENT_NOT_PRESENT_TIME = 2
    url = None
    login = os.environ.get("TP_LOGIN")
    password = os.environ.get("PASSWORD")

    def __init__(self, driver):
        self.driver = driver

    def signIn(self):
        self.driver.find_element(By.XPATH, "//a[text()='Вход для участников']").click()
        self.driver.find_element(By.XPATH, "//input[@name='login']").send_keys(self.login)
        self.driver.find_element(By.XPATH, "//input[@name='password']").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@name='submit_login']").click()

    def navigate(self):
        self.driver.get(self.url)

    def signInAndNavigate(self):
        self.navigate()
        self.signIn()
        WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='dropdown-user']"))
        )
        self.navigate()

    def scrollToBottomRight(self):
        return self.driver.execute_script('window.scrollTo(document.body.scrollWidth, '
                                          'document.body.scrollHeight); '
                                          'return document.body.scrollHeight')

    def getWindowYCoordinates(self):
        return self.driver.execute_script('return window.pageYOffset')

    def getWindowXCoordinates(self):
        return self.driver.execute_script('return window.pageXOffset')


class SchedulePage(BasePage):
    url = 'http://ftest.tech-mail.ru/schedule/'

    def isOpened(self):
        try:
            ScheduleTable(self.driver)
        except TimeoutException:
            return False
        return True

    def getFirstDate(self):
        firstElement = self.__waitForFirstElement()
        return firstElement.get_attribute('data-date')

    def getLastDate(self):
        self.__waitForFirstElement()
        lastDateElement = ScheduleElement(self.driver).getLast()
        return int(lastDateElement.get_attribute('data-date'))

    def switchPeriod(self):
        periodSwitcher = PeriodSwitcher(self.driver).get()
        periodSwitcher.click()
        self.__waitUntilLoaded()

    def clickCalendarDay(self):
        self.__waitForFirstElement()
        self.scrollToBottomRight()
        CalendarDayNumber(self.driver).get().click()

    def changeGroup(self, name):
        self.__waitForFirstElement()
        dropdown = GroupDropdown(self.driver).get()
        self.__clickOnDropdownElement(dropdown, name)

    def isGroupPresent(self, name):
        self.__waitForFirstElement()
        return self.__checkPresence((By.XPATH, "//nobr[text()='%s']" % name))

    def changeDiscipline(self, name):
        self.__waitForFirstElement()
        dropdown = DisciplineDropdown(self.driver).get()
        self.__clickOnDropdownElement(dropdown, name)

    def isDisciplinePresent(self, name):
        self.__waitForFirstElement()
        return self.__checkPresence((By.XPATH, "//td/strong/a[text()='%s']" % name))

    def changeEvent(self, name):
        self.__waitForFirstElement()
        dropdown = EventDropdown(self.driver).get()
        self.__clickOnDropdownElement(dropdown, name)

    def isEventPresent(self, name):
        self.__waitForFirstElement()
        return self.__checkPresence((By.XPATH, "//p[contains(., '%s')]" % name))

    def switchToMobile(self):
        self.scrollToBottomRight()
        self.driver.find_element(By.XPATH, "//a[text()='Мобильная версия']").click()
        self.driver.find_element(By.XPATH, "//span[text()='Мобильная версия']").click()

    def getScheduleWidth(self):
        schedule = ScheduleTable(self.driver).get()
        return schedule.value_of_css_property('max-width')

    def clickInfoIcon(self):
        InfoIcon(self.driver).get().click()

    def hasInfoPoppedUp(self):
        return SubjectInfoPopup(self.driver).get().is_displayed()

    def clickBlogIcon(self):
        BlogIcon(self.driver).get().click()

    def getBlogSection(self):
        return BlogSection(self.driver).get()

    def clickSchedulePill(self):
        SchedulePill(self.driver).get().click()

    def hasSubjectInfoPoppedUp(self):
        return self.__checkPresence(ClassInfoPopup(self.driver).locator)

    def getDisplayedDays(self):
        lastDate = self.getLastDate()
        return (lastDate - int(time.time() * 1000)) / 86400000

    def __waitForFirstElement(self):
        return ScheduleElement(self.driver).get()

    def __waitUntilLoaded(self):
        AjaxLoader().waitToDisappear(self.driver)

    def __clickOnDropdownElement(self, dropdown, name):
        dropdown.click()
        self.driver.find_element(By.XPATH, "//li/a[text()='%s']" % name).click()
        self.__waitUntilLoaded()

    def __checkPresence(self, locator):
        try:
            WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
