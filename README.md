### REST-api
When you run the code you will start a local server; could access the API endpoints using a tool like Postman or curl.
#### test1.py > basic level (read only api)
URLs that represent specific actions or resources.
- GET http://127.0.0.1:5000/items: Get all items.
- GET http://127.0.0.1:5000/items/1: Get item with ID 1.

try it out by:
```
py test1.py
```
#### test2.py > GET, POST, DELETE methods
Level 2 API will allow you to perform basic operations (`GET`, `POST`, `DELETE`) on a list of items.

You can use tools like curl or Postman to test the API; example below is `curl` under your own terminal/console.

Get all items (`GET /items`):
```
curl http://127.0.0.1:5000/items
```
Get a specific item by ID (`GET /items/<id>`):
```
curl http://127.0.0.1:5000/items/1
```
Add a new item (`POST /items`):
```
- curl -X POST -H "Content-Type: application/json" -d "{\"name\": \"New Item\"}" http://127.0.0.1:5000/items
```
Delete an item by ID (`DELETE /items/<id>`):
```
curl -X DELETE http://127.0.0.1:5000/items/1
```
try it out by:
```
py test2.py
```
#### test3.py > UUID (random hash instead of counter id)
By using a `UID hash` instead of an `incremental ID`, the API can handle more complex scenarios where unique identifiers are needed without relying on sequential numbers. This is particularly useful in distributed systems where guaranteeing uniqueness without a central authority is essential.

UUID Generation:
- Each item now has a uid field, which is a UUID string generated using `uuid.uuid4()`. This ensures a unique identifier for each item.

Endpoints:
- The `GET`, `POST`, and `DELETE` methods are now based on the uid instead of an integer id; awesome🎉

try it out by:
```
py test3.py
```
