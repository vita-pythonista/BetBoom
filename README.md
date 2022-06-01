# TestAutoTest
Функционирующий инстанс доступен по адресу [ruapm.online](http://ruapm.online/).

Данный сервис предназначен для тестирования.
В рамках сервиса реализуется возможность регистрации и авторизании пользователя,
а так-же создание и удаление контактов (телефон и email) пользователя.

## Задача
Организовать автоматизированное тестирование позитивных тест-кейсов для **API** и **HTML Page**
данного сервиса.
Реализовать тесты для:
- API
    - Регистрация (можем зарегистрировать пользователя)
    - Авторизация (можем авторизовать пользователя)
    - Добавление контакта (можем добавить контакт пользователя)
    - Удаление контакта (можем удалить контакт пользователя)
- HTML Page
    - Проверка корректного отображения имени пользователя в `span .username`

Тестируем с использованием python3. Других ограничений нет.


## Подготовка и запуск
### Без Docker
Грузим зависимости
```bash
pip3 install -r requirements.txt
```

Находясь в `src` (`cd src`)
```bash
python -m aiohttp.web -H 0.0.0.0 -P 8080 application:create_application
```

### Docker
Собираем образ в корне проекта.
```bash
docker build . -t test-auto-test:1
```
Запускаем.
```bash
docker run -ti -p 8080:8080 test-auto-test:1
```

**P.S.**
В приведённом примере сервер слушает все интерфейсы на порту `8080`.

## HTML Page
Можно получить HTML страницу с данными о пользователе в рамках сессии.
Для этого достаточно открыть браузер и перейти по URL `http://localhost:8080/session/{ssid}`, 
где `ssid` - идентификатор сессии. `ssid` можно получить средствами API (смотри метод `/api/v1/user/login`).

## API
Варианты ответа API:

**Запрос успешено обработан**
```JSON
{
  "success": true,
  "result": ...
}
```

**При обработке запроса возникла ошибка**
```JSON
{
  "success": false,
  "error": "Some error details"
}
```


### Регистрация
> **POST** /api/v1/user/registration

#### Параметры запроса:  
**[headers]**  
**-**   

**[path]**  
**-**   

**[body]**
- `user` - данные пользователя
- `user.login` - логин
- `user.password` - пароль


#### Параметры ответа
**[body]**
- `success` - успешность обработки запроса
- `result` - объект с результатом запроса
- `result.user` - данные созданного пользователя
- `result.user.login` - логин пользователя
- `result.user.contacts` - список контактов пользователя
- `result.user.contacts[].id` - идентификатор контакта
- `result.user.contacts[].type` - тип контакта
- `result.user.contacts[].content` - данные контакта (`phone` / `email`)

Запрос:
```bash
curl -XPOST http://localhost:8080/api/v1/user/registration -d '{"user": {"login": "username", "password": "******"}}'
```

Ответ:
```JSON
{
  "success": true,
  "result": {
    "user": {
      "login": "username",
      "contacts": []
    }
  }
}
```
 
 
 
 
 
 
### Авторизация
> **POST** /api/v1/user/login

#### Параметры запроса:  
**[headers]**  
**-**   

**[path]**  
**-**   

**[body]**
- `user` - данные пользователя
- `user.login` - логин
- `user.password` - пароль


#### Параметры ответа
- `success` - успешность обработки запроса
- `result` - объект с результатом запроса
- `result.ssid` - идентификатор созданной сессии. Используется для передачи в заголовке `ssid`
- `result.user` - данные созданного пользователя
- `result.user.login` - логин пользователя
- `result.user.contacts` - список контактов пользователя
- `result.user.contacts[].id` - идентификатор контакта
- `result.user.contacts[].type` - тип контакта
- `result.user.contacts[].content` - данные контакта (`phone` / `email`)


#### Пример
Запрос:
```bash
curl -XPOST http://localhost:8080/api/v1/user/login -d '{"user": {"login": "username", "password": "******"}}'
```

Ответ:
```JSON
{
  "success": true,
  "result": {
    "ssid": "fd2f6760-8388-4be3-8af7-bb3920180dfd",
    "user": {
      "login": "username",
      "contacts": []
    }
  }
}
```



### Получение данных пользователя
> **GET** /api/v1/user

#### Параметры запроса:  
**[headers]**
- `ssid` - идентификатор сессии, полученный в результате вызова `/api/v1/user/login`   

**[path]**  
**-**   

**[body]**  
**-**   


#### Параметры ответа
**[body]**
- `success` - успешность обработки запроса
- `result` - объект с результатом запроса
- `result.ssid` - идентификатор созданной сессии. Используется для передачи в заголовке `ssid`
- `result.user` - данные созданного пользователя
- `result.user.login` - логин пользователя
- `result.user.contacts` - список контактов пользователя
- `result.user.contacts[].id` - идентификатор контакта
- `result.user.contacts[].type` - тип контакта (`phone`, `email`)
- `result.user.contacts[].content` - данные контакта 


#### Пример

Запрос:
```bash
curl -XGET http://localhost:8080/api/v1/user -H 'ssid: 0c9298d7-6f97-4e73-9ad2-6d5a5b5a1503'
```

Ответ:
```JSON
{
  "success": true,
  "result": {
    "user": {
      "login": "username",
      "contacts": [
        {
          "id": 2,
          "type": "phone",
          "content": "+000"
        },
        {
          "id": 5,
          "type": "phone",
          "content": "+100"
        }
      ]
    }
  }
}
```

### Добавить контакт пользователя
> **POST** /api/v1/user/contact

#### Параметры запроса:  
**[headers]**
- `ssid` - идентификатор сессии, полученный в результате вызова `/api/v1/user/login`   

**[path]**  
**-**   

**[body]**  
- `contact` - данные создаваемого контакта
- `contact.type` - тип создаваемого контакта (`phone`, `email`)
- `contact.content` - данные контакта

#### Параметры ответа
**[body]**
- `success` - успешность обработки запроса
- `result` - объект с результатом запроса
- `result.ssid` - идентификатор созданной сессии. Используется для передачи в заголовке `ssid`
- `result.user` - данные созданного пользователя
- `result.user.login` - логин пользователя
- `result.user.contacts` - список контактов пользователя
- `result.user.contacts[].id` - идентификатор контакта
- `result.user.contacts[].type` - тип контакта (`phone`, `email`)
- `result.user.contacts[].content` - данные контакта 

#### Пример

Запрос:
```bash
curl -XPOST http://localhost:8080/api/v1/user/contact -H 'ssid: d03f3a3f-e778-4e43-b23d-c579274a4c48' -d '{
  "contact": {
      "type": "phone",
      "content": "+79990001122"
  }
}'
```

Ответ:
```JSON
{
  "success": true,
  "result": {
    "user": {
      "login": "username",
      "contacts": [
        {
          "id": 2,
          "type": "phone",
          "content": "+000"
        },
        {
          "id": 5,
          "type": "phone",
          "content": "+100"
        },
        {
          "id": 6,
          "type": "phone",
          "content": "+79990001122"
        }
      ]
    }
  }
}
```


### Удалить контакт пользователя
> **POST** /api/v1/user/contact/{id}

#### Параметры запроса:  
**[headers]**
- `ssid` - идентификатор сессии, полученный в результате вызова `/api/v1/user/login`   

**[path]**  
- `id` - идентификатор контакта к удалению 

**[body]**  
**-**   


#### Параметры ответа
**[body]**
- `success` - успешность обработки запроса
- `result` - объект с результатом запроса
- `result.ssid` - идентификатор созданной сессии. Используется для передачи в заголовке `ssid`
- `result.user` - данные созданного пользователя
- `result.user.login` - логин пользователя
- `result.user.contacts` - список контактов пользователя
- `result.user.contacts[].id` - идентификатор контакта
- `result.user.contacts[].type` - тип контакта (`phone`, `email`)
- `result.user.contacts[].content` - данные контакта 


#### Пример

Запрос:
```bash
curl -XDELETE http://localhost:8080/api/v1/user/contact/2 -H 'ssid: 9d60dbb2-92ae-407c-80fb-91ebbbf8c1c9'
```

Ответ:
```JSON
{
  "success": true,
  "result": {
    "user": {
      "login": "username",
      "contacts": [
        {
          "id": 5,
          "type": "phone",
          "content": "+100"
        },
        {
          "id": 6,
          "type": "phone",
          "content": "+79990001122"
        }
      ]
    }
  }
}
```

