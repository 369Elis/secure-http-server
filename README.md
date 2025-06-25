<<<<<<< HEAD
# 🔐 Secure HTTP Server in Python

This project is a low-level, multithreaded HTTP/1.1 server built from scratch using Python's `socket` and `ssl` modules. It supports basic HTTP functionality along with essential security features, making it a practical learning tool for network programming and secure server design.

---

## 🚀 Features

- 📡 Handles `GET`, `POST`, `/echo/`, `/user-agent`, and `/files/` endpoints
- 🔒 TLS encryption via self-signed certificate (HTTPS)
- 🛡 Input validation to block path traversal (`../`, `\`, `<script>`)
- ❌ CRLF injection protection
- 🚦 Rate limiting per IP (10 requests / 5 seconds)
- 📄 Request logging with alerting for suspicious behavior
- 🧼 Gracefully handles non-HTTPS connections

---

## 🔧 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/secure-http-server.git
cd secure-http-server
```

2. Install required Python package
   pip install pyOpenSSL

3. Generate TLS certificate
   python generate_cert.py

4. Run the server
   python main.py --directory .

🔍 Example Endpoints

curl -k https://localhost:4221/echo/hello
curl -k -X POST https://localhost:4221/files/test.txt --data "Hello, file!"
curl -k https://localhost:4221/files/test.txt

🛠 Tech Stack
Python 3.12

Sockets + Threads

TLS (ssl)

pyOpenSSL (for cert generation)
=======
# secure-http-server
>>>>>>> a610f9df49dd199f25924dbc827cf982eed7f37c
