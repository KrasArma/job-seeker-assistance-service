import os
import threading
from datetime import datetime
import csv

"""
CustomLogger — logger with info and error methods, file rotation, and per-level log files in CSV-table format for errors.

Usage:
from custom_logger import logger
logger.info('Module starts with params: ...')
logger.info('Module finish with results: ...')
logger.error('ErrorType', 'Error message', input_data, output_data, method, request_id)

- INFO: logs/info1.log, logs/info2.log (timestamp,message)
- ERROR: logs/error1.log, logs/error2.log (timestamp,error_type,message,method,request_id,input_data,output_data)
- File rotation: if a file exceeds MAX_SIZE, the next file is created, max 2 files per level (oldest is deleted)
"""

LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
MAX_SIZE = 1024 * 1024 * 2  # 2 MB per file
LEVELS = ['INFO', 'ERROR']

class CustomLogger:
    def __init__(self):
        self.lock = threading.Lock()
        os.makedirs(LOG_DIR, exist_ok=True)
        self.files = {level: [self._log_path(level, 1), self._log_path(level, 2)] for level in LEVELS}
        self._init_csv_headers()

    def _log_path(self, level, idx):
        return os.path.join(LOG_DIR, f"{level.lower()}{idx}.log")

    def _init_csv_headers(self):
        info_header = ['timestamp', 'message']
        error_header = ['timestamp', 'error_type', 'message', 'method', 'request_id', 'input_data', 'output_data']
        for idx in [1, 2]:
            info_path = self._log_path('INFO', idx)
            error_path = self._log_path('ERROR', idx)
            if not os.path.exists(info_path):
                with open(info_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(info_header)
            if not os.path.exists(error_path):
                with open(error_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(error_header)

    def info(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [timestamp, messag]
        with self.lock:
            self._write_csv('INFO', row)

    def error(self, error_type, message, input_data=None, output_data=None, method=None, request_id=None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [
            timestamp,
            error_type,
            message,
            method or '',
            request_id or '',
            repr(input_data) if input_data is not None else '',
            repr(output_data) if output_data is not None else ''
        ]
        with self.lock:
            self._write_csv('ERROR', row)

    def _write_csv(self, level, row):
        files = self.files.get(level)
        for idx, path in enumerate(files):
            if not os.path.exists(path) or os.path.getsize(path) < MAX_SIZE:
                with open(path, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(row)
                break
            elif idx == 1:
                os.remove(files[0])
                os.rename(files[1], files[0])
                with open(files[1], 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    if level == 'INFO':
                        writer.writerow(['timestamp', 'message'])
                    else:
                        writer.writerow(['timestamp', 'error_type', 'message', 'method', 'request_id', 'input_data', 'output_data'])
                    writer.writerow(row)
                break

logger = CustomLogger() 