 # Проект: Веб-сервис для фанатов вселенной Гарри Поттера
## Описание

Задача проекта — создать сервис для фанатов, где они смогут ознакомиться с различными героями, объектами и событиями из вселенной Гарри Поттера, а также визуализировать их взаимосвязи в виде графа.

Проект представляет собой веб-приложение, включающее:

- **Frontend** — клиентская часть на Vite + Vue 3
- **Backend** — API на Flask, обрабатывающее запросы и взаимодействующее с базой данных
- **Базу данных Neo4j** — для хранения сущностей и связей между ними

Все компоненты развертываются через Docker Compose.

---

## Требования

- ОС: Ubuntu 22.04 или новее
- Установленный Docker и Docker Compose

---

## Клонирование репозитория

```bash
git clone https://github.com/moevm/nosql1h25-hogwarts.git
cd nosql1h25-hogwarts
```

---

## Настройка переменных окружения

В корне проекта уже присутствует пример `.env` файла.
Отредактируйте файл `.env` в нужных местах.

---

## Сборка и запуск контейнеров

Выполните команды:

```bash
docker compose build --no-cache
docker compose up
```

Проект развернёт три сервиса:

| Сервис    | Назначение                  | URL                       |
|-----------|-----------------------------|---------------------------|
| frontend  | Клиентская часть (Vue 3)    | http://localhost:3000     |
| backend   | API-сервер (Flask)          | http://localhost:5000     |
| neo4j     | База данных + визуализация  | http://localhost:7474     |

> Интерфейс приложения для пользователей доступен по адресу: [http://localhost:3000](http://localhost:3000)
---

## Структура проекта

```
.
├── client/           # Исходный код frontend (Vite + Vue 3)
├── potter_api/       # Исходный код backend (Flask)
├── .env.example      # Пример файла переменных окружения
├── docker-compose.yml
└── README.md
```

---

## Остановка и очистка

Для остановки всех контейнеров:

```bash
docker compose down
```

Для удаления контейнеров, образов и томов:

```bash
docker compose down --volumes --rmi all
```

---


# nosql_template


## Предварительная проверка заданий

<a href=" ./../../../actions/workflows/1_helloworld.yml" >![1. Согласована и сформулирована тема курсовой]( ./../../actions/workflows/1_helloworld.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/2_usecase.yml" >![2. Usecase]( ./../../actions/workflows/2_usecase.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/3_data_model.yml" >![3. Модель данных]( ./../../actions/workflows/3_data_model.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/4_prototype_store_and_view.yml" >![4. Прототип хранение и представление]( ./../../actions/workflows/4_prototype_store_and_view.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/5_prototype_analysis.yml" >![5. Прототип анализ]( ./../../actions/workflows/5_prototype_analysis.yml/badge.svg)</a> 

<a href=" ./../../../actions/workflows/6_report.yml" >![6. Пояснительная записка]( ./../../actions/workflows/6_report.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/7_app_is_ready.yml" >![7. App is ready]( ./../../actions/workflows/7_app_is_ready.yml/badge.svg)</a>
