import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type
import psycopg2
import os
import time

#To login to database use: http://localhost:5050. Then use password and login from docker-compose.yml. Later server is set.
DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_PORT = int(os.environ.get('DB_PORT', 5432))
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')

def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("Połączono z bazą danych")
            return conn
        except psycopg2.OperationalError:
            print("Błąd połączenia z bazą danych, ponawianie za 5 sekund...")
            time.sleep(5)

conn = connect_to_db()
cursor = conn.cursor()
cursor.execute("DELETE FROM users")
conn.commit()
cursor.execute("INSERT INTO users (id, first_name, last_name, role) VALUES (0, 'test', 'test', 'test')")
conn.commit()
# Define the request handler class by extending BaseHTTPRequestHandler.
# This class will handle HTTP requests that the server receives.
class SimpleRequestHandler(BaseHTTPRequestHandler):
    users = [{"index": 0 ,"name": "test", "surname": "test", "role": "test"}]
    def do_DELETE(self):
        #Complicated splitting :D
        query = self.path.split('?')
        if len(query) > 1:
                index = int(query[1].split('=')[1])
                if 0 <= index < len(self.users):
                    self.users.pop(index)
                    cursor.execute("DELETE FROM users WHERE id = %s", (index,))
                    conn.commit()

                    cursor.execute("SELECT id FROM users ORDER BY id")
                    users = cursor.fetchall()
                    #I added indexing here, which I didn't have before... I was deleting through positions.
                    for i in range(len(self.users)):
                        self.users[i]['index'] = i
                    for new_index, (user_id,) in enumerate(users):
                        cursor.execute("UPDATE users SET id = %s WHERE id = %s", (new_index, user_id))
                    conn.commit()

                    cursor.execute("SELECT * FROM users ORDER BY id")
                    rows = cursor.fetchall()
                    users_from_db = [{"index": row[0], "name": row[1], "surname": row[2], "role": row[3]} for row in rows]

                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()

                    response = {
                        "users": users_from_db
                    }
                    self.wfile.write(json.dumps(response).encode())


            
    # Handle OPTIONS requests (used in CORS preflight checks).
    # CORS (Cross-Origin Resource Sharing) is a mechanism that allows restricted resources
    # on a web page to be requested from another domain outside the domain from which the resource originated.
    def do_OPTIONS(self):
        # Send a 200 OK response to acknowledge the request was processed successfully.
        self.send_response(200, "OK")

        # Set headers to indicate that this server allows any origin (*) to access its resources.
        # This is important for browsers when making cross-origin requests.
        self.send_header("Access-Control-Allow-Origin", "*")

        # Specify the allowed HTTP methods that can be used in the actual request.
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

        # Indicate what request headers are allowed (e.g., Content-Type for JSON requests).
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        # End headers and complete the response
        self.end_headers()

    # Handle GET requests.
    # When the client sends a GET request, this method will be called.
    def do_GET(self) -> None:
        # Set the HTTP response status to 200 OK, which means the request was successful.
        self.send_response(200)
       
        # Set the Content-Type header to application/json, meaning the response will be in JSON format.
        self.send_header('Content-type', 'application/json')

        # Allow any domain to make requests to this server (CORS header).
        self.send_header('Access-Control-Allow-Origin', '*')

        # Finish sending headers
        self.end_headers()
        #Here im trying to add test into database.

        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        users_from_db = [{"index": row[0], "name": row[1], "surname": row[2], "role": row[3]} for row in rows]
        # Prepare the response data, which will be returned in JSON format.
        # The response contains a simple message and the path of the request.
        response = {
            "users": users_from_db
        }

        # Convert the response dictionary to a JSON string and send it back to the client.
        # self.wfile.write() is used to send the response body.
        self.wfile.write(json.dumps(response).encode())

    # Handle POST requests.
    # This method is called when the client sends a POST request.
    def do_POST(self) -> None:
        # Retrieve the content length from the request headers.
        # This tells us how much data to read from the request body.
        content_length: int = int(self.headers['Content-Length'])

        # Read the request body based on the content length.
        post_data: bytes = self.rfile.read(content_length)

        # Decode the received byte data and parse it as JSON.
        # We expect the POST request body to contain JSON-formatted data.
        received_data: dict = json.loads(post_data.decode())

        # Prepare the response data.
        # It includes a message indicating it's a POST request and the data we received from the client.
        username = received_data.get("name")
        surname = received_data.get("surname")
        role = received_data.get("role")
        if username and surname and role:

            new_index1 = len(self.users)
            self.users.append({"index": new_index1,"name": username, "surname": surname, "role": role})

            cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM users")
            new_index = cursor.fetchone()[0]
            
            cursor.execute(
                "INSERT INTO users (id, first_name, last_name, role) VALUES (%s, %s, %s, %s)",
                (new_index, username, surname, role)
            )
            conn.commit()

        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        users_from_db = [{"index": row[0], "name": row[1], "surname": row[2], "role": row[3]} for row in rows]
        # Send the response headers.
        # Set the status to 200 OK and indicate the response content will be in JSON format.
        self.send_response(200)
        self.send_header('Content-type', 'application/json')

        # Again, allow any origin to access this resource (CORS header).
        self.send_header('Access-Control-Allow-Origin', '*')

        # Finish sending headers.
        self.end_headers()
        response = {
            "message": "User added successfully",
            "users": users_from_db  
        }
        # Convert the response dictionary to a JSON string and send it back to the client.
        self.wfile.write(json.dumps(response).encode())


# Function to start the server.
# It takes parameters to specify the server class, handler class, and port number.
def run(
        server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler,
        port: int = 8000
) -> None:
    # Define the server address.
    # '' means it will bind to all available network interfaces on the machine, and the port is specified.
    server_address: tuple = ('', port)

    # Create an instance of HTTPServer with the specified server address and request handler.
    httpd: HTTPServer = server_class(server_address, handler_class)

    # Print a message to the console indicating that the server is starting and which port it will listen on.
    print(f"Starting HTTP server on port {port}...")

    # Start the server and make it continuously listen for requests.
    # This method will block the program and keep running until interrupted.
    httpd.serve_forever()


# If this script is executed directly (not imported as a module), this block runs.
# It calls the run() function to start the server.
if __name__ == '__main__':
    run()