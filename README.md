# SDET_Practicum_FirstWeek
<h2>Решение ТЗ первой недели практикума от SimbirSoft</h2>
<h3>Что использовалось и реализованно?</h3>
<ul>
    <li>Язык - Python 3.10</li>
    <li>Инструменты - Selenium, Pytest, Pytest-Xdist, Allure</li>
    <li>Паттерны проектирования - Page Object Model, Page Factory</li>
</ul>

<h3>Объект тестирования и чек-лист</h3>
<p>Объект - https://automationteststore.com/</p>
<strong>Чек-Лист</strong></br>
<ul></ul>

<h2>Установка и запуск</h2>
<ol>
    <li>Клонировать репозиторий</li>
    <li>Настроить переменные окружения в <code>.venv</code></li>
    <li>Установить зависимости: <code>pip install -r requirements.txt</code></li>
    <li>Запустить тесты с нужными вам параметрами: <code>pytest -v -s</code> - это выдаст подробное описание тестов и все print</li>
    <li>Если вам нужен конректные тесты (Поиск элементов, Положительные или Негативные тесты), то запускайте так - <code>cd tests</code>, потом <code>pytest *Название файла*</code></li>
    <li>Если вам нужен тест какой-то из тест-кейса (функцию), то запускайте так - <code>cd tests</code>, потом <code>pytest *Название файла*::*Название класса тестов*::*Название теста*</code></li>
    <li>Если нужен отчет allure, можете локально запустить свой - <code>pytest --alluredir=allure-results</code></li>
    <li>Далее прописываете <code>allure serve allure-results</code></li>
    <li>Если нужно быстро пройтись по тестам, можно использовать несколько воркеров для запуска параллельных тестов - <code>pytest -v -n auto</code></li>
</ol>