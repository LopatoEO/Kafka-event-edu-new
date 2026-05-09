# Kafka-Event-Edu

## Описание

Kafka-Event-edu - система для обработки и аналитики событий в реальном времени. Система построена на базе брокера сообщений Apache Kafka для потоковой обработки данных и СУБД ClickHouse для распределенного хранения данных. Проект демонстрирует архитектуру микросервисов с использованием Docker для контейнеризации.

## Архитектура

Система состоит из следующих компонентов:

- **Apache Kafka** (3 брокера): Распределенная платформа для потоковой обработки данных
- **ClickHouse** (4 узла): Колонно-ориентированная СУБД для аналитики
- **Zookeeper**: Координационный сервис для Kafka
- **Event Producer**: REST API для отправки событий в Kafka
- **Consumer**: Сервис для чтения событий из Kafka и записи в ClickHouse
- **Analytic Service**: REST API для выполнения аналитических запросов к ClickHouse
- **Nginx**: Реверс-прокси для маршрутизации запросов

## Компоненты

### Event Producer

FastAPI приложение, предоставляющее REST API для отправки событий в Kafka.

### Consumer

Сервис на Python, который:

- Читает сообщения из Kafka топика "events"
- Обрабатывает события с помощью диспетчера
- Пакетно записывает данные в ClickHouse

### Analytic Service

FastAPI приложение для аналитических запросов:

- Выполнение SQL запросов к ClickHouse
- Получение статистики по событиям
- REST API для внешних клиентов

### Инфраструктура

- **Kafka кластер**: 3 брокера с KRaft режимом (без Zookeeper для координации)
- **ClickHouse кластер**: 4 узла с репликацией
- **Nginx**: Проксирование

## Установка и запуск

### Предварительные требования

- Docker и Docker Compose
- Git

### Клонирование репозитория

```bash
git clone <repository-url>
cd Kafka-event-edu-new
```

### Запуск системы

```bash
docker-compose up -d
```

### Проверка работы

Через FastAPI сваггер

- Event Producer API: http://localhost/event-producer/docs
- Analytic Service API: http://localhost/analitic/docs

## API Документация

### Event Producer API

#### Отправка события

```http
POST /event-producer/
Content-Type: application/json

{
  "event": "created",
  "data": {
    "id": "123",
    "name": "example",
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

### Analytic Service API

#### Получение событий

```http
GET /analitic/v1/events
```

## Конфигурация

### Переменные окружения

#### Event Producer

- `KAFKA_BOOTSTRAP_SERVERS`: Адреса Kafka брокеров
- `ANALITICS_SERVICE_HOST`: Хост аналитического сервиса
- `ANALITICS_SERVICE_PORT`: Порт аналитического сервиса

#### Consumer

- `KAFKA_BOOTSTRAP_SERVERS`: Адреса Kafka брокеров
- `CLICKHOUSE_HOST`: Хост ClickHouse
- `CLICKHOUSE_PORT`: Порт ClickHouse

#### Analytic Service

- `KAFKA_BOOTSTRAP_SERVERS`: Адреса Kafka брокеров
- `CLICKHOUSE_HOST`: Хост ClickHouse
- `CLICKHOUSE_PORT`: Порт ClickHouse
- `BATCH_SIZE`: Размер пакета для записи

## **Схема данных

### ClickHouse таблицы

База данных: `kafka_events`

#### events_local (на каждом узле)

```sql
CREATE TABLE kafka_events.events_local (
  event_id UUID DEFAULT generateUUIDv4(),
  user_id UInt64,
  type String,
  value String,
  ts DateTime64(6)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(ts)
ORDER BY (ts, event_id)
SETTINGS index_granularity = 8192;
```

#### events (распределенная таблица)

```sql
CREATE TABLE kafka_events.events (
  event_id UUID DEFAULT generateUUIDv4(),
  user_id UInt64,
  type String,
  value String,
  ts DateTime64(6)
) ENGINE = Distributed('company_cluster', 'kafka_events', 'events_local', rand());
```

### Типы событий

- `created`: Создание объекта
- `updated`: Обновление объекта
- `deleted`: Удаление объекта</content>
  <parameter name="filePath">/Users/egor/fast/Kafka-event-edu-new/README.md
