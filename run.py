import subprocess
import uvicorn
from pymongo import MongoClient
from config.config import settings
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import signal

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, server_process):
        self.server_process = server_process

    def on_any_event(self, event):
        print(f"Change detected: {event.src_path}. Restarting server...")
        os.kill(self.server_process.pid, signal.SIGTERM)
        time.sleep(1)
        self.server_process = start_fastapi()

def start_mongo():
    try:
        subprocess.run(["mongod", "--fork", "--logpath", "/var/log/mongodb.log", "--dbpath", "/data/db"])
        print("MongoDB started successfully.")
    except Exception as e:
        print(f"Failed to start MongoDB: {e}")

def start_fastapi():
    return subprocess.Popen(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    start_mongo()
    server_process = start_fastapi()

    event_handler = ReloadHandler(server_process)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
