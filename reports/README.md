# Отчеты о тестировании

В этой директории расположены отчеты о тестировании пакетов в виде скриншотов и файлов.

## Как запускать allure-отчеты

- Установить в .env переменную `HOST_REPORT_PATH` на директорию с нужным отчетом. Например, `HOST_REPORT_PATH=./reports/main`
- Запустить allure-container:

```bash
docker compose up -d --build --force-recreate --no-deps allure
```

## Список отчетов

- main: Основной отчет с большинством пакетов,
- clang: Отчёт для пакетов clang-dev и clang-format,
- diff-pckgs: Отчёт для некоторых специфичных пакетов, которые конфликтуют с утилитами в стандартном образе,
- mini: Отчёт для некоторых пакетов (в основном go), которые нельзя протестировать в стандартном образе.

## Информация о тестах

Все тесты успешно прошли на тестовых образах, кроме тестов на следующие пакеты:

### main

| Пакет | Статус | Проблема |
| ----- | ------ | -------- |
| curl-staticdev | Failed 1/2 | Проблема с зависимостями (glibc, undefined reference) при статической линковке библиотеки `libcurl.a`. |
| e2fsprogs | Failed 4/23 | Ошибка утилиты `chattr`: `Operation not supported while setting flags`; бинарный файл `resize2fs` не найден в образе; вывод утилиты `lsattr` не проходит проверку (должен начинаться со строки `--------------e-------`). |
| fault-injection-staticdev | Missing | Нет информации о пакете в интернете |
| fmt-dev | Failed 1/4 | Статическая библиотека `libfmt.a` не найдена. Возможна проблема установки в образ. |
| fmt-staticdev | Failed 1/3 | Статическая библиотека `libfmt.a` не найдена. Возможна проблема установки в образ. |
| krb5 | Failed 5/5 | Не ясен точный состав пакета что необходимо протестировать. Пакет разбит на подпакеты, в которых сосредоточена основная функциональность, но они не установлены в образе и не числятся в списке для тестирования. Без установки подпакетов тестировать де-факто нечего. |
| libcrp-staticdev | Failed 1/1 | Не найдена статическая библиотека `libcrp.a`. Возможна проблема установки в образ. |
| libgcc-dev | Failed 1/1 | Динамическая библиотека не соответствует ELF-формату (Сигнатура не удовлетворяет '177 E L F'). |
| liburcu-staticdev | Failed 2/2 | Не найдена статическая библиотека `liburcu*.a`. Возможна проблема установки в образ. |
| libxcrypt-dev | Missing | Тесты не реализованы (в файле test_libxcrypt_dev.py тесты не на пакет libxcrypt-dev) |
| lmdb | Missing | Тесты не реализованы: не ясно, является ли этот пакет алиасом на lmdb-dev и различается ли их содержимое. |
| lvm2-dev | Failed 1/3 | Неожиданный вывод работы программы: функция `dm_get_library_version` не завершается успешно. |
| ncurses-staticdev | Failed 1/3 | Не найдена статическая библиотека `libncurses.a`. Возможна проблема установки в образ. |
| ncurses-tools | Failed 8/23 | Не проходят тесты на ряд утилит по различным причинам: clear, infocmp: `TERM environment variable not set.`; infotocap: `"/tmp/run-test/t/test-terminal": This is not a text-file`; man: `man: can't resolve man7/groff_man.7 No manual entry for man`; share: utility not found; reset, tset: `terminal attributes: No such device or address`; tput: `No value for $TERM and no -T specified` |
| nettle-dev | Failed 1/4 | Не найдена статическая библиотека `libnettle.a`. Возможна проблема установки в образ. |
| ntp | Failed 2/2 | Не найдены утилита ntpq. Возможна проблема установки в образ. |
| numactl-dev | Failed 1/3 | Неожиданный вывод программы: функция `numa_available` возвращает false. |
| numactl-staticdev | Failed 1/3 | Неожиданный вывод программы: функция `numa_available` возвращает false. |
| openldap-staticdev | Failed 1/3 | Проблема с зависимостями (glibc, undefined reference) при статической линковке библиотеки `libldap.a`. |
| rdma-core | Failed 2/7 | Не проходит ряд проверок: rdma: `Failed to open NETLINK_RDMA socket`; ibv_devices: `Failed to get IB devices list`. |
| rng-tools | Missing | Не реализован в связи с проблемой тестирования: выполняется бесконечно долго. |
| snappy-dev | Failed 1/3 | Не найдена динамическая библиотека `libsnappy.so`. Возможна проблема установки в образ. |
| systemtap-dev | Failed 5/5 | Не найдены файлы пакета (проблема с установкой в образ). |
| util-linux-libuuid-staticdev | Failed 2/3 | Не найдена статическая библиотека `libuuid.a`. Возможна проблема установки в образ. |
| vim-common | Failed 2/3 | Отсутствует утилита xxd. Возможна проблема установки в образ. |
| vim-vimrc | Failed 1/1 | Отсутствует содержимое пакета. Проблема с установкой в образ. |
| xmlstarlet | Failed 2/2 | Отсутствует содержимое пакета. Проблема с установкой в образ |

