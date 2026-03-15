import os
import re
import subprocess
import time
import select
from anthropic import Anthropic
from prometheus_client import start_http_server, Gauge

# 1. Prometheus Metric Setup
SECURITY_SCORE = Gauge('log_security_score', 'Risk score', ['job'])

# 2. Anthropic Client Setup
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a security log risk scoring engine.
CRITICAL: Only output a single number between 0.0 and 10.0 wrapped in <score> tags.
- SQLi/XSS = 10.0
- Normal = 0.0"""

def analyze_log(log_line):
    try:
        if "HEALTHCHECK" in log_line or not log_line.strip():
            return 0.0

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=200, # Increased for Claude 4.6 'thinking' space
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"Analyze: {log_line}"}]
        )
        raw_text = message.content[0].text
        print(f"DEBUG - AI Response: {raw_text}") # See the raw output

        # 1. Try to find the number within tags
        match = re.search(r"<score>\s*(\d+\.?\d*)\s*</score>", raw_text)
        if match:
            return float(match.group(1))

        # 2. Fallback: If tags are missing/broken, find the first number in the text
        numbers = re.findall(r"\d+\.\d+|\d+", raw_text)
        if numbers:
            return float(numbers[0])

        return 0.0
    except Exception as e:
        print(f"API Error: {e}")
        return 0.5

if __name__ == "__main__":
    start_http_server(8000, addr='0.0.0.0')
    print("Sentinel live on port 8000...")

    log_file = "app_access.log"
    SECURITY_SCORE.labels(job='ai-sentinel').set(0.0)

    cmd = ["tail", "-F", log_file]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        while True:
            r, _, _ = select.select([process.stdout], [], [], 1.0)
            if r:
                 line = process.stdout.readline()
                 if line and line.strip():
                     score = analyze_log(line)
                     SECURITY_SCORE.labels(job='ai-sentinel').set(score)
                     print(f"Scored {score}: {line.strip()[:60]}...")
                     # THIS LINE IS KEY: It keeps the 10.0 active long enough
                     # for Prometheus to 'catch' it before the loop resets to 0.0
                     time.sleep(2)
            else:
                SECURITY_SCORE.labels(job='ai-sentinel').set(0.0)
    except KeyboardInterrupt:
        process.terminate()
