# HTTPie Cheat Sheet
> a collection of HTTPie commands


## Query Parameters

### Query Parameter: Regular request

```bash
$ http get localhost:5000/items/ q=="one"
```

### Query Parameter: Parameter list

```bash
$ http get localhost:5000/items/ q=="one" q=="two"
```

### Query Parameter: empty parameter

```bash
# q is empty, but sent as a query parameter
$ http get localhost:5000/items/ q==
```

## Request Body

### Request Body: fields with single types

```bash
http POST localhost:5000/items/ name=iPhone price=999 desc="Newest iPhone"
```
### Request body: nested objects with arrays

```bash
$ http post :5000/items/1 user[username]="jason" user[full_name]="Jason Isaacs" \
item[name]="foo" item[description]="bar" item[price]=1.23 item[tax]=3.21 item[tags][]="baz" item[tags][]="foobar"
```

Note the syntax `item[tags][]` to JSON arrays.


### Request body: nested objects with arrays of objects

```bash
$ http put :5000/v4/items/1 name="foo" price=2.31 tags[]="foo" tags[]="bar" tags[]="baz" tags[]="foo" images[0][url]=http://example.com/pic1.png images[0][name]="foobar1" images[1][url]=http://example.com/pic2.png images[1][name]="foobar2"
```

### Request body: deeply nested objects

The following JSON payload:

```json
{
    "description": "offer_description",
    "items": [
        {
            "description": null,
            "images": [
                {
                    "name": "pic1",
                    "url": "http://example.com/pic1.png"
                }
            ],
            "name": "item0",
            "price": 1.11,
            "tags": [],
            "tax": null
        }
    ],
    "name": "offer_name",
    "price": 12345.67
}
```

can be created with:

```bash
$ http post :5000/offers/ name="offer_name" description="offer_description" price=12345.67 items[0][name]="item0" items[0][price]=1.11 items[0][images][0][url]=http://example.com/pic1.png items[0][images][0][name]="pic1"
```


### Request body: array being top-level element (not an object)


```json
[
    {
        "name": "pic1",
        "url": "http://example.com/pic1.png"
    },
    {
        "name": "pic2",
        "url": "http://example.com/pic2.png"
    }
]
```

can be created with:

```bash
$ http post :5000/images/multiple/ [0][url]=http://example.com/pic1.png [0][name]="pic1" [1][url]=http://example.com/pic2.png [1][name]="pic2"
```

### Request body: arbitrary dict

```bash
$ http post :5000/index-weights/ 1=1.1 2=2.22
```

will send:

```json
{
    "1": 1.1,
    "2": 2.22
}
```

### Request body: sending datetimes, timedeltas, UUIDs

```bash
# Using ISO8601 format for duration
$ http put :5000/items/12345678-1234-5678-1234-567812345678 start_datetime=2026-02-14T19:37+02:00 end_datetime=2026-02-14T20:37+02:00 process_after=PT60S

# Using number of seconds
$ http put :5000/items/12345678-1234-5678-1234-567812345678 start_datetime=2026-02-14T19:37+02:00 end_datetime=2026-02-14T20:37+02:00 process_after:=60.0
```

## Cookies

### Single cookie

```bash
$ http get :5000/items/ Cookie:ads_id=1234
```

### Multiple cookies

```bash
$ http get :5000/items/ Cookie:"ads_id=1234;session_id=35"
```

## Headers

### Request with header

```bash
$ http :5000/v2/items/ X-Token:1
```

### Request with header accepting multiple values

```bash
$ http :5000/v2/items/ X-Token:1 X-Token:2
```

## Raw JSON

```bash
$ http post :5000/items/1 --raw '{"user":{"username": "jason", "full_name":"Jason Isaacs"},"item":{"name":"foo", "description":"foobar", "price":1.23, "tax":3.21, "tags":["baz", "foobar"]}}
```

## Forms

### Form fields
```bash
$ http --form POST :5000/login username="sergio" password="secret"
```

### Form with file fields

```bash
http --form POST :5000/files/ file@./main.py
```

### Mixing form fields and file fields

```bash
$ http --form :5000/files/ file_a@main.py file_b@main.py token=token1
```

## Streams

### Streaming response

```bash
# explicit use of streaming
$ http --stream :5000/items/stream-sync --verbose
```