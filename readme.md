# HTTP REST API сервер
HTTP сервер для предоставления информации по географическим объектам России. 
Источник данных: GeoNames.
## Описание сервера
Данный сервер предоставляет REST API, содержащий следующие методы:
1. Метод, возвращающий по id информацию о городе;
2. Метод, возвращающий список городов, исходя из параметров:
    - номер страницы;
    - количество городов на странице.
3. Метод, возвращающий информацию о двух городах, и отдельно то, какой город севернее, а так же определяющий разницу во времени и часовые зоны.
## Технологии
Данный HTTP сервер реализован на языке программирования *Python* в связке с модулем *socket*.

## Запуск сервера
```console
python script.py
```
После применения команды сервер запустится по адресу *127.0.0.1* на *8000* порту.

## Описание методов
Все методы возвращают результат либо в *text/html*, либо в *application/json* в зависимости от заголовка.
##### Метод, возвращающий информацию о городе по id:
Через *URL*:
```http
http://127.0.0.1:8000/cities/{номер}
```
Через запрос:
```http
GET /cities/{номер} HTTP/1.1
Host: {имя хоста}
Accept: {формат ответа}
```
Пример:
```http
GET /cities/470213 HTTP/1.1
Host: example.local
Accept: text/html
```
Результат:
```html
<html>
    <head>
    </head>
    <body>{'name': 'Vysokaya', 'asciiname': 'Vysokaya', 'alternatenames': 'Vysokaja,Vysokaya,Высокая', 'latitude': 60.32379, 'longitude': 40.6906, 'feature_class': 'P', 'feature_code': 'PPL', 'country_code': 'RU', 'cc2': '', 'admin1_code': '85', 'admin2_code': '', 'admin3_code': '', 'admin4_code': '', 'population': 0, 'elevation': '', 'dem': 180, 'timezone': 'Europe/Moscow', 'modification_date': '2012-01-17\n'}
    </body>
</html>
```
##### Метод, возвращающий список городов по параметрам номера страницы и количества элементов
Через *URL*:
```http
http://127.0.0.1:8000/citylist?page={номер страницы}&number={количество отображаемых элементов}
```
Через запрос:
```http
GET /citylist?page={номер страницы}&number={количество элементов} HTTP/1.1
Host: {имя хоста}
Accept: {формат ответа} 
```
###### Пример 1
Запрос:
```http
GET /citylist?page=10&number=2 HTTP/1.1
Host: example.local
Accept: application/json
```
Результат:
```json
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 808

{"number": 2, "page": 10, "cities": [{"name": "Yegor\u2019ye", "asciiname": "Yegor'ye", "alternatenames": "", "latitude": 57.02174, "longitude": 34.29403, "feature_class": "P", "feature_code": "PPL", "country_code": "RU", "cc2": "", "admin1_code": "77", "admin2_code": "", "admin3_code": "", "admin4_code": "", "population": 0, "elevation": "", "dem": 268, "timezone": "Europe/Moscow", "modification_date": "2011-07-09\n"}, {"name": "Yefremovo", "asciiname": "Yefremovo", "alternatenames": "", "latitude": 57.06001, "longitude": 34.74787, "feature_class": "P", "feature_code": "PPL", "country_code": "RU", "cc2": "", "admin1_code": "77", "admin2_code": "", "admin3_code": "", "admin4_code": "", "population": 0, "elevation": "", "dem": 188, "timezone": "Europe/Moscow", "modification_date": "2011-07-09\n"}]}
```
###### Пример 2
Запрос:
```url
http://127.0.0.1:8000/citylist?page=300&number=3
```
Результат:
```html
<html>
<head>
</head>
<body>
    <ol>
        <li>
        {'name': 'Lyubinka', 'asciiname': 'Lyubinka', 'alternatenames': 'Ljubinka,Lyubinka,Любинка', 'latitude': 57.49262, 'longitude': 34.84387, 'feature_class': 'H', 'feature_code': 'STM', 'country_code': 'RU', 'cc2': '', 'admin1_code': '77', 'admin2_code': '', 'admin3_code': '', 'admin4_code': '', 'population': 0, 'elevation': '', 'dem': 158, 'timezone': 'Europe/Moscow', 'modification_date': '2012-01-16\n'}
        </li>
        <li>
        {'name': 'Petrilovka', 'asciiname': 'Petrilovka', 'alternatenames': 'Petrilovka,Петриловка', 'latitude': 57.48945, 'longitude': 34.29631, 'feature_class': 'H', 'feature_code': 'STM', 'country_code': 'RU', 'cc2': '', 'admin1_code': '77', 'admin2_code': '', 'admin3_code': '', 'admin4_code': '', 'population': 0, 'elevation': '', 'dem': 172, 'timezone': 'Europe/Moscow', 'modification_date': '2012-01-16\n'}
        </li>
        <li>
        {'name': 'Krasnoarmeyets', 'asciiname': 'Krasnoarmeyets', 'alternatenames': 'Krasnoarmeec,Krasnoarmeyets,Красноармеец', 'latitude': 57.48173, 'longitude': 34.89405, 'feature_class': 'P', 'feature_code': 'PPL', 'country_code': 'RU', 'cc2': '', 'admin1_code': '77', 'admin2_code': '', 'admin3_code': '', 'admin4_code': '', 'population': 0, 'elevation': '', 'dem': 171, 'timezone': 'Europe/Moscow', 'modification_date': '2012-01-16\n'}
        </li>
    </ol>
</body>
</html>
```
##### Метод, получающий информацию о двух городах
На вход методу подаются города на русском языке. Поиск совпадений происходит в альтернативных именах, а так же с применением транслитерации к переданным значениям, на случай того, что список альтернативных имен - пустой.

