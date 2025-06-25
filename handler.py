import os
import gzip
import re
from security import is_safe_path


# app/handler.py
def handle_request(request: str, directory: str) -> bytes:
    # Step 1: Extract request line
    request_line = request.split("\r\n")[0]
    method, path, version = request_line.split(" ")


    if method != "GET": 
        return b"HTTP/1.1 405 Method Not Allowed\r\n\r\n"
    # Step 2: Handle root path
    if path == "/":
        return b"HTTP/1.1 200 OK\r\n\r\n"

    # Step 3: Handle echo path
    elif path.startswith("/echo/"):
        

        message = path[len("/echo/"):]
        raw_body = message.encode()

        accept_encoding = ""
        connection_close = False

        for line in request.split("\r\n"):
            if line.lower().startswith("accept-encoding:"):
                accept_encoding = line.split(":", 1)[1].strip().lower()
            elif line.lower().startswith("connection:") and "close" in line.lower():
                connection_close = True
        
        accept_encoding = [ e.strip() for e in accept_encoding.split(",")]

        

        if "gzip" in accept_encoding:
            body = gzip.compress(raw_body)
            headers = [
            "HTTP/1.1 200 OK",
            "Content-Type: text/plain",
            f"Content-Length: {len(body)}",
            "Content-Encoding: gzip"
        ]


        else:
            body = raw_body
            headers = [
            "HTTP/1.1 200 OK",
            "Content-Type: text/plain",
            f"Content-Length: {len(body)}"
        ]
            
        if connection_close:
            headers.append("Connection: close")
            
        response = "\r\n".join(headers) + "\r\n\r\n"
        return response.encode() + body
    

    elif path == "/user-agent":
        user_agent = "" 
        for line in request.split("\r\n"):
            if line.lower().startswith("user-agent:"):
                user_agent = line.split(":", 1)[1].strip()
                break
        body = user_agent.encode()
        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
        )
        return headers.encode() + body
    
    elif path.startswith("/files/"):
        

        filename = path[len("/files/"):]  # Get just the filename
        
        if not is_safe_path(directory, filename):
            return b"HTTP/1.1 400 Bad Request\r\n\r\nInvalid filename."

        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                content = f.read()
            headers = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/octet-stream\r\n"
                f"Content-Length: {len(content)}\r\n"
                "\r\n"
            )
            return headers.encode() + content
        else:
            return b"HTTP/1.1 404 Not Found\r\n\r\n"
    
    elif path.startswith("/files/") and method == "POST":
        

        filename = path[len("/files/"):]
        file_path = os.path.join(directory,filename)

        content_length = 0
        for line in request.split("\r\n"):
            if line.lower().startswith("content-length:"):
                content_length = int(line.split(":",1)[1].strip())
                break
        
        body_split = request.split("\r\n\r\n", 1)
        body = body_split[1][:content_length] if len(body_split) > 1 else ""

        # Write to file
        with open(file_path, "wb") as f:
            f.write(body.encode())

        return b"HTTP/1.1 201 Created\r\n\r\n"
            


    else:
        return b"HTTP/1.1 404 Not Found\r\n\r\n"
