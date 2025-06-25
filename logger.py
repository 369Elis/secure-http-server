import logging
from datetime import datetime

logging.basicConfig(
    filename='log/requests.log',
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_request(ip, request):
    logging.info(f"Request from {ip}:\n{request}")

def alert_abnormal_behavior(ip, reason):
    logging.warning(f"⚠️ ALERT from {ip}: {reason}")
