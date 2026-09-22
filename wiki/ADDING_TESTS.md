# Добавление новых тестов

## Расположение тестов

- Smoke тесты лежат в директории `agent/tests/smoke`;
- В этой директории создаётся файл с названием `test_<название_пакета>.py`;
- Используемые в тестах доп. файлы хранятся в директории `agent/tests/smoke/test_files`.

### Пример

Расположение теста для icu-dev: `agent/tests/smoke/test_icu_dev.py`;
Расположение доп. файла для теста: `agent/tests/smoke/test_files/test_icu_dev.cpp`.

## Организация теста

- Для пакета в указанном выше файле создаётся класс с названием `Test<НазваниеПакета>`
- Класс помечается следующими декораторами:
    * `@allure.suite('<название-пакета> tests')`
    * `@pytest.mark.smoke`
    * `@pytest.mark.<название_пакета>`

### Пример

Для теста icu-dev будет создан класс со следующими декораторами:

```Python
@allure.suite('icu-dev tests')
@pytest.mark.smoke
@pytest.mark.icu_dev
class TestIcuDev:
    '''icu-dev smoke test class'''
```

## Тесткейсы

- Тесткейсы описываются в методах данного класса
- Сигнатура метода тесткейса: `def test_<название_пакета>_<содержание_теста>(self, ssh_client: SshClient)`
- Каждый тесткейс помечается декоратором `@allure.title('<название-пакета>: описание теста')`:
```Python
@allure.title('icu-dev: compile and run test')
def test_icu_dev(self, ssh_client: SshClient):
    '''Test that ICU header files are installed'''
```
- В тесткейсах необходимо писать типы аргументов метода, но не следует писать тип возвращаемого значения, кроме фикстур (см. Кодстайл).
- В тесткейсах необходимо придерживаться правила одного ассерта (см. ниже).
- Рекомендуется использование готовых фикстур, описанных в `conftest.py`. В частности, фикстура `remote_tmp_path` должна использоваться в тестах, создающих на удаленной машине файлы, для их последующей автоматической очистки. Также в `conftest.py` есть фикстуры для пропуска тестов при отсутствии необходимых пакетов (g++, gcc и т.д.)
- Для тестов на ELF-файлы и статические библиотеки рекомендовано использование функций из `helpers.py`: `check_elf_file` и `check_static_lib`. При необходимости можно добавлять новые функции-хелперы.

## Виды тесткейсов

### 1. Минимальные
    - Используют только утилиты из минимального образа и сам пакет
    - Проверяют базовую функциональность или базовые признаки установки пакета
    - Не требуют компиляторов и сторонних пакетов
    - Помечаются меткой `@pytest.mark.minimal`

### 2. Полные
    - Проверяют основные сценарии использования пакета
    - Могут использовать сторонние утилиты и компиляторы

- Для каждого пакета необходимо сделать хотя бы один минимальный тесткейс
- Если пакет для своей стандартной работы требует сторонних пакетов, компилятора и др., необходимо сделать оба вида тесткейсов
### Пример

Для пакета `icu-dev`, требующего для своей стандартной рабоыт компилятор g++, создаются следующие тесты:
```Python
@allure.title('icu-dev: development headers test')
@pytest.mark.minimal        # маркировка минимального теста
def test_icu_headers(self, ssh_client: SshClient):
    '''Test that ICU header files are installed'''
    # Использует стандартный stat для проверки наличия файлов

@allure.title('icu-dev: compile and run test')
def test_icu_dev(self, ssh_client: SshClient):
    '''Test icu development headers and libraries'''
    # Использует компилятор g++
```

### Пример организации теста

- На примере  icu-dev.
- Расположение тестов: `agent/tests/smoke/test_icu_dev.py`
- Структура теста:
```Python
@allure.suite('icu-dev tests')
@pytest.mark.smoke
@pytest.mark.icu_dev
class TestIcuDev:
    '''icu-dev smoke test class'''

    @allure.title('icu-dev: development headers test')
    @pytest.mark.minimal 
    def test_icu_headers(self, ssh_client: SshClient):
        '''Test that ICU header files are installed'''
        with allure.step('Checking unicode headers directory'):
            # Some actions

    @allure.title('icu-dev: compile and run test')
    def test_icu_dev(self, ssh_client: SshClient):
        '''Test icu development headers and libraries'''
        # preparation
        with allure.step('Compiling program using icu'):
            # Step 1
        with allure.step('Running program using isu'):
            # Step 2

```

## Выбор тестов по метке

- Для запуска всех smoke тестов указывается `PACKAGES_RAW=smoke` (или В PACKAGES_FILE)
- Для запуска только минимальных тестов указывается `PACKAGES_RAW=minimal`

## Правило одного ассерта

- При использовании assert в каждом тесткейсе должен быть ровно 1 assert.
- По возможности следует разбивать один тест с несколькими ассертами на несколько тестов с одним ассертом.
- При необходимости выполнить больше проверок в одном тесте следует использовать soft assertions. Например, из pytest-check [https://pypi.org/project/pytest-check/].

### Плохо:
```
assert cmd.rc == 0, 'Error'
assert 'GOOD' in cmd.stdout, 'Unexpected output' 
```
### Хорошо:
```Хорошо:
import pytest_check as check
check.equal(cmd.rc, 0, 'Error')
check.is_in('GOOD', cmd.stdout, 'Unexpected output')
```

## Кодстайл

- В проверках необходимо прописывать assert message (`assert cmd.rc == 0, 'ASSERT MESSAGE'`).
- Большое содержимое файлов (коды программ, настройки) рекомендуется выносить в отдельные файлы в директории `agent/tests/smoke/test_files` и загружать их на удаленную машину при помощи `ssh_client.put_file`.
- В тесткейсах необходимо указывать типы аргументов метода, но не следует писать тип возвращаемого значения. 
- В фикстурах необходимо указывать типы аргументов фикстуры и тип возвращаемого значения.
- Необходимо использование одинарных кавычек везде, кроме строк, содержащих одинарные кавычки (в данном случае лучше избежать экранирования). [https://peps.python.org/pep-0008/#string-quotes]
- Перед коммитом требуется пройтись по коду линтером (файл с настройками лежит на вики: `.pylintrc`) и выполнить автоформатирование кода (для VS Code: Ctrl + Shift + i)

## Примечания

- Все создаваемые метки необходимо описывать в `agent/tests/pytest.ini` в формате: `<метка>: <описание метки>`. Содержимое файла следует поддерживать в алфавитном порядке.
- Логические этапы внутри тесткейса рекомендуется оборачивать через `allure.step('<Описание действий теста>')`. Рекомендуется для каждого тесткейса описывать хотя бы один этап (для лучшего отображения в отчёте Allure)
- Подробнее о доступных в минимальном образе утилитах: [https://ru.wikipedia.org/wiki/BusyBox]