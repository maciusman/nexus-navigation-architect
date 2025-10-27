# 🚀 Quick Start - Nexus Navigation Architect

## Instalacja (jednorazowo)

### 1. Zainstaluj zależności

```bash
cd "x:\Aplikacje\SEO - 3.0 - Budowa kategorii ecommerce"
pip install -r requirements.txt
```

**Instalowane pakiety:**
- `requests` - HTTP requests
- `beautifulsoup4` - parsing XML/HTML
- `lxml` - parser XML
- `Pillow` - obrazki (logo)

### 2. Uzyskaj klucze API

#### OpenRouter (dla kroków 3-5)
1. Wejdź na https://openrouter.ai/keys
2. Zaloguj się (Google/GitHub/Email)
3. Kliknij "Create Key"
4. Skopiuj klucz

#### Jina AI (dla kroku 2)
1. Wejdź na https://jina.ai/reader
2. Zarejestruj się
3. Skopiuj API key z dashboard

---

## Uruchomienie

```bash
python app.py
```

---

## Pierwsze Użycie - Pełny Workflow

### Krok po kroku:

#### 1️⃣ Tab: Ustawienia

- **OpenRouter API Key:** wklej klucz
- **Jina AI API Key:** wklej klucz
- **Kliknij:** "Załaduj modele" ✅
- **Kliknij:** "Nowy projekt"
- **Podaj nazwę:** np. "moj-sklep"

#### 2️⃣ Tab: Workflow

**Krok 1: Sitemap**
- URL Sitemap: `https://twoj-sklep.pl/sitemap.xml`
- Filtr URL: `.html` (lub `/product/`)
- ☑️ Zaznacz "Uruchom krok 1"

**Krok 2: Jina Reader**
- Wątki Jina: `10`
- Powtórzenia: `3`
- ☑️ Zaznacz "Uruchom krok 2"

**Krok 3: Ekstrakcja**
- Model AI: `Google Gemini Flash` (auto-wybrane)
- Wątki: `1`
- Powtórzenia: `4`
- ☑️ Zaznacz "Uruchom krok 3"

**Krok 4: Struktura**
- Model AI: `Google Gemini Flash` (auto-wybrane)
- Rozmiar paczki: `100`
- Wątki batch: `10`
- ☑️ Zaznacz "Uruchom krok 4"

**Krok 5: Finalizacja**
- Model AI: `OpenAI o1-mini` (auto-wybrane)
- Powtórzenia: `3`
- ☑️ Zaznacz "Uruchom krok 5"

#### 3️⃣ Uruchomienie

- **Kliknij:** "▶ Start Workflow"
- **Czekaj** - monitoruj logi i progress bar
- **Wynik:** `projekty/moj-sklep/categories_final.json` ⭐

---

## Typowe Scenariusze

### Scenariusz A: Mam już products.txt i content_website.json

1. **Nowy projekt** lub **Wybierz** istniejący folder
2. **Skopiuj** `products.txt` i `content_website.json` do folderu projektu
3. **Odśwież Status** - kroki 1 i 2 będą ✅
4. **Zaznacz** tylko kroki 3, 4, 5
5. **Start Workflow**

### Scenariusz B: Chcę tylko zoptymalizować kategorię (krok 5)

1. **Wybierz** projekt z wykonanymi krokami 1-4
2. **Odśwież Status** - kroki 1-4 będą ✅
3. **Odznacz** kroki 1-4
4. **Zaznacz** tylko krok 5
5. **Zmień model** (np. testuj różne: o1-mini, QwQ, DeepSeek)
6. **Start Workflow**

### Scenariusz C: Edycja promptów

1. **Tab:** "Edytor Promptów"
2. **Wybierz:** Krok 3/4/5
3. **Edytuj** prompt (np. dodaj "Focus on brand names")
4. **Zapisz konfigurację** 💾
5. **Tab:** "Workflow"
6. **Uruchom** wybrany krok
7. **Porównaj** wyniki z `backups/`

---

## Wskazówki

### 💰 Oszczędzanie kosztów
- **Krok 1-2:** Darmowe (Jina ma darmowy tier)
- **Krok 3:** Użyj Gemini Flash (najtańszy)
- **Krok 4:** Użyj Gemini Flash
- **Krok 5:** Użyj QwQ-32b lub DeepSeek (tanie reasoning)

### ⚡ Przyspieszenie
- **Krok 2:** Zwiększ wątki Jina do 20
- **Krok 3:** Zwiększ wątki AI do 10 (ale droższe!)
- **Krok 4:** Zwiększ wątki batch do 10

### 🎯 Jakość wyników
- **Krok 3:** Gemini Flash wystarczy
- **Krok 4:** Gemini Flash wystarczy
- **Krok 5:** Użyj **o1-mini** (najlepszy dla JSON) lub **Claude Sonnet** (najlepszy dla treści)

### 🔧 Troubleshooting

**Problem: "Nie udało się załadować modeli"**
- Sprawdź klucz OpenRouter
- Sprawdź internet
- Sprawdź saldo na OpenRouter

**Problem: "Błęd JSON w kroku 5"**
- Zmień model na o1-mini
- Zwiększ powtórzenia do 5
- Sprawdź prompt (czy zawiera "Output ONLY valid JSON")

**Problem: "Krok 2 trwa wieczność"**
- Zmniejsz liczbę produktów (użyj filtra w kroku 1)
- Zwiększ wątki Jina do 20
- Sprawdź czy URL-e są poprawne

**Problem: "Brak pliku X"**
- Odśwież Status
- Sprawdź folder projektu
- Uruchom poprzedni krok

---

## Struktura Wynikowa

Po zakończeniu workflow w folderze projektu:

```
projekty/moj-sklep/
├── products.txt                     # 500 URL-i produktów
├── content_website.json            # Treści stron (markdown)
├── product_extraction.json         # Ekstrakcja (kategorie+parametry)
├── categories_structure.json       # Wstępna struktura
├── categories_final.json           # ⭐ FINALNA STRUKTURA
├── prompts_config.json             # Twoje prompty (opcjonalnie)
├── project_settings.json           # Status projektu
└── backups/                        # Automatyczne backupy
    ├── categories_structure_20250121_143052.json
    └── categories_final_20250121_150230.json
```

**Główny wynik:** `categories_final.json` 🎯

---

## Next Steps

Po uzyskaniu `categories_final.json`:

1. **Przejrzyj strukturę** - otwórz plik w edytorze JSON
2. **Zaimportuj do CMS** - PrestaShop, WooCommerce, Shopify
3. **Optymalizuj dalej** - uruchom krok 5 ponownie z innym modelem
4. **Export do formatu** - CSV, XML (TODO: future feature)

---

**Happy Building! 🚀**

*Nexus Navigation Architect - Professional SEO Category Builder*
