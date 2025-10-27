"""
Sitemap Parser - do pobierania listy URL produktów z sitemap
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Optional


class SitemapParser:
    """Parser sitemap XML"""

    def __init__(self):
        self.product_urls = []

    def parse_sitemap(
        self,
        sitemap_url: str,
        filter_pattern: Optional[str] = None,
        progress_callback=None
    ) -> List[str]:
        """
        Parsuj sitemap i wyfiltruj URL-e produktów

        Args:
            sitemap_url: URL do sitemap index lub pojedynczego sitemap
            filter_pattern: Pattern do filtrowania URL-i (np. ".html", "/product/")
            progress_callback: Callback do raportowania postępu

        Returns:
            Lista przefiltrowanych URL-i produktów
        """
        self.product_urls = []

        if progress_callback:
            progress_callback("Pobieranie sitemap index...")

        # Pobierz sitemap index
        index_response = requests.get(sitemap_url)
        index_response.raise_for_status()
        index_content = index_response.content

        # Parsuj XML
        index_soup = BeautifulSoup(index_content, 'xml')

        # Sprawdź czy to sitemap index czy pojedynczy sitemap
        sitemap_urls = [loc.text for loc in index_soup.find_all('loc')]

        # Jeśli brak sub-sitemap, traktuj jako główny sitemap
        if not sitemap_urls or sitemap_url in sitemap_urls:
            sitemap_urls = [sitemap_url]

        if progress_callback:
            progress_callback(f"Znaleziono {len(sitemap_urls)} sitemap(ów) do przetworzenia")

        # Pobierz i parsuj każdy sitemap
        for idx, sm_url in enumerate(sitemap_urls, 1):
            if progress_callback:
                progress_callback(f"Przetwarzanie sitemap {idx}/{len(sitemap_urls)}")

            sm_response = requests.get(sm_url)
            sm_response.raise_for_status()
            sm_soup = BeautifulSoup(sm_response.content, 'xml')

            # Wyciągnij wszystkie URL-e
            for url_tag in sm_soup.find_all('url'):
                loc = url_tag.find('loc')
                if loc:
                    url = loc.text

                    # Filtruj według patternu jeśli podany
                    if filter_pattern is None or filter_pattern in url:
                        self.product_urls.append(url)

        if progress_callback:
            progress_callback(f"Znaleziono {len(self.product_urls)} URL-i produktów")

        return self.product_urls

    def save_to_file(self, filepath: str):
        """Zapisz URL-e do pliku tekstowego"""
        with open(filepath, 'w', encoding='utf-8') as f:
            for url in self.product_urls:
                f.write(url + '\n')

    def load_from_file(self, filepath: str) -> List[str]:
        """Wczytaj URL-e z pliku tekstowego"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.product_urls = [line.strip() for line in f if line.strip()]
        return self.product_urls

    def get_urls(self) -> List[str]:
        """Pobierz listę URL-i"""
        return self.product_urls

    def count(self) -> int:
        """Liczba znalezionych URL-i"""
        return len(self.product_urls)
