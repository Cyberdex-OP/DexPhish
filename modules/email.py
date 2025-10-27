import openai, time, logging
from tenacity import retry, stop_after_attempt, wait_exponential

log = logging.getLogger("email")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
def generate_email(url: str, company: str, config: dict) -> str:
    prompt = f"Write a concise, urgent phishing email for {company}. Link: {url}. Under 130 words. Professional. No disclaimers."
    try:
        resp = openai.ChatCompletion.create(
            model=config['openai']['model'],
            messages=[{"role": "user", "content": prompt}],
            timeout=config['openai']['timeout']
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        log.error(f"AI gen failed: {e}")
        raise
