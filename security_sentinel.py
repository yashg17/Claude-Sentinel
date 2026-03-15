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
SCORING RULES:
- 10.0: Confirmed SQLi/XSS
- 0.0: Normal traffic
Wrap score in <score></score> tags."""

def analyze_log(log_line):
    try:
        if "HEALTHCHECK" in log_line or not log_line.strip():
            return 0.0

        message = client.messages.create(
            model="claude-sonnet-4-6", # Updated to the March 2026 Standard
            max_tokens=50,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"Analyze: {log_line}"}]
        )
        raw_text = message.content[0].text
        match = re.search(r"<score>\s*(\d+\.?\d*)\s*</score>", raw_text)
        return float(match.group(1)) if match else 1.0
    except Exception as e:
        print(f"API Error: {e}")
        # Return 0.1 so your Grafana line shows a tiny "heartbeat"
        # to prove the script is alive even if the API fails.
        return 0.1

if __name__ == "__main__":
    start_http_server(8000, addr='0.0.0.0')
    print("Sentinel live on port 8000...")

    log_file = "app_access.log"
    SECURITY_SCORE.labels(job='ai-sentinel').set(0.0)

    # tail -F follows the file even if Jenkins deletes/recreates it
    cmd = ["tail", "-F", log_file]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        while True:
            # Check for new data every 1 second
            r, _, _ = select.select([process.stdout], [], [], 1.0)

            if r:
                line = process.stdout.readline()
                if line and line.strip():
                    score = analyze_log(line)
                    SECURITY_SCORE.labels(job='ai-sentinel').set(score)
                    print(f"Scored {score}: {line.strip()[:60]}...")
            else:
                # This causes the graph to drop back to 0 when quiet
                SECURITY_SCORE.labels(job='ai-sentinel').set(0.0)

    except KeyboardInterrupt:
        process.terminate()
