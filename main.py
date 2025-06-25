# app/main.py
import socket
import threading
import sys
from handler import handle_request
from security import has_crlf_injection
import time
from logger import log_request, alert_abnormal_behavior
import ssl  # Import SSL for secure connections




# Rate limit tracker: {ip: [timestamps]}
rate_limit = {}



def handle_connection(connection,directory):
    ip = connection.getpeername()[0]
   



    while True:
        request = connection.recv(1024).decode()
        if not request.startswith("GET") and not request.startswith("POST"):
         connection.send(b"HTTP/1.1 400 Bad Request\r\n\r\nThis server requires HTTPS.\r\n")
         connection.close()
         return

        if not request:
            break

        now = time.time()
        rate_limit.setdefault(ip, []).append(now)
        rate_limit[ip] = [t for t in rate_limit[ip] if now - t < 5]
        if len(rate_limit[ip]) > 10:
            alert_abnormal_behavior(ip, "Rate limit exceeded")
            connection.send(b"HTTP/1.1 429 Too Many Requests\r\n\r\nRate limit exceeded.")
            connection.close()
            return



        if has_crlf_injection(request): 
            alert_abnormal_behavior(ip, "CRLF injection attempt")
            connection.send(b"HTTP/1.1 400 Bad Request\r\n\r\nHeader injection detected.")
            connection.close()
            return


        print("Received request:\n", request)


        log_request(ip, request)  # Log every request

        if len(request) > 5000:
         alert_abnormal_behavior(ip, "Large request size")



        response = handle_request(request,directory)
        connection.send(response)

        if "connection: close" in request.lower():
            break

    connection.close()

def main():

    if len(sys.argv) != 3 or sys.argv[1] != "--directory":
        print("Usage: python main.py --directory <path_to_directory>")
        return

    directory = sys.argv[2]
    print("Starting server on port 4221...")

    server_socket = socket.create_server(("localhost", 4221))
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="certs/server.pem", keyfile="certs/server.key")
    server_socket = context.wrap_socket(server_socket, server_side=True)

    while True:
        connection, _ = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=(connection,directory))
        thread.start()

if __name__ == "__main__":
    main()
