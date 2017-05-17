# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time


class BasePage(object):
    DEFAULT_WAIT_TIME = 10
    ELEMENT_NOT_PRESENT_TIME = 2
    url = None
    login = 'arid1995@mail.ru.local'
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


class SchedulePage(BasePage):
    url = 'http://ftest.tech-mail.ru/schedule/'

    def isOpened(self):
        try:
            WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, "//table[@class='schedule-timetable']"))
            )
        except TimeoutException:
            return False
        return True

    def __waitForFirstElement(self):
        return WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, "//tr[@class='schedule-timetable__item']"))
        )

    def hasPeriodChanged(self):
        firstElement = self.__waitForFirstElement()

        firstDate = firstElement.get_attribute('data-date')

        periodElement = self.driver.find_element(By.XPATH, "//li/a[text()='Весь семестр']")
        periodElement.click()

        try:
            WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, "//tr[@data-date<%d]" % int(firstDate)))
            )
        except TimeoutException:
            return False

        return True

    def __dropDownChecker(self, name1, name2, menuLocator, itemLocator):
        self.__waitForFirstElement()

        dropdown = self.driver.find_element(*menuLocator).find_element_by_class_name(
            'nav-pills_dropdown__active__title')

        dropdown.click()
        self.driver.find_element(By.XPATH, "//li/a[text()='%s']" % name1).click()

        try:
            WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME).until(
                EC.presence_of_element_located(itemLocator(name1))
            )
        except TimeoutException:
            return False

        dropdown.click()
        self.driver.find_element(By.XPATH, "//li/a[text()='%s']" % name2).click()

        try:
            WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME).until(
                EC.presence_of_element_located(itemLocator(name2))
            )
        except TimeoutException:
            return False

        return True

    def hasGroupChanged(self):
        return self.__dropDownChecker('BALinux-11', 'DevAppiOS-11',
                                      (By.XPATH, "//div[@class='schedule-filters__item schedule-filters__item_group']"),
                                      lambda s: (By.XPATH, "//nobr[text()='%s']" % s))

    def hasDisciplineChanged(self):
        return self.__dropDownChecker('Разработка приложений на iOS ', 'Программирование на Python',
                                      (By.XPATH, "//div[@class='schedule-filters__item "
                                                 "schedule-filters__item_discipline']"),
                                      lambda s: (By.XPATH, "//td/strong/a[text()='%s']" % s))

    def hasScrolled(self):
        self.__waitForFirstElement()
        firstPosition = self.driver.execute_script('window.scrollTo(document.body.scrollWidth, '
                                                   'document.body.scrollHeight); '
                                                   'return document.body.scrollHeight')
        self.driver.find_element(By.XPATH, "//td[@class='calendar-month__body__item__day "
                                           "calendar-month__body__item__day_active']").click()
        time.sleep(0.4)
        lastPosition = self.driver.execute_script('return window.pageYOffset')
        if firstPosition != lastPosition:
            return True
        return False

    def hasWentMobile(self):
        self.driver.find_element(By.XPATH, "//a[text()='Мобильная версия']").click()
        schedule = self.driver.find_element(By.XPATH, "//table[@class='schedule-timetable']")
        if schedule.value_of_css_property('max-width') == '600px':
            return True
        return False

    def hasEventChanged(self):
        return self.__dropDownChecker('Лекция', 'Семинар',
                                      (By.XPATH, "//div[@class='schedule-filters__item schedule-filters__item_type']"),
                                      lambda s: (By.XPATH, "//p[contains(., '%s')]" % s))

    def hasInfoPoppedUp(self):
        self.driver.find_element(By.XPATH, "//a[@class='schedule-show-info icon-info-blue']").click()
        return self.driver.find_element(By.XPATH, "//div[@class='modal modal-show-info jqm-init']").is_displayed()

    def hasNavigatedToBlog(self):
        self.driver.find_element(By.XPATH, "//a[@class='icon-blog']").click()
        try:
            WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='blog-section']"))
            )
        except TimeoutException:
            return False
        return True

    def hasSubjectInfoPoppedUp(self):
        self.driver.find_element(By.XPATH, "//div[@class='schedule-item js-schedule-item']").click()
        try:
            WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='qtip qtip-default schedule-item-popup "
                                                          "qtip-pos-tl qtip-focus']"))
            )
        except TimeoutException:
            return False
        return True

    def isOnlyTwoWeeks(self):
        self.__waitForFirstElement()
        lastElement = self.driver.find_elements(By.XPATH, "//tr[@class='schedule-timetable__item']")[-1:][0]

        lastDate = int(lastElement.get_attribute('data-date'))
        if lastDate > int(time.time() * 1000) + 1209600000:
            return False
        return True
