import allure
from selene import browser, have, be
from project.data.users import User
from project.data.cars import Car
from utils.logger import step


class MainPage:

    @step
    @allure.step("UI: open browser")
    def open(self):
        browser.open("/")

    @step
    @allure.step('UI: Authorization registered user')
    def authorization_registered_user(self, user: User):
        browser.element('#loginInfo').click()
        browser.element('#Login').should(be.blank).send_keys(user.username)
        browser.element('#Password').should(be.blank).send_keys(user.password)
        browser.element('.icon.fa').click()
        browser.element('#submit_logon_page').click()
        browser.element('#user_info').should(have.exact_text(user.username))

    @step
    @allure.step('UI: Authorization unregistered user')
    def authorization_unregistered_user(self, user: User):
        browser.element('.cabinet.ng-star-inserted').click()
        browser.element('#Login').send_keys(user.username)
        browser.element('#Password').send_keys(user.password)
        browser.element('.icon.fa').click()
        browser.element('#submit_logon_page').click()
        browser.element('#errorMessage').should(have.exact_text('Не удалось авторизоваться.'))

    @step
    @allure.step("UI: Checking authorization")
    def user_should_be_authorized(self, user):
        browser.element('#user_info').should(have.exact_text(user))

    @step
    @allure.step("UI: Checking authorization form")
    def registration_form_should_have_exact_visible_text(self):
        browser.element('.registration').click()
        browser.element('.title').should(have.text('Регистрация пользователя'))

    @step
    @allure.step("UI: Checking balance form")
    def main_page_auth_user_should_have_exact_visible_text(self, name):
        browser.element('.balance-main').should(have.text(name))

    @step
    @allure.step("UI: Search")
    def search_item_by_tool_number(self, value):
        browser.element('#partNumberSearch').should(be.blank).send_keys(value)
        browser.element('.search-button').click()
        browser.element('.breadcrumbs-header').should(have.text(value))

    @step
    @allure.step("UI-API: Search")
    def search_item_by_tool_name_and_number(self, name, value):
        browser.element('#partNumberSearch').should(be.blank).send_keys(name, value)
        browser.element('.search-button').click()
        browser.element('.sub-nav.promark.ng-star-inserted').should(have.text(name))

    @step
    @allure.step("UI: Search by VIN number")
    def search_by_vin_number(self, car: Car):
        browser.element('[name=vin]').should(be.blank).send_keys(car.vin)
        browser.element('.btn-transparent').click()
        browser.element('.breadcrumbs').should(have.text('Оригинальный каталог'))

    @step
    @allure.step("UI: Checking phrase")
    def main_page_should_have_visible_text(self):
        browser.element('.homepage-content__title').should(have.exact_text('Запчасти в интернет-магазине Автодок'))

    @step
    @allure.step("UI: Clear cart")
    def clear_cart(self):
        browser.element('.a-icon.a-cart').click()
        browser.element('.button-red').click()
        browser.element('.p-element.button-red.p-button.p-component').click()


main_page = MainPage()