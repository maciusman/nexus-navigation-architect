"""
Jina Reader API Client - do pobierania treści stron produktowych
"""
import requests
from typing import Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


class JinaClient:
    """Klient do komunikacji z Jina Reader API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://r.jina.ai/"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-Engine": "browser",
            "X-Retain-Images": "none",
            "X-Return-Format": "markdown"
        }

    def fetch_url(self, url: str, max_retries: int = 3) -> Dict[str, str]:
        """Pobierz treść pojedynczego URL"""
        for attempt in range(max_retries + 1):
            try:
                data = {"url": url}
                response = requests.post(
                    self.base_url,
                    headers=self.headers,
                    json=data
                )
                response.raise_for_status()
                return {"url": url, "content": response.text}
            except Exception as e:
                if attempt < max_retries:
                    continue
                else:
                    return {"url": url, "content": "", "error": str(e)}

    def fetch_urls_parallel(
        self,
        urls: list,
        num_threads: int = 10,
        max_retries: int = 3,
        progress_callback=None,
        stop_flag_callback=None
    ) -> list:
        """Pobierz treść wielu URL równolegle"""
        results = []
        total = len(urls)
        processed = 0

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []

            # Submit tasks and check stop flag
            for url in urls:
                if stop_flag_callback and not stop_flag_callback():
                    break
                future = executor.submit(self.fetch_url, url, max_retries)
                futures.append(future)

            # Collect results
            for future in as_completed(futures):
                # Check if should stop
                if stop_flag_callback and not stop_flag_callback():
                    # Cancel remaining futures
                    for f in futures:
                        f.cancel()
                    break

                result = future.result()
                results.append(result)
                processed += 1

                if progress_callback:
                    progress_callback(processed, total)

        return results

    def test_connection(self) -> bool:
        """Testuj połączenie z API"""
        try:
            test_url = "https://example.com"
            result = self.fetch_url(test_url, max_retries=1)
            return "content" in result and result["content"] != ""
        except Exception:
            return False
