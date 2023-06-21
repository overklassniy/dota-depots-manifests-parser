import logging
import os
import sys
import winreg
from datetime import datetime as dt

import psutil
import requests
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QAction, QMessageBox
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from downloader_ui import Ui_MainWindow
from static import depot_URLs, month_dict, template


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        QtGui.QFontDatabase.addApplicationFont("static/font/MuseoSansCyrl.otf")
        self.font = QFont('MuseoSansCyrl', 14)

        try:
            self.settings = []
            settings = open('settings.txt', 'r').readlines()
            for setting in settings:
                tmp = setting.strip()
                self.settings.append(tmp)
            self.theme = int(self.settings[0])
            self.chrome_profile_path = self.settings[1]
        except Exception as e:
            # If settings file is not found, set default values
            self.settings = open('settings.txt', 'w')
            self.settings.write('0')
            if os.path.isdir(os.path.expandvars('%localappdata%/Google/Chrome/User Data')):
                self.chrome_profile_path = str(os.path.expandvars(r'%localappdata%/Google/Chrome/User Data'))
            else:
                QMessageBox.about(self, "Не найден путь к профилю Chrome",
                                  "У Вас не установлен путь к Вашему профилю Google Chrome. Пожалуйста, выберите папку, указанную в Вашем браузере на странице chrome://version (Путь к профилю)")
                self.chrome_profile_path = QFileDialog.getExistingDirectory(self, 'Select')
            self.settings.write(self.chrome_profile_path)
            self.settings.close()
            self.theme = 0
        self.set_theme(self.theme)

        try:
            self.version = open('version.txt', 'r', encoding='UTF-8').readline().strip().rstrip()
        except Exception as e:
            self.version = 'NOT FOUND version.txt'

        self.version_check()

        self.datetime_patch = ''
        self.out_script = ''
        self.web = ''

        self.action_theme_light.triggered.connect(self.light_theme_clicked)
        self.action_theme_dark.triggered.connect(self.dark_theme_clicked)

        self.action_author.triggered.connect(self.author_msg)
        self.action_app.triggered.connect(self.app_msg)

        self.pushButton_create.clicked.connect(self.create_download_script)

        self.quit = QAction(self)
        self.quit.triggered.connect(self.closeEvent)

        self.setWindowIcon(QIcon('static/png/icon.png'))

        # Setup debug logging
        logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s [DEBUG] %(message)s')

    def version_check(self):
        # URL релиза репозитория на GitHub
        releases_url = "https://api.github.com/repos/overklassniy/dota-depots-manifests-parser/releases/latest"
        response = requests.get(releases_url).json()
        latest_tag = response['tag_name']
        if self.version != latest_tag:
            msgBox = QMessageBox()
            msgBox.setFont(self.font)
            msgBox.setTextFormat(Qt.RichText)
            msgBox.setWindowIcon(QIcon('static/png/warning.png.png'))
            msgBox.setText('Доступна новая версия приложения!')
            msgBox.setWindowTitle('У Вас старая версия...')
            if self.version != 'NOT FOUND version.txt':
                msgBox.setInformativeText(
                    f"""<a>Установленная версия: </a><a href='https://github.com/overklassniy/dota-depots-manifests-parser/releases/tag/{self.version}'>{self.version}</a><br><br>
            <a><a>Новейшая версия: </a><a href='https://github.com/overklassniy/dota-depots-manifests-parser/releases/tag/{latest_tag}'>{latest_tag}</a>""")
            else:
                msgBox.setInformativeText(f"""<a>Подробная инструкция по использованию приложения может быть найдена здесь: </a><a href='https://discord.gg/EvG3xHC9e5'><br>Dota Hub</a><br><br>
            <a>Версия: {self.version}</a>""")
            msgBox.exec()

    def set_theme(self, n):
        """
        Set the interface theme based on the value of n.

        Arguments:
        - n (int): theme value (0 - light theme, 1 - dark theme)
        """
        if n == 0:
            self.light_theme_clicked()
            self.action_theme_light.setChecked(True)
        elif n == 1:
            self.dark_theme_clicked()
            self.action_theme_dark.setChecked(True)

    def light_theme_clicked(self):
        """Apply the light theme to the interface."""
        self.setStyleSheet(open('static/css/light_theme.css').read())
        self.theme = 0

    def dark_theme_clicked(self):
        """Apply the dark theme to the interface."""
        self.setStyleSheet(open('static/css/dark_theme.css').read())
        self.theme = 1

    def author_msg(self):
        """
        Show the author information message box.
        """
        msgBox = QMessageBox()
        msgBox.setFont(self.font)
        msgBox.setTextFormat(Qt.RichText)
        msgBox.setWindowIcon(QIcon('static/png/info.png'))
        msgBox.setText('Приложение разработано автором Discord сервера Dota Hub')
        msgBox.setWindowTitle('Об авторе')
        msgBox.setInformativeText("""<a href='https://discord.gg/EvG3xHC9e5'>(Discord) Dota Hub</a><br>
<a href='https://t.me/dota_patches'>(Telegram) Dota Hub</a><br>
<a href='https://github.com/overklassniy'>GitHub автора</a>""")
        msgBox.exec()

    def app_msg(self):
        """
        Show the application information message box.
        """
        msgBox = QMessageBox()
        msgBox.setFont(self.font)
        msgBox.setTextFormat(Qt.RichText)
        msgBox.setWindowIcon(QIcon('static/png/info.png'))
        msgBox.setText('Автоподбор манифестов для скрипта загрузки старых патчей Dota 2')
        msgBox.setWindowTitle('О приложении')
        if self.version != 'NOT FOUND version.txt':
            msgBox.setInformativeText(f"""<a>Подробная инструкция по использованию приложения может быть найдена здесь: </a><a href='https://discord.gg/EvG3xHC9e5'><br>Dota Hub</a><br><br>
<a>Версия: </a><a href='https://github.com/overklassniy/dota-depots-manifests-parser/releases/tag/{self.version}'>{self.version}</a>""")
        else:
            msgBox.setInformativeText(f"""<a>Подробная инструкция по использованию приложения может быть найдена здесь: </a><a href='https://discord.gg/EvG3xHC9e5'><br>Dota Hub</a><br><br>
<a>Версия: {self.version}</a>""")
        msgBox.exec()

    def find_patch_timestamp(self, patch_url):
        """
        Find the patch timestamp based on the patch URL.

        Arguments:
        - patch_url (str): patch URL

        Returns:
        - patch_timestamp (datetime.datetime): patch timestamp
        """
        patch_id = patch_url.split('/')[-2]
        search_url = '/patchnotes/' + patch_id + '/'
        self.web.get('https://steamdb.info/app/570/patchnotes/')
        bs_patch = BeautifulSoup(self.web.page_source, 'html.parser')
        bs_patches = bs_patch.find_all('a', href=True)
        bs_patch_el = next((element for element in bs_patches if search_url in str(element)), None)
        bs_patch_el_parent = bs_patch_el.parent
        bs_patch_el_parent_parent = bs_patch_el_parent.parent
        patch_timestamp = dt.fromtimestamp(float(str(bs_patch_el_parent_parent).split('\n')[0].split('"')[-2]) - 10800)
        return patch_timestamp

    def find_manifest(self, depot_url, patch_timestamp):
        """
        Find the manifest based on the depot URL and patch timestamp.

        Arguments:
        - depot_url (str): depot URL
        - patch_timestamp (datetime.datetime): patch timestamp

        Returns:
        - manifest (str): manifest
        """
        self.web.get(depot_url)
        bs_depot = BeautifulSoup(self.web.page_source, "html.parser")
        dates_depot = bs_depot.find_all(class_='text-right')
        manifests_depot = bs_depot.find_all(class_='tabular-nums')
        for date, manifest in zip(dates_depot, manifests_depot):
            date_parts = date.text.split(' – ')
            date_str, time_str = date_parts[0], date_parts[1]
            day, month, year = date_str.split()
            t_month = month_dict[month]
            t_date = f'{day} {t_month} {year}'
            t_datetime = f'{t_date} {time_str.split()[0]}'
            dt_date = dt.strptime(t_datetime, '%d %m %Y %H:%M:%S')
            if dt_date.timestamp() <= patch_timestamp + 300:
                return manifest.text

    def find_chrome_path(self):
        """
        Finds chrome installation path via registry
        """
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                          r"Software\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe")
            value, _ = winreg.QueryValueEx(registry_key, "")
            return str(value).replace('\\', '/')
        except Exception as e:
            print("Error: ", str(e))

    def create_download_script(self):
        """
        Create a script for downloading manifests.

        The script is saved in the selected output file.
        """
        self.out_script, _ = QFileDialog.getSaveFileName(self, 'Выбрать', 'script.txt', "Text files (*.txt)")
        self.statusbar.clearMessage()
        for proc in psutil.process_iter(['name']):
            if "chrome" in proc.info['name'].lower():
                proc.kill()
        chrome_options = Options()
        chrome_options.add_argument(f'user-data-dir={self.chrome_profile_path}')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.web = webdriver.Chrome(options=chrome_options)
        patch_url = self.lineEdit_patch.text()
        self.datetime_patch = self.find_patch_timestamp(patch_url)
        with open(self.out_script, 'w') as out_script:
            for depot, depot_url in depot_URLs.items():
                manifest = self.find_manifest(depot_url, self.datetime_patch.timestamp())
                out_script.write(template[depot].replace('XXXXXXXXXXXXXXXXXX', manifest.strip().rstrip()) + '\n')
        self.statusbar.showMessage('Скрипт создан!')
        self.statusbar.setStyleSheet("background-color: green; color: #eff0f1")
        self.web.close()

    def closeEvent(self, event):
        """
        Handler for the application close event.

        Closes the application and saves the current theme to the settings file.
        """
        with open('settings.txt', 'w') as settings:
            settings.write(f'{self.theme}\n')
            settings.write(self.chrome_profile_path.replace('\\', '/'))
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
