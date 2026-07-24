# -*- coding: utf-8 -*-
import sys
import os

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import subprocess
import time
import re
import urllib.request

def get_public_url():
    print("Starting secure public tunnel...")
    cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=30", "-R", "80:127.0.0.1:8080", "nokey@localhost.run"]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore')
    
    url = None
    start_time = time.time()
    
    while time.time() - start_time < 20:
        line = process.stdout.readline()
        if not line:
            break
        print(line.strip())
        match = re.search(r'https://[a-zA-Z0-9-]+\.lhr\.life', line)
        if match:
            url = match.group(0)
            break
            
    return url, process

if __name__ == '__main__':
    url, proc = get_public_url()
    if url:
        print("\n=======================================================")
        print(f"ACTIVE PUBLIC URL: {url}")
        print("=======================================================")
        with open('PUBLIC_URL.txt', 'w', encoding='utf-8') as f:
            f.write(url)
        
        # Keep process alive
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            proc.terminate()
    else:
        print("Could not retrieve URL, retrying...")
