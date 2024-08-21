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

You can use tools like curl or Postman to test the API; examples below are `curl` under your own terminal/console.

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
curl -X POST -H "Content-Type: application/json" -d "{\"name\": \"New Item\"}" http://127.0.0.1:5000/items
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

### step-by-step - make it into production (example)
To deploy your Flask application to production on an Ubuntu server, you'll typically want to use a production-grade web server like Gunicorn along with a reverse proxy like Nginx. Here's a step-by-step guide to getting your Flask application into production on an Ubuntu server:

#### Step 1: Set Up Your Ubuntu Server
Update your server:
```
sudo apt update && sudo apt upgrade -y
```

Install necessary packages:
```
sudo apt install python3-pip python3-dev nginx
```

#### Step 2: Set Up Your Flask Application

Create a directory for your Flask application:
```
mkdir ~/myflaskapp
cd ~/myflaskapp
```
Create a Python virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

Install Flask and Gunicorn:
```
pip install Flask gunicorn
```
#### Create your Flask app (if you haven't already):

Create a file called app.py inside ~/myflaskapp/:
```
from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

# Sample data using UID hash instead of integer ID
items = [
    {"uid": str(uuid.uuid4()), "name": "Item 1"},
    {"uid": str(uuid.uuid4()), "name": "Item 2"},
    {"uid": str(uuid.uuid4()), "name": "Item 3"}
]

# GET method to retrieve all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# GET method to retrieve a single item by UID
@app.route('/items/<uid>', methods=['GET'])
def get_item(uid):
    item = next((item for item in items if item["uid"] == uid), None)
    if item is not None:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

# POST method to add a new item with a UID
@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.json
    new_item["uid"] = str(uuid.uuid4())  # Generate a new UUID
    items.append(new_item)
    return jsonify(new_item), 201

# PUT method to update an existing item or create it if it doesn't exist
@app.route('/items/<uid>', methods=['PUT'])
def update_item(uid):
    new_data = request.json
    item = next((item for item in items if item["uid"] == uid), None)

    if item is not None:
        # Update existing item
        item["name"] = new_data["name"]
        return jsonify(item)
    else:
        # Create new item with provided UID
        new_data["uid"] = uid
        items.append(new_data)
        return jsonify(new_data), 201

# DELETE method to delete an item by UID
@app.route('/items/<uid>', methods=['DELETE'])
def delete_item(uid):
    global items
    items = [item for item in items if item["uid"] != uid]
    return jsonify({"message": "Item deleted"}), 200

if __name__ == '__main__':
    app.run()
```

#### Step 3: Configure Gunicorn
Test Gunicorn locally:

While still in the ~/myflaskapp/ directory and with your virtual environment activated:
```
gunicorn --bind 0.0.0.0:8000 app:app
```
You should be able to access your Flask app at http://your_server_ip:8000.

#### Create a systemd service file for Gunicorn:

Create the file /etc/systemd/system/myflaskapp.service:
```
sudo nano /etc/systemd/system/myflaskapp.service
```

Add the following content:
```
[Unit]
Description=Gunicorn instance to serve myflaskapp
After=network.target

[Service]
User=your_username
Group=www-data
WorkingDirectory=/home/your_username/myflaskapp
Environment="PATH=/home/your_username/myflaskapp/venv/bin"
ExecStart=/home/your_username/myflaskapp/venv/bin/gunicorn --workers 3 --bind unix:myflaskapp.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
Replace your_username with your actual username.
```

Start and enable the Gunicorn service:
```
sudo systemctl start myflaskapp
sudo systemctl enable myflaskapp
```

#### Step 4: Configure Nginx as a Reverse Proxy
#### Create an Nginx configuration file

Create the file /etc/nginx/sites-available/myflaskapp:
```
sudo nano /etc/nginx/sites-available/myflaskapp
```

Add the following content:
```
server {
    listen 80;
    server_name your_domain_or_IP;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/your_username/myflaskapp/myflaskapp.sock;
    }
}
```

Replace your_domain_or_IP with your server's IP address or domain name, and replace your_username with your actual username.

Enable the Nginx configuration:
```
sudo ln -s /etc/nginx/sites-available/myflaskapp /etc/nginx/sites-enabled
```

Test Nginx configuration and restart:
```
sudo nginx -t
sudo systemctl restart nginx
```

Allow Nginx through the firewall (if applicable):
```
sudo ufw allow 'Nginx Full'
```

#### Step 5: Access Your Flask Application
You should now be able to access your Flask application by visiting http://your_domain_or_IP in your web browser.

#### Step 6: Securing Your Application
Consider using SSL to secure your application with HTTPS. You can obtain a free SSL certificate using Let's Encrypt and configure it with Nginx.

Install Certbot:
```
sudo apt install certbot python3-certbot-nginx
```

#### Obtain an SSL certificate:
```
sudo certbot --nginx -d your_domain_or_IP
```

Test the certificate renewal process:
```
sudo certbot renew --dry-run
```
Now your Flask application should be secured and running in production.