Через *URL*:
```url
http://127.0.0.1:8000/citycompare?city1={город 1}&city2={город 2}
```

###### Пример
Запрос:
```url
http://127.0.0.1:8000/citycompare?city1=Краснодар&city2=Москва
```
Результат:
```html
<html>
    <head>
    </head>
    <body>
        <p>Город Краснодар: {'name': 'Krasnodar', 'asciiname': 'Krasnodar', 'alternatenames': 'Ekaterinodar,KRR,Krasnodar,Krasnodara,Novorosyisk,Yekaterinodar,ke la si nuo da er,keulaseunodaleu,kurasunodaru,qrsnwdr,Краснодар,קרסנודר,クラスノダル,克拉斯诺达尔,크라스노다르', 'latitude': 45.04484, 'longitude': 38.97603, 'feature_class': 'P', 'feature_code': 'PPLA', 'country_code': 'RU', 'cc2': '', 'admin1_code': '38', 'admin2_code': '', 'admin3_code': '', 'admin4_code': '', 'population': 649851, 'elevation': '', 'dem': 28, 'timezone': 'Europe/Moscow', 'modification_date': '2019-02-27\n'}
        </p>
        <p>Город Москва: {'name': 'Moskva', 'asciiname': 'Moskva', 'alternatenames': 'Maskva,Moscou,Moscow,Moscu,Moscú,Moskau,Moskou,Moskovu,Moskva,Məskeu,Москва,Мәскеу', 'latitude': 55.76167, 'longitude': 37.60667, 'feature_class': 'A', 'feature_code': 'ADM1', 'country_code': 'RU', 'cc2': '', 'admin1_code': '48', 'admin2_code': '', 'admin3_code': '', 'admin4_code': '', 'population': 11503501, 'elevation': '', 'dem': 161, 'timezone': 'Europe/Moscow', 'modification_date': '2020-03-31\n'}</p>
        <p>Севернее находится город: Москва</p>
        <p>Временная зона: Одинаковая</p>
        <p>Разница во времени: -0.09129066666666663</p>
    </body>
</html>
```


