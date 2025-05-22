# zara_spider.py

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import pandas as pd
import time
from tqdm import tqdm

class ZaraSpider:
    BASE_URL = 'https://www.zara.com/ww/en/woman-dresses-l1066.html'

    def __init__(self, max_pages: int = 50, headless: bool = True):
        self.max_pages = max_pages
        self.headless = headless
        self.results = []



    def _init_browser(self):
        playwright = sync_playwright().start()
        # Launch with headless=False so we can mimic a real browser
        browser = playwright.chromium.launch(headless=False,
                                             args=[
                                                 "--disable-blink-features=AutomationControlled"
                                             ])
        # Create context with a common User-Agent and language header
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9"
            }
        )
        return playwright, browser, context


    def _close_browser(self, playwright, browser):
        browser.close()
        playwright.stop()

    def scrape(self, delay: float = 2.0):
        # 1️⃣ Initialize browser and navigate
        playwright, browser, context = self._init_browser()
        page = context.new_page()
        page.goto(self.BASE_URL, timeout=60000)

        # 2️⃣ Handle infinite scroll so all products load
        self._handle_infinite_scroll(page)

        # 3️⃣ DEBUG: dump the fully rendered HTML to disk
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        print("📝 Wrote debug_page.html – open this in your editor to inspect selectors")

        # 4️⃣ Now start parsing products and paginating
        for _ in tqdm(range(self.max_pages), desc="Pages scraped"):
            try:
                self._parse_products(page)

                # Click the "Next" button if it exists and is enabled
                next_btn = page.query_selector('button[aria-label="Next"]')
                if not next_btn or next_btn.is_disabled():
                    break

                next_btn.click()
                page.wait_for_timeout(2000)  # polite pause
                self._handle_infinite_scroll(page)

            except Exception as e:
                print(f"⚠️ Error on page iteration: {e}")
                time.sleep(delay)
                continue

        # 5️⃣ Clean up browser
        self._close_browser(playwright, browser)

        # 6️⃣ Return results as DataFrame
        return pd.DataFrame(self.results)


    def _handle_infinite_scroll(self, page, scroll_pause: float = 1.0, max_scrolls: int = 20):
        """Scroll down incrementally to load JS-rendered items."""
        previous_height = page.evaluate("() => document.body.scrollHeight")
        for _ in range(max_scrolls):
            page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(scroll_pause * 1000)
            new_height = page.evaluate("() => document.body.scrollHeight")
            if new_height == previous_height:
                break
            previous_height = new_height
        time.sleep(scroll_pause)

    def _parse_products(self, page):
        items = page.query_selector_all('li.product-grid-product')
        for item in items:
            try:
                # ── 1) Listing-level data
                link = item.query_selector('a.product-link').get_attribute('href')
                img  = item.query_selector('img.media-image__image').get_attribute('src')
                title = item.query_selector('img.media-image__image').get_attribute('alt')

                # ── 2) Open detail page to get price
                detail_page = page.context.new_page()
                detail_page.goto(link, timeout=60000)
                detail_page.wait_for_selector('span.money-amount__main')

                price = detail_page.query_selector('span.money-amount__main').inner_text().strip()

                detail_page.close()

                # ── 3) Save the result
                self.results.append({
                    'title': title,
                    'price': price,
                    'link': link,
                    'image': img
                })

            except Exception as e:
                print(f"⚠️ Skipping item due to error: {e}")
                continue


if __name__ == '__main__':
    spider = ZaraSpider(max_pages=30, headless=True)
    df = spider.scrape()
    df.to_csv('zara_products.csv', index=False)
    print(f"Scraped {len(df)} items. Saved to zara_products.csv")