Пакеты nodejs и nodejs-npm тестировались в контейнере.

### clang

| Пакет | Статус | Проблема |
| ----- | ------ | -------- |
| clang-dev | Failed 2/3 | Не найдены заголовки и библиотеки. Возможна проблема установки пакета в образ. |

### mini

| Пакет | Статус | Проблема |
| ----- | ------ | -------- |
| systemd-rpm-macros | Broken 1/1 | Не найден дополнительный файл для тестирования |

### Решено не тестировать

Список пакетов, которые было решено не тестировать:

| Пакет | Проблема |
| ----- | -------- |
| base-config | Не ставится в образ; нет точной информации о составе пакета; считается устаревшим |
| expected-lite-dev | Принято решение не тестировать, причина не известна. |
| libpam-dev | Отсутствует dev-версия пакета libpam, пакет может предоставлять неполную функциональность. |
| libpfm4-dev | Отсутствует dev-версия пакета libpfm4, пакет может предоставлять неполную функциональность. |
| libtatlin-raid | Нет информации о пакете в интернете. |
| libtraidnl* | Нет информации о пакете в интернете. |
| libtraidnl-devel | Нет информации о пакете в интернете. |
| libtraidnl-devel-static | Нет информации о пакете в интернете. |
| optional-lite-dev | Отсутствует dev-версия пакета optional-lite, пакет может предоставлять неполную функциональность. |
| perl-module* | Отсутствует в официальном образе Yocto и в кастомном слое коллег. |
| range-v3-dev | Отсутствует dev-версия пакета range-v3, пакет может предоставлять неполную функциональность. |
| string-view-lite-dev | Отсутствует dev-версия пакета string-view-lite, пакет может предоставлять неполную функциональность. |
| tcpc-staticdev | Нет информации о пакете в интернете. |
| urio | Нет информации о пакете в интернете. |
| variant-lite-dev | Отсутствует dev-версия пакета variant-lite, пакет может предоставлять неполную функциональность. |
| storcli | Тесты не реализованы, так как протестировать функциональность пакета в Yocto невозможно: пакет, ориентированный на оборудование. |
| QConvergeConsoleCLI | Тесты не реализованы, так как протестировать функциональность пакета в Yocto невозможно: пакет, ориентированный на оборудование. |
| di-dev | Отсутствует в официальных слоях Yocto. |

## Статистика

- Всего пакетов: 309
- Решено не тестировать: 18 (5.8%)
- Сделано: 287 (92.8%)
- Failed пакетов: 26 (8.4%)
- Из них failed из-за возможных проблем с установкой в образ: 15 (4.8%)

## Приложение

Списки утилит, для которых собраны образы **clang**, **diff-pckgs**, **mini**:

- **clang**: clang-dev, clang-14-format;
- **diff-pckgs**: di-dev, hat-trie-dev, libgssglue-dev, rxvt-unicode-terminfo, storcli, QConvergeConsoleCLI;
- **mini**: dnf-plugins-core, dwz, dracut, go2xunit, gocov, gocov-xml, go-junit-report, go-pkger, goyacc, protoc-gen-go, mstflint, systemd-analyze, systemd-dev, systemd-rpm-macros.

### Документ с проблемными пакетами

<https://docs.google.com/document/d/1mVtquA02BGwyz65umSiFOw-8K3X4cm0YVI3HFgFnNc8/edit?usp=sharing>
