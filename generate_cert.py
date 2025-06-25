from OpenSSL import crypto
from pathlib import Path

certs_dir = Path("certs")
certs_dir.mkdir(exist_ok=True)

key_file = certs_dir / "server.key"
cert_file = certs_dir / "server.pem"

# Create key pair
k = crypto.PKey()
k.generate_key(crypto.TYPE_RSA, 2048)

# Create certificate
cert = crypto.X509()
cert.get_subject().CN = "localhost"
cert.set_serial_number(1000)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(365*24*60*60)
cert.set_issuer(cert.get_subject())
cert.set_pubkey(k)
cert.sign(k, 'sha256')

with open(cert_file, "wb") as f:
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
with open(key_file, "wb") as f:
    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

print("✅ Self-signed certificate saved to certs/server.pem and server.key")
