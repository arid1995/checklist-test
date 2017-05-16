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

    def hasPeriodChanged(self):
        firstElement = WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, "//tr[@class='schedule-timetable__item']"))
        )

        firstDate = firstElement.get_attribute('data-date')

        periodElement = self.driver.find_element(By.XPATH, "//li/a[text()='Весь семестр']")
        periodElement.click()

        try:
            WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME).until(
                EC.presence_of_element_located(By.XPATH, "//tr[@data-date<%d]" % int(firstDate))
            )
        except TimeoutException:
            return False

        return True

    def __dropDownChecker(self, name1, name2, menuLocator, itemLocator):
        dropdown = self.driver.find_element(menuLocator).find_element_by_class_name('nav-pills_dropdown__active__title')

        dropdown.click()
        self.driver.find_element((By.XPATH, "//li/a[text()='%s']" % name1)).click()

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
                                      lambda s: (By.XPATH, "//nobr[text()='%s'" % s))

    def hasDisciplineChanged(self):
        return self.__dropDownChecker('Разработка приложений на iOS ', 'Программирование на Python',
                                      (By.XPATH, "//div[@class='schedule-filters__item "
                                                 "schedule-filters__item_discipline']"),
                                      lambda s: (By.XPATH, "//td/strong/a[text()='%s']" % s))
