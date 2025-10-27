# 🎯 Nexus Navigation Architect

**Professional SEO Category Builder 3.0** - Automatyczna budowa struktury kategorii dla sklepów e-commerce

![Version](https://img.shields.io/badge/version-3.0-orange)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Spis Treści

- [Cechy](#-cechy)
- [Wymagania](#-wymagania)
- [Instalacja](#-instalacja)
- [Szybki Start](#-szybki-start)
- [Workflow (5 Kroków)](#-workflow-5-kroków)
- [Interfejs](#-interfejs)
- [Zarządzanie Projektami](#-zarządzanie-projektami)
- [Edycja Promptów](#-edycja-promptów)
- [FAQ](#-faq)

---

## ✨ Cechy

### 🎨 Profesjonalny Interfejs
- **Dark Theme** - wzorowany na nowoczesnych aplikacjach webowych
- **3 główne zakładki** - Ustawienia, Workflow, Edytor Promptów
- **Logo i branding** - "Nexus Navigation Architect"
- **Progress tracking** - wizualizacja postępu dla każdego kroku

### 🔄 Pełny Workflow (Kroki 1-5)
1. **Krok 1** - Pobranie listy produktów z sitemap
2. **Krok 2** - Pobranie opisów produktów (Jina AI Reader)
3. **Krok 3** - Ekstrakcja parametrów produktów (AI)
4. **Krok 4** - Budowa wstępnej struktury kategorii (AI)
5. **Krok 5** - Finalizacja i optymalizacja SEO (AI)

### 📁 Zarządzanie Projektami
- **Foldery projektowe** - wszystkie pliki w jednym miejscu
- **Automatyczne backupy** - przed nadpisaniem plików
- **Status kroków** - wizualna indykacja wykonanych kroków
- **Wczytywanie projektów** - kontynuacja pracy

### 🛠️ Edytowalne Prompty
- **Edytor promptów** - dla kroków 3, 4, 5
- **Zapisywanie konfiguracji** - własne prompty per projekt
- **Reset do domyślnych** - powrót do oryginalnych promptów
- **Podgląd na żywo** - edycja z numeracją linii

### 🚀 Technologia
- **OpenRouter API** - dostęp do wszystkich modeli AI (OpenAI, Anthropic, Google, Meta, etc.)
- **Jina AI Reader** - ekstrakcja treści ze stron produktowych
- **Multi-threading** - równoległe przetwarzanie
- **Retry mechanism** - automatyczne ponawianie przy błędach

---

## 📦 Wymagania

- **Python 3.8+**
- **Klucz API OpenRouter** - https://openrouter.ai/keys (dla kroków 3-5)
- **Klucz API Jina AI** - https://jina.ai/reader (dla kroku 2)

---

## 🔧 Instalacja

### 1. Sprawdź Pythona

```bash
python --version
```

Jeśli nie masz Pythona, pobierz z https://www.python.org/downloads/

### 2. Sklonuj repozytorium

```bash
git clone https://github.com/maciusman/nexus-navigation-architect.git
cd nexus-navigation-architect
```

### 3. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 4. Uruchom aplikację

```bash
python app.py
```

---

## 🚀 Szybki Start

### Scenariusz 1: Nowy Projekt (Pełny Workflow)

1. **Uruchom aplikację**
   ```bash
   python app.py
   ```

2. **Tab: Ustawienia**
   - Wprowadź klucz **OpenRouter API**
   - Wprowadź klucz **Jina AI API**
   - Kliknij **"Załaduj modele"**
   - Kliknij **"Nowy projekt"** i podaj nazwę

3. **Tab: Workflow**
   - **Krok 1**: Wpisz URL sitemap i filtr (np. `.html`) LUB wybierz plik TXT z listą URL-i
   - **Krok 2**: Ustaw liczbę wątków dla Jina (domyślnie 10)
   - **Kroki 3-5**: Wybierz modele AI (auto-sugestie)
   - Zaznacz wszystkie kroki (1-5)
   - Kliknij **"▶ Start Workflow"**

4. **Czekaj na zakończenie**
   - Monitoruj logi i progress bar
   - Wynik w pliku `categories_final.json`

### Scenariusz 2: Kontynuacja Projektu (Tylko Kroki 3-5)

1. **Tab: Ustawienia**
   - Wprowadź klucz **OpenRouter API**
   - Kliknij **"Załaduj modele"**
   - Kliknij **"Wybierz"** i wskaż folder projektu

2. **Tab: Workflow**
   - Aplikacja automatycznie wykryje wykonane kroki (✅)
   - Odznacz wykonane kroki
   - Zaznacz tylko kroki do wykonania (np. tylko krok 5)
   - Kliknij **"▶ Start Workflow"**

---

## 🔄 Workflow (5 Kroków)

### Krok 1: Pobranie listy produktów

**Wejście:** URL sitemap LUB plik TXT z listą URL-i
**Wyjście:** `products.txt` (lista URL-i produktów)

**Metoda A: Parsowanie sitemap XML**
- `URL Sitemap` - adres sitemap index lub pojedynczego sitemap
- `Filtr URL` - pattern filtrowania (np. `.html`, `/product/`, `/p/`)

**Metoda B: Upload pliku TXT**
- Kliknij przycisk **"Wybierz plik"**
- Wybierz plik TXT z listą URL-i (jeden URL na linię)
- Plik zostanie skopiowany do projektu jako `products.txt`

**Przykład (Metoda A):**
- URL: `https://example.com/sitemap.xml`
- Filtr: `.html`
- Wynik: 500 URL-i produktów

**Przykład (Metoda B):**
```
https://example.com/product-1.html
https://example.com/product-2.html
https://example.com/product-3.html
```

---

### Krok 2: Pobranie opisów produktów

**Wejście:** `products.txt`
**Wyjście:** `content_website.json` (treści stron w markdown)

**Ustawienia:**
- `Wątki Jina` - liczba równoległych zapytań (1-20)
- `Powtórzenia` - ile razy powtórzyć przy błędzie (1-5)

**Technologia:** Jina AI Reader (konwersja HTML → Markdown)

---

### Krok 3: Ekstrakcja parametrów produktów

**Wejście:** `content_website.json`
**Wyjście:** `product_extraction.json` (kategorie + parametry)

**Ustawienia:**
- `Model AI` - zalecane: szybkie/tanie (Gemini Flash, GPT-4o-mini, Claude Haiku)
- `Wątki` - liczba równoległych zapytań do AI (1-30)
- `Powtórzenia` - ile razy powtórzyć przy błędzie JSON (1-5)

**Format JSON:**
```json
{
  "url": "https://...",
  "extraction": {
    "product_category": {
      "main_category": "Electronics",
      "subcategories": ["Smartphones", "Accessories"]
    },
    "product_parameters": {
      "brand": "Apple",
      "model": "iPhone 15",
      "color": "Black"
    }
  }
}
```

---

### Krok 4: Budowa struktury kategorii

**Wejście:** `product_extraction.json`
**Wyjście:** `categories_structure.json` (wstępna struktura nawigacji)

**Ustawienia:**
- `Model AI` - zalecane: szybkie modele
- `Rozmiar paczki` - ile produktów w jednej paczce (10-100)
- `Wątki batch` - liczba równoległych paczek (1-10)

**Batch Processing:**
- Dzieli produkty na paczki (domyślnie 100)
- Przetwarza paczki równolegle
- Merguje wyniki w jedną strukturę

**Format JSON:**
```json
{
  "main_navigation": [
    {
      "name": "Electronics",
      "subcategories": [
        {"name": "Smartphones"},
        {"name": "Laptops"}
      ]
    }
  ]
}
```

---

### Krok 5: Finalizacja i optymalizacja

**Wejście:** `categories_structure.json`
**Wyjście:** `categories_final.json` (finalna struktura SEO)

**Ustawienia:**
- `Model AI` - **zalecane: reasoning models** (o1, o1-mini, QwQ-32b, DeepSeek)
- `Powtórzenia` - ile razy powtórzyć przy błędzie (1-5)

**Optymalizacje:**
- Konsolidacja podobnych kategorii
- Limit głębokości do 3 poziomów
- Title case dla nazw
- Usunięcie redundancji

**Format JSON:**
```json
{
  "categories": [
    {
      "name": "Electronics",
      "subcategories": [
        {
          "name": "Smartphones",
          "subcategories": [
            {"name": "iPhone"},
            {"name": "Samsung"}
          ]
        }
      ]
    }
  ]
}
```

---

## 🎨 Interfejs

### Tab 1: ⚙️ Ustawienia

- **Klucze API**
  - OpenRouter API Key (dla kroków 3-5)
  - Jina AI API Key (dla kroku 2)
  - Przyciski testowania połączenia

- **Zarządzanie Projektem**
  - Wybór folderu projektu
  - Tworzenie nowego projektu
  - Wyświetlanie aktualnego projektu

### Tab 2: 🔄 Workflow

- **Kroki 1-5**
  - Checkbox wyboru kroku
  - Status kroku (✅ Wykonane / ⏸️ Do wykonania)
  - Ustawienia specyficzne dla kroku
  - Wybór modelu AI (dla kroków 3-5)

- **Postęp**
  - Progress bar z % postępu
  - Przyciski: Start, Stop, Odśwież Status

- **Logi**
  - Logi przetwarzania w czasie rzeczywistym
  - Informacje o błędach
  - Statystyki (X/Y przetworzonych)

### Tab 3: 📝 Edytor Promptów

- **Edytory dla kroków 3, 4, 5**
  - TextArea z numeracją linii
  - Syntax highlighting (opcjonalnie)
  - Podgląd promptu

- **Zarządzanie**
  - 💾 Zapisz konfigurację (do projektu)
  - 📂 Wczytaj konfigurację (z projektu)
  - 🔄 Resetuj do domyślnych

---

## 📁 Zarządzanie Projektami

### Struktura Projektu

```
projekty/
└── moj-sklep/
    ├── products.txt                  # Krok 1
    ├── content_website.json         # Krok 2
    ├── product_extraction.json      # Krok 3
    ├── categories_structure.json    # Krok 4
    ├── categories_final.json        # Krok 5 ⭐
    ├── prompts_config.json          # Własne prompty
    ├── project_settings.json        # Ustawienia projektu
    └── backups/                     # Automatyczne backupy
        ├── product_extraction_20250121_143052.json
        └── categories_final_20250121_150230.json
```

### Automatyczne Backupy

Przed nadpisaniem plików aplikacja tworzy automatyczne backupy z timestampem:

```
backups/
├── product_extraction_20250121_143052.json
├── categories_structure_20250121_145123.json
└── categories_final_20250121_150230.json
```

### Status Projektu

Plik `project_settings.json` przechowuje:

```json
{
  "project_name": "moj-sklep",
  "created_at": "2025-01-21T14:25:30",
  "last_modified": "2025-01-21T15:02:45",
  "steps_completed": {
    "step1": true,
    "step2": true,
    "step3": true,
    "step4": true,
    "step5": true
  }
}
```

---

## 🛠️ Edycja Promptów

### Domyślne Prompty

Prompty systemowe dla kroków 3-5 znajdują się w:

```
config/default_prompts.json
```

### Własne Prompty

1. **Edycja** - Tab "Edytor Promptów"
2. **Zapisanie** - Kliknij "💾 Zapisz konfigurację"
   - Zapisuje do `projekty/{nazwa_projektu}/prompts_config.json`
3. **Wczytanie** - Kliknij "📂 Wczytaj konfigurację"
   - Wczytuje z pliku projektu
4. **Reset** - Kliknij "🔄 Resetuj do domyślnych"

### Testowanie Promptów

1. Edytuj prompt dla kroku 5
2. Zapisz konfigurację
3. Odznacz kroki 1-4
4. Uruchom tylko krok 5
5. Porównaj wyniki z poprzednią wersją

**Tip:** Użyj folderów `backups/` do porównania wyników różnych promptów

---

## 💡 FAQ

### 1. Ile kosztuje użycie aplikacji?

Aplikacja jest **darmowa**, ale używa płatnych API:

- **OpenRouter** - pay-as-you-go, koszty zależą od modelu i liczby tokenów
  - Gemini Flash: ~$0.01-0.05 za 1000 produktów (krok 3)
  - o1-mini: ~$0.10-0.50 za finalizację (krok 5)

- **Jina AI Reader** - darmowy plan: 1M znaków/miesiąc
  - Wystarczy dla ~100-500 produktów

**Szacunkowy koszt dla 500 produktów:** $1-3 USD

### 2. Które modele wybrać dla kroków 3-5?

**Rekomendowane:**

- **Krok 3** (ekstrakcja): szybkie/tanie
  - ✅ Gemini Flash (najszybszy, najtańszy)
  - ✅ GPT-4o-mini (dobry stosunek jakość/cena)

- **Krok 4** (struktura): szybkie
  - ✅ Gemini Flash
  - ✅ Claude Haiku

- **Krok 5** (finalizacja): reasoning
  - ✅ o1-mini (najlepszy dla JSON)
  - ✅ QwQ-32b (tani reasoning)
  - ✅ DeepSeek (dobry i tani)
  - ✅ Gemini 2.5 Pro (doskonały reasoning)

### 3. Co zrobić gdy krok 5 zwraca błędy JSON?

1. Zmień model na **o1-mini** lub **QwQ-32b**
2. Zwiększ `Powtórzenia` do 5
3. Sprawdź czy prompt zawiera "Output ONLY valid JSON"
4. Sprawdź logi - aplikacja pokazuje fragment błędnej odpowiedzi

### 4. Czy mogę przerwać workflow i wznowić później?

**Tak!**

1. Kliknij "⏸ Stop" aby przerwać
2. Aplikacja zapisuje wyniki po każdym kroku
3. Uruchom ponownie aplikację
4. Wybierz projekt
5. Odznacz wykonane kroki (✅)
6. Uruchom tylko pozostałe

### 5. Jak testować różne modele dla tego samego kroku?

1. Wykonaj krok z modelem A
2. Sprawdź backup w `backups/`
3. Wykonaj krok ponownie z modelem B
4. Porównaj wyniki:
   - `backups/categories_final_timestampA.json` (model A)
   - `categories_final.json` (model B)

### 6. Czy mogę używać własnych promptów?

**Tak!**

1. Tab "Edytor Promptów"
2. Edytuj prompt dla wybranego kroku
3. Zapisz konfigurację (💾)
4. Uruchom workflow - użyje nowych promptów
5. W razie problemów: Resetuj do domyślnych (🔄)

### 7. Ile czasu trwa pełny workflow?

**Zależy od:**
- Liczby produktów
- Liczby wątków
- Wybranego modelu

**Przykłady:**

| Produkty | Wątki Jina | Wątki AI | Model | Czas |
|----------|------------|----------|--------|------|
| 100 | 10 | 1 | Gemini Flash | ~10 min |
| 500 | 10 | 5 | Gemini Flash + o1-mini | ~45 min |
| 1000 | 20 | 10 | GPT-4o-mini + QwQ | ~90 min |

**Tip:** Zwiększ wątki aby przyspieszyć (ale większy koszt API!)

### 8. Co jeśli sitemap ma >10,000 produktów?

**Opcje:**

1. **Filtruj w kroku 1**
   - Użyj filtra np. `/category/electronics/`
   - Przetworz tylko wybrane kategorie

2. **Podziel na batche**
   - Utwórz osobne projekty dla kategorii
   - Uruchom równolegle (osobne instancje app)

3. **Zwiększ wątki**
   - Krok 2: 20 wątków Jina
   - Krok 3: 30 wątków AI
   - Krok 4: 10 wątków batch

**Limit:** Aplikacja bez problemu obsłuży 10,000+ produktów

---

## 📞 Wsparcie

Jeśli masz problemy:

1. **Sprawdź logi** - aplikacja pokazuje szczegółowe błędy
2. **Sprawdź klucze API** - czy są aktywne i mają środki
3. **Sprawdź pliki** - czy `products.txt`, `content_website.json` etc. istnieją
4. **Sprawdź model** - spróbuj innego modelu (np. reasoning models dla kroku 5)

---

## 📄 Licencja

MIT License - projekt edukacyjny

---

**Nexus Navigation Architect** - Build Better E-commerce Navigation 🚀
