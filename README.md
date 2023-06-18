<br/>
<p align="center">
  <a href="https://github.com/overklassniy/dota-depots-manifests-parser">
    <img src="https://github.com/overklassniy/dota-depots-manifests-parser/blob/master/static/png/icon.png?raw=true" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">DotaOPDSG</h3>

  <p align="center">
    Автоподбор манифестов для скрипта загрузки старых патчей Dota 2
    <br/>
    <br/>
    <a href="https://github.com/overklassniy/dota-depots-manifests-parser/issues">Report Bug</a>
|
    <a href="https://github.com/overklassniy/dota-depots-manifests-parser/issues">Request Feature</a>
  </p>
</p>

![Issues](https://img.shields.io/github/issues/overklassniy/dota-depots-manifests-parser) 

## Содержание

* [О проекте](#О-проекте)
* [Как собрать](#Как-собрать)
  * [Требования](#Требования)
  * [Сборка](#Сборка)
* [Использование](#Использование)
* [План работ над проектом](#План-работ-над-проектом)
* [Содействие разработке](#Содействие-разработке)
* [Благодарности](#Благодарности)

## О проекте

![Screen Shot](https://github.com/overklassniy/dota-depots-manifests-parser/blob/master/.info/screenshot.png?raw=true)

Автоматический подбор манифестов депотов по времени релиза патча Dota 2

## Как собрать

Инструкция по сборке приложения

### Требования

* [Python](https://www.python.org/downloads/)

### Сборка

1. Клонируйте репозиторий

```sh
git clone https://github.com/overklassniy/dota-depots-manifests-parser.git
```

2. Установите Python библиотеки

```sh
pip install -r .info/requirements.txt
```

3. Создайте файл `version.txt` с любым содержимым

4. Запустите скрипт для сборки приложения
```sh
python setup.py build
```

## Использование

Подробная инструкция по использованию приложения может быть найдена здесь: [Dota Hub](https://discord.gg/EvG3xHC9e5)

## План работ над проектом

Посмотрите [открытые задачи](https://github.com/overklassniy/dota-depots-manifests-parser/issues) для списка предлагаемых функций (и известных проблем).

## Содействие разработке

Запросы на слияние (Pull Requests) - это то, что делает сообщество открытого программного обеспечения таким удивительным местом для обучения, вдохновения и творчества. Любые ваши запросы на слияние **очень ценятся**.

### Создание запроса на слияние (Pull Request)

1. Сделайте форк проекта.
2. Создайте свою ветку функциональности (`git checkout -b feature/AmazingFeature`).
3. Зафиксируйте свои изменения (`git commit -m 'Добавить замечательную функцию'`).
4. Отправьте изменения в ветку (`git push origin feature/AmazingFeature`).
5. Откройте запрос на слияние (Pull Request).

## Благодарности

* [ShaanCoding](https://github.com/ShaanCoding/ReadME-Generator)
* [Marcelo Duarte](https://github.com/marcelotduarte/cx_Freeze)
