# coding=utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_WAIT_TIME = 10

class BaseElement(object):
    locator = None

    def __init__(self, driver):
        self.element = WebDriverWait(driver, DEFAULT_WAIT_TIME).until(
            EC.presence_of_element_located(self.locator)
        )
        self.driver = driver

    def get(self):
        return self.element


class ScheduleTable(BaseElement):
    locator = (By.XPATH, "//table[@class='schedule-timetable']")


class PeriodSwitcher(BaseElement):
    locator = (By.XPATH, "//li/a[text()='Весь семестр']")


class CalendarDayNumber(BaseElement):
    locator = (By.XPATH, "//td[@class='calendar-month__body__item__day calendar-month__body__item__day_active']")


class ScheduleElement(BaseElement):
    locator = (By.XPATH, "//tr[@class='schedule-timetable__item']")

    def getLast(self):
        return self.driver.find_elements(*self.locator)[-1:][0]


class Dropdown(BaseElement):
    locator = None

    def get(self):
        return self.element.find_element_by_class_name('nav-pills_dropdown__active__title')


class GroupDropdown(Dropdown):
    locator = (By.XPATH, "//div[@class='schedule-filters__item schedule-filters__item_group']")


class DisciplineDropdown(Dropdown):
    locator = (By.XPATH, "//div[@class='schedule-filters__item schedule-filters__item_discipline']")


class EventDropdown(Dropdown):
    locator = (By.XPATH, "//div[@class='schedule-filters__item schedule-filters__item_type']")


class InfoIcon(BaseElement):
    locator = (By.XPATH, "//a[@class='schedule-show-info icon-info-blue']")


class SubjectInfoPopup(BaseElement):
    locator = (By.XPATH, "//div[@class='modal modal-show-info jqm-init']")


class BlogIcon(BaseElement):
    locator = (By.XPATH, "//a[@class='icon-blog']")


class BlogSection(BaseElement):
    locator = (By.XPATH, "//div[@class='blog-section']")


class SchedulePill(BaseElement):
    locator = (By.XPATH, "//div[@class='schedule-item js-schedule-item']")


class ClassInfoPopup(BaseElement):
    locator = (By.XPATH, "//div[@class='large-item__content']")


class AjaxLoader(object):
    locator = (By.XPATH, "//div[@class='icon-ajax-loader']")

    def waitToDisappear(self, driver):
        WebDriverWait(driver, DEFAULT_WAIT_TIME).until(
            EC.invisibility_of_element_located(self.locator)
        )
