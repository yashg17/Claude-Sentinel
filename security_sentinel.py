import os
import re
import time
from anthropic import Anthropic
from prometheus_client import start_http_server, Gauge

# 1. Prometheus Metric Setup
SECURITY_SCORE = Gauge('log_security_score', 'Security risk score of the latest log line', ['log_source'])

# 2. Anthropic Client Setup
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a security log risk scoring engine.
SCORING RULES:
- 10.0: Confirmed SQLi/XSS
- 0.0: Normal traffic

CRITICAL INSTRUCTION:
You must wrap your final numerical score in <score></score> tags.
Example: <score>9.5</score>
Do not provide any other analysis or tables."""

def analyze_log(log_line):
    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=50,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"Analyze this log: {log_line}"}]
        )

        raw_text = message.content[0].text

        # Look for the number inside the XML tags
        match = re.search(r"<score>\s*(\d+\.?\d*)\s*</score>", raw_text)

        if match:
            return float(match.group(1))
        else:
            # Fallback: find any number if tags are missing
            fallback = re.search(r"(\d+\.?\d*)", raw_text)
            if fallback:
                return float(fallback.group(1))

            print(f"Still no score found. Raw output: {raw_text}")
            return 1.0

    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return 1.0

if __name__ == "__main__":
    # Start Prometheus exporter on port 8000
    start_http_server(8000)
    print("Sentinel is watching... Metrics at http://localhost:8000")

    test_log = '192.168.1.1 - - [14/Mar/2026:12:00:01] "GET /search?id=1; SELECT * FROM users HTTP/1.1" 200'

    while True:
        risk_score = analyze_log(test_log)
        SECURITY_SCORE.labels(log_source='web_access').set(risk_score)
        print(f"Log Analyzed. Risk Score: {risk_score}")
        time.sleep(10) # Wait 10 seconds so you don't burn through API credits
