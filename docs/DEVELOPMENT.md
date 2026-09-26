# Разработка

## Окружение

Проверяемая платформа — Windows 10/11 x64, Python 3.12. Из корня репозитория:

```powershell
py -3.12 -m venv .venv-gui
.\.venv-gui\Scripts\python.exe -m pip install -e ".[dev,build]"
.\run.ps1
```

После editable-установки изменения в `src/bdo_sim` подхватываются сразу.
`run.ps1` и `build.ps1` принимают `-Python` с путём к другому интерпретатору.
Для обычной установки используйте `pip install .`; точка запуска — `python -m bdo_sim`.

## Слои

| Модуль | Ответственность |
| --- | --- |
| `domain.py` | Независимые от Qt сущности Item, Chest и три механики открытия |
| `definitions.py` | Декларативные наследники, Loot, Stage, проверка и регистрация классов |
| `content/` | Конкретные предметы и сундуки с английскими ID |
| `catalog.py` | Создание экземпляров, проверка ссылок и ресурсов |
| `engine.py` | Очередь, отдельный RNG, Opening и Report |
| `outcomes.py`, `rarity.py` | Вероятности для отображения, редкость, сортировка каталога |
| `storage.py` | Транзакционная история SQLite |
| `i18n.py` | Язык и словари интерфейса |
| `ui/` | Qt-окна, темы, анимации, общий Audio-сервис |
| `app.py` | Создание зависимостей и запуск приложения |

`Chest.open(rng)` полиморфный. Движок проверяет тип награды только для постановки
вложенного сундука в очередь. Симуляция хранит счётчики, а не полный журнал событий.
Быстрый режим работает короткими пакетами между событиями Qt.

Seed принадлежит симуляции. Анимации, звук и темы не меняют RNG.
Одинаковые каталог, корзина и seed дают одинаковый результат. После изменения таблиц
результат для прежнего seed может измениться.

## Проверки

```powershell
.\.venv-gui\Scripts\python.exe -m ruff check src tests scripts
.\.venv-gui\Scripts\python.exe -m ruff format --check src tests scripts
.\.venv-gui\Scripts\python.exe -m unittest discover -s tests -v
$env:QT_QPA_PLATFORM = 'offscreen'
.\.venv-gui\Scripts\python.exe tests/gui_smoke.py
.\.venv-gui\Scripts\python.exe -m bdo_sim --smoke-test
```

Для проверки окон через системный backend задайте `QT_QPA_PLATFORM=windows`.
31 тест проверяет ядро, регистрацию, UI, локализацию, результаты и звук. Сравнение
с прототипом использует 54 независимых контрольных результата в `tests/fixtures`.
См. [описание эталона](../tests/fixtures/README.md).

`tests/gui_smoke.py` проходит корзину, поиск, анимацию, пропуск, отмену, отчёт,
CSV, историю и темы. Служебные снимки сохраняются в игнорируемую `.test-output/`.

## Скриншоты README

```powershell
.\.venv-gui\Scripts\python.exe scripts/screenshots.py
```

Сценарий создаёт отдельные временные настройки и SQLite-базу. Личная статистика
не изменяется. Сохраняются четыре PNG в `docs/screenshots/`, с фиксированными seed.

## Windows-сборка

```powershell
.\build.ps1 -Builder pyinstaller
.\build.ps1 -Builder pyinstaller -OutputName BDOChestStudio-dev -Incremental
.\build.ps1 -Builder nuitka
```

PyInstaller использует `scripts/BDOChestStudio.spec`, Nuitka — `src/launcher.py`.
Оба включают `src/bdo_sim/assets`, LICENSE и THIRD_PARTY_NOTICES. Выход — `dist/`.
Для Nuitka нужен C/C++ toolchain. Скорость конкретной сборки нужно измерять;
сам факт компиляции не гарантирует ускорения. PyInstaller onefile распаковывает
зависимости во временную папку при старте.

Скрипт временно очищает PATH от сторонних Qt/ICU DLL. Spec исключает системные
ICU/UCRT/API-set DLL, которые должны предоставляться Windows.

Workflow `Checks` проверяет код при push/PR. `Windows build` запускается вручную
и создаёт ZIP-артефакт, без автоматической публикации Release. При распространении
учитывайте [лицензии зависимостей и игровых ресурсов](../THIRD_PARTY_NOTICES.md).

## Локальные данные

История: Qt `AppLocalDataLocation`, обычно
`%LOCALAPPDATA%/PetProjects/BDOChestStudio/history.sqlite3`.
Для тестового профиля задайте `BDO_SIM_DATA_DIR`. Настройки темы/языка/звука хранятся
отдельно через QSettings. Исходные ресурсы не изменяются приложением.
