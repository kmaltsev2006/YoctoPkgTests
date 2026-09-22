# yocto-pkg-tests
Project contains scripts and environment for linux packages smoke testing

> [!IMPORTANT]
> Готовые отчеты работы системы в виде скриншотов и json-файлов для allure находятся в директории [./reports](./reports). 


## Быстрый запуск (MODE: RUN)

Копирование содержимого .env.example в .env и создание директорий для volume:
```bash
cp .env.example .env
mkdir -p ./volume ./volume/bblayers ./volume/built-images ./volume/conf ./volume/log ./volume/poky ./volume/reports
```

Поместите тестируемый образ в `./volume/built-images`   
*Образ должен иметь имя `IMAGE_NAME` (см. в .env)*  
Запуск:
```bash
docker compose up -d --build
```

Просмотр отчёта тестирования: *http://localhost:8080/*

## ⚠️ Внимание
Из-за медленного запуска QEMU контейнеры могут стартовать некорректно, что приводит к следующей ошибке health_check:
```bash
 ✔ agent                            Built                               0.0s 
 ✔ allure                           Built                               0.0s 
 ✔ yp-target                        Built                               0.0s 
 ✔ Network yocto-pkg-tests_default  Created                             0.1s 
 ✘ Container yp-target-container    Error                              11.1s 
 ✔ Container agent-container        Created                             0.1s 
 ✔ Container allure-container       Created                             0.1s 
dependency failed to start: container yp-target-container is unhealthy
```

Чтобы исправить это, рекомендуется запускать контейнеры по одному, дожидаясь healthy статуса yp-target:
```bash
docker compose up -d --build yp-target
# wait for healthy status of yp-target-container...
docker compose up -d --build agent allure
```

## .env
| Переменная                   | Описание |
| ---------------------------- | --- |
| `HOST_LOG_PATH`              | Путь к директории логирования |
| `HOST_POKY_PATH`             | Путь к директории poky |
| `HOST_IMAGE_PATH`            | Путь к директории с образами |
| `HOST_CONF_PATH`             | Путь к директории с файлами конфигурации сборки |
| `HOST_BBLAYERS_PATH`         | Путь к директории с bblayers |
| `YOCTO_RELEASE_BRANCH_NAME`  | Используемый релиз yocto |
| `SSH_TARGET_USER`            | Пользователь для SSH подключения в контейнер |
| `SSH_TARGET_PASSWORD`        | Пароль для SSH_TARGET_USER |
| `SSH_TARGET_PORT`            | Порт на хосте для подключения к контейнеру по SSH |
| `SSH_QEMU_PORT`              | Порт на хосте для подключения к QEMU по SSH |
| `SSH_QEMU_INTERNAL_PORT`     | Порт в контейнере для подключения к QEMU по SSH |
| `MODE`                       | Режим запуска (BUILD\|RUN\|IDLE) |
| `IMAGE_NAME`                 | Имя запускаемого образа (устанавливается только для MODE=RUN) |
| `HOST_REPORT_PATH`           | Путь к директории отчётов |
| `HOST_TEST_PATH`             | Путь к директории с тестами |
| `REPORT_FORMAT`              | Формат отчета (txt\|allure, default: txt) |
| `PACKAGES_RAW`               | Список тестируемых пакетов через запятую, точку с запятой или пробел |
| `PACKAGES_FILE`              | Путь к файлу с описанием тестируемых пакетов (для использования нужно раскомментировать volume в docker-compose.yml) |
| `ALLURE_PORT`                | Порт для доступа к Allure отчетам |


## Режимы запуска (MODE)
- BUILD - собирает образ, копируя его в `/var/yocto/built-images` контейнера с суффиксом в виде текущего UNIX времени и запускает его
- RUN - запускает образ по переданному `IMAGE_NAME`
- IDLE - ничего не делает (режим для отладки)

## Дополнительно:
*Все значения для команд взяты из .env.example*

Подключение к yp-target-container по SSH:
```bash
ssh ypdev@localhost -p 2222
```

Подключение к QEMU по SSH с хоста:
```bash
ssh root@localhost -p 3333
```

Подкючение к QEMU по SSH в контейнере:
```bash
ssh root@localhost -p 3333
```

Сборка образа вручную внутри yp-target-container (должно запускаться **не** от root-пользователя):
```bash
./build.sh
```

Запуск образа:
```bash
./runqemu.sh -i image_name # in the foreground
```
```bash
./runqemu.sh -i image_name -d # in the background
```

Коды выхода agent:  
| Код | Значение                                                                           |
| --- | ---------------------------------------------------------------------------------- |
| 0   | Все тесты прошли успешно                                                           |
| 1   | Ошибка обязательных переменных окружения или неверный формат/порт                  |
| 2   | Ошибка инфраструктуры: нет директории для тестов или не удалось соединиться по SSH |

Особенность allure:  
При использовании режима txt для агента allure будет отображать пустой allure отчет.
