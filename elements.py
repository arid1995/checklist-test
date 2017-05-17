# coding=utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseElement(object):
    locator = None

    def __init__(self, driver):
        self.element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(self.locator)
        )

    def get(self):
        return self.element


class ScheduleTable(BaseElement):
    locator = (By.XPATH, "//table[@class='schedule-timetable']")


class PeriodSwitcher(BaseElement):
    locator = (By.XPATH, "//li/a[text()='Весь семестр']")


class CalendarDayNumber(BaseElement):
    locator = (By.XPATH, "//td[@class='calendar-month__body__item__day calendar-month__body__item__day_active']")