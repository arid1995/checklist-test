# coding=utf-8
import os
import time

from selenium.common.exceptions import TimeoutException

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
        lastDateElement = self.driver.find_elements(By.XPATH, "//tr[@class='schedule-timetable__item']")[-1:][0]
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
        dropdown = self.__getDropDown((By.XPATH, "//div[@class='schedule-filters__item schedule-filters__item_group']"))
        self.__clickOnDropdownElement(dropdown, name)

    def isGroupPresent(self, name):
        self.__waitForFirstElement()
        return self.__checkPresence((By.XPATH, "//nobr[text()='%s']" % name))

    def changeDiscipline(self, name):
        self.__waitForFirstElement()
        dropdown = self.__getDropDown((By.XPATH, "//div[@class='schedule-filters__item "
                                                 "schedule-filters__item_discipline']"))
        self.__clickOnDropdownElement(dropdown, name)

    def isDisciplinePresent(self, name):
        self.__waitForFirstElement()
        return self.__checkPresence((By.XPATH, "//td/strong/a[text()='%s']" % name))

    def changeEvent(self, name):
        self.__waitForFirstElement()
        dropdown = self.__getDropDown((By.XPATH, "//div[@class='schedule-filters__item schedule-filters__item_type']"))
        self.__clickOnDropdownElement(dropdown, name)

    def isEventPresent(self, name):
        self.__waitForFirstElement()
        return self.__checkPresence((By.XPATH, "//p[contains(., '%s')]" % name))

    def switchToMobile(self):
        self.driver.find_element(By.XPATH, "//a[text()='Мобильная версия']").click()
        self.driver.find_element(By.XPATH, "//span[text()='Мобильная версия']").click()

    def getScheduleWidth(self):
        schedule = ScheduleTable(self.driver).get()
        return schedule.value_of_css_property('max-width')

    def clickInfoIcon(self):
        self.driver.find_element(By.XPATH, "//a[@class='schedule-show-info icon-info-blue']").click()

    def hasInfoPoppedUp(self):
        return self.driver.find_element(By.XPATH, "//div[@class='modal modal-show-info jqm-init']").is_displayed()

    def clickBlogIcon(self):
        self.driver.find_element(By.XPATH, "//a[@class='icon-blog']").click()

    def getBlogSection(self):
        return self.driver.find_element(By.XPATH, "//div[@class='blog-section']")

    def clickSchedulePill(self):
        self.driver.find_element(By.XPATH, "//div[@class='schedule-item js-schedule-item']").click()

    def hasSubjectInfoPoppedUp(self):
        return self.__checkPresence((By.XPATH, "//div[@class='large-item__content']"))

    def getDisplayedDays(self):
        lastDate = self.getLastDate()
        return (lastDate - int(time.time() * 1000)) / 86400000

    def __waitForFirstElement(self):
        return WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, "//tr[@class='schedule-timetable__item']"))
        )

    def __waitUntilLoaded(self):
        WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[@class='icon-ajax-loader']"))
        )

    def __getDropDown(self, locator):
        return self.driver.find_element(*locator).find_element_by_class_name('nav-pills_dropdown__active__title')

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
