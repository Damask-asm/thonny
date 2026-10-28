Thonny Classroom 5.0.0.1 — неофициальная сборка
============================================

Независимая модификация Thonny для занятий Python. Это не официальный выпуск
разработчиков Thonny. Оригинальные лицензии MIT, авторство и уведомления
компонентов сохранены в LICENSE.txt, CREDITS.rst и licenses/.

Скачать и установить
-------------------

https://github.com/Damask-asm/thonny/releases/latest

Скачайте ``Thonny-Classroom-5.0.0-x64-Setup.exe`` и ``SHA256SUMS.txt``.
Требуется Windows 10/11 x64. Встроенный Python 3.14.4 уже включен.
Проверка: ``Get-FileHash .\Thonny-Classroom-5.0.0-x64-Setup.exe -Algorithm SHA256``.
Запустите мастер от обычного пользователя: права администратора не требуются.
Есть ярлыки меню «Пуск» и рабочего стола, удаление через настройки Windows.
Установщик не подписан сертификатом издателя.

Каталог установки: ``%LOCALAPPDATA%\Programs\Thonny-Classroom``.
Отдельный профиль: ``%APPDATA%\Thonny-Classroom``. Официальный Thonny и
ассоциации файлов не изменяются. Не выбирайте каталог другого приложения.
При первом запуске можно выбрать русский язык. Настройки и файлы уроков
при удалении сохраняются.

Отличия и происхождение
-----------------------

Основа строго официальный v5.0.0, commit
``5eb79646973128838818c960d6dcefa85086c603``.
Ветка ``classroom-5.0.0`` не включает более новые изменения upstream.

* В ``thonny/workbench.py`` удалены регистрация SupportUkraine и связанные
  обработчики: нет кнопки с флагом и пункта Support Ukraine в меню Help.
* В ``thonny/__init__.py`` изменен только каталог профиля Windows.
* Редактор, отладчик, переменные, встроенный Python, русская локализация и
  остальные компоненты сохранены. Неиспользуемые ресурсы upstream сохранены.

Берется официальный portable-комплект Windows 5.0.0 с закрепленным SHA-256.
Проверяется совпадение двух исходных модулей комплекта с upstream commit,
после чего они заменяются модулями из этого форка. Пакеты pip не скачиваются.
Отдельный Inno Setup используется потому, что оригинальный batch зависит от
локального Python разработчика, незакрепленных пакетов и его сертификата.

Исходники и самостоятельная сборка
----------------------------------

https://github.com/Damask-asm/thonny/tree/classroom-5.0.0

Исходники также доступны в Source code каждого релиза.
На Windows x64 с Git и Python 3.12+::

    git clone --branch classroom-v5.0.0.1 https://github.com/Damask-asm/thonny.git
    cd thonny
    python classroom/prepare.py

Установите скачанный ``build/downloads/innosetup-6.4.3.exe`` (либо используйте
параметры установки компилятора из workflow). Затем::

    build\bundle\python.exe -I classroom\smoke.py
    build\bundle\python.exe -I classroom\gui_smoke.py
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" classroom\installer.iss
    Get-FileHash dist\Thonny-Classroom-5.0.0-x64-Setup.exe -Algorithm SHA256

Используйте чистый checkout/build для каждой сборки. Входной runtime,
зависимости, компилятор и Actions закреплены хешами. Побитовая идентичность
EXE не обещается: метки времени и версии Windows runner могут отличаться.
``build-inputs.json`` записывает исходный commit и SHA-256 входных файлов.

GitHub Actions и публикация
--------------------------

Actions → Build Windows Classroom → Run workflow → classroom-5.0.0.
EXE, SHA-256, manifest и протоколы тестов находятся в artifact
``Thonny-Classroom-5.0.0-x64`` (30 дней).

Workflow Publish Classroom Release запускается при push тега
``classroom-v5.0.0.1`` и после тех же проверок создает постоянный публичный
GitHub Release, помеченный latest. Для новых версий нужно согласованно
обновить номер установщика и документацию. Публикация::

    git tag classroom-v5.0.0.1
    git push origin classroom-v5.0.0.1

Сборка имеет только contents:read. Право contents:write получает только
отдельный job публикации после успешных тестов. Actions закреплены commit SHA,
credentials checkout не сохраняются. Сборка не использует секреты,
pull request workflow не запускается. Официальный upstream не изменяется.

Проверки
--------

Автоматически: синтаксис; отсутствие регистрации команды, кнопки и пункта меню;
создание настоящего Tk-окна с плагинами и русской локализацией; запуск backend;
выполнение Python; переменные; шаги штатного отладчика с проверкой значений;
компиляция Inno; тихая установка; повтор тестов из установленного каталога;
проверка обоих ярлыков; удаление приложения и ярлыков.

Визуальная приемка мастера и ручных клавиатурных действий в Windows 10/11
остается отдельной проверкой. Инструкция: ``classroom/MANUAL_TESTS.md``.

======
Thonny
======

Thonny is a Python `IDE <https://en.wikipedia.org/wiki/Integrated_development_environment>`_ meant for learning programming.


End users
---------
See https://thonny.org and `wiki <https://github.com/thonny/thonny/wiki>`_ for more info.


Contributors
------------
Contributions are welcome! See `CONTRIBUTING.rst <https://github.com/thonny/thonny/blob/master/CONTRIBUTING.rst>`_ for more info.


Sponsors
----------
You can sponsor development of Thonny by sending a donation to Thonny's main author Aivar Annamaa: https://github.com/thonny/thonny/wiki/Sponsors
