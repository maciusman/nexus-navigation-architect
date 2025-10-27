# 📋 Changelog - Nexus Navigation Architect

Wszystkie istotne zmiany w projekcie będą dokumentowane w tym pliku.

---

## [3.0.4] - 2025-01-21

### 🎨 UI Polish - Subtelne Ulepszenia Wizualne

#### ✅ Poprawki Kolorów
- ✅ Dodano `option_add` dla Combobox dropdown menu - ciemne tło (#2a2a2a)
- ✅ Rozszerzono `style.map` dla Combobox - stany readonly/disabled
- ✅ Rozszerzono `style.map` dla Spinbox - stany readonly/disabled
- ✅ Dodano `selectbackground` i `selectforeground` dla lepszego zaznaczenia

#### ✅ Ulepszenia Przycisków
- ✅ Większy padding przycisków (15x8px) - lepszy clickable area
- ✅ Dodano hover state dla Dark.TButton (#323232)
- ✅ Smooth transitions dla Accent.TButton (orange → #ff8533)
- ✅ `relief='flat'` dla nowoczesnego wyglądu

#### 🎯 Efekty
- ✅ Dropdown menu comboboxów ma ciemne tło
- ✅ Hover effect na przyciskach (subtelne podświetlenie)
- ✅ Lepszy kontrast zaznaczenia w listach

**Zmienione pliki:**
- `app.py`: setup_dark_theme() - dodane mapowania i option_add

**UWAGA:** Zero zmian w funkcjonalności - tylko kosmetyczne poprawki!

---

## [3.0.3] - 2025-01-21

### 🔧 Poprawki Krytyczne i UI Polish

#### ✅ NAPRAWIONO TRYB AUTOMATYCZNY (🔴 KRYTYCZNE)
- ✅ Walidacja kroków nie blokuje uruchomienia wszystkich kroków 1-5 naraz
- ✅ Zmieniono logikę w `start_workflow()` (linie 917-928)
- ✅ Dodano warunek: `and not self.run_stepX.get()` dla każdej walidacji
- ✅ Teraz można zaznaczyć wszystkie kroki i uruchomić pełny workflow

**Przed:** Uruchomienie kroków 1-5 → błąd "Krok 2 wymaga wykonania kroku 1"
**Po:** Uruchomienie kroków 1-5 → workflow wykonuje wszystkie kroki po kolei ✅

#### ✅ Resume Workflow po STOP
- ✅ Przycisk "Kontynuuj" aktywuje się po naciśnięciu STOP
- ✅ Użytkownik może wznowić workflow od miejsca zatrzymania
- ✅ Dodano `self.last_completed_step` - tracking postępu
- ✅ `run_workflow_thread(resume=False)` - parametr resume
- ✅ Skip wykonanych kroków przy wznowieniu
- ✅ `continue_workflow()` obsługuje tryb nadzorowany + resume

**Scenariusz:**
1. Start workflow kroków 1-5
2. STOP w trakcie kroku 2
3. Sprawdzenie częściowych wyników
4. Kontynuuj → workflow wznawia od kroku 2 (pomija krok 1)

#### 🎨 UI Improvements

**Wyłączono scroll w comboboxach:**
- ✅ Unbind MouseWheel, Button-4, Button-5 dla comboboxów modeli
- ✅ Zapobiega przypadkowej zmianie modelu przy scrollowaniu

**Dark theme dla Entry readonly:**
- ✅ Zamieniono ttk.Entry (readonly) na tk.Label
- ✅ Plik URL-ami: ciemne tło (#2a2a2a), widoczny tekst (#e0e0e0)

**Dark theme dla Spinboxów:**
- ✅ Dodano styl `Dark.TSpinbox` w `setup_dark_theme()`
- ✅ Wszystkie 7 spinboxów (wątki, powtórzenia, paczki) z ciemnym tłem

#### 📁 Zmienione Pliki
- `app.py`: Walidacja kroków, resume workflow, UI fixes

---

## [3.0.2] - 2025-01-21

### 🔧 Poprawki i Ulepszenia

#### ✅ Naprawiono Przycisk STOP
- ✅ Krok 2 (Jina): Dodano `stop_flag_callback` do `fetch_urls_parallel()` - prawidłowe anulowanie pending requests
- ✅ Krok 3 (Ekstrakcja): Anulowanie futures w ThreadPoolExecutor przy STOP
- ✅ Krok 4 (Struktura): Anulowanie futures w ThreadPoolExecutor przy STOP
- ✅ Krok 5 (Finalizacja): Sprawdzanie `self.processing` w pętli retry

#### ✨ Nowy Tryb Nadzorowany (Human-in-the-Loop)
- ✅ Checkbox "Tryb nadzorowany (Human-in-the-loop)" w zakładce Workflow
- ✅ Po każdym kroku workflow się zatrzymuje i czeka na potwierdzenie użytkownika
- ✅ Przycisk "Kontynuuj" do przejścia do kolejnego kroku
- ✅ Użytkownik może sprawdzić wyniki pośrednie przed kontynuacją
- ✅ Metoda `_wait_for_confirmation(step_name)` z polling loop
- ✅ Dodano zmienną `self.waiting_for_confirmation`

#### 🎨 Dark Input Dialog
- ✅ Zastąpiono `tk.simpledialog.askstring()` własnym `DarkInputDialog`
- ✅ Spójny dark theme dla okna "Nowy projekt"
- ✅ Dodano brakujący import `simpledialog`
- ✅ Custom styling (bg: #1a1a1a, fg: #e0e0e0, accent: #f97316)

#### 📁 Zmienione Pliki
- `app.py`: DarkInputDialog class, supervised mode, STOP fixes
- `utils/jina_client.py`: stop_flag_callback parameter

---

## [3.0.1] - 2025-01-21

### 🎨 UI Improvements

#### ✅ Custom Scrollbar i Mouse Wheel
- ✅ Custom dark theme scrollbar (`ModernScrollbar`)
- ✅ Rekursywne bindowanie mouse wheel - scroll działa wszędzie (nie tylko na marginesach)
- ✅ Periodic check (100ms) do bindowania dynamicznie dodawanych widgetów
- ✅ Nowy plik: `utils/custom_widgets.py`

#### ✅ Alternatywna Metoda w Kroku 1
- ✅ Opcja A: Sitemap URL + filtr (istniejąca)
- ✅ Opcja B: Upload pliku TXT z URL-ami (nowa)
- ✅ Metoda `browse_urls_file()` do wyboru pliku
- ✅ Logika if/elif w `execute_step1()`

#### ✅ Branding i Wizualizacja
- ✅ Fioletowy kolor tytułu (#a855f7 zamiast #f97316)
- ✅ Ikona okna z logo (logo.ico) zamiast piórka Pythona
- ✅ Skrócony tytuł okna: "Nexus Navigation Architect"
- ✅ Lepsze checkboxy z wyraźnym zaznaczeniem (foreground: orange w selected state)

#### 📁 Nowe Pliki
- `utils/custom_widgets.py`: ScrollableFrame, ModernScrollbar, create_modern_checkbox_style
- `assety/logo.ico`: Window icon (32x32, 48x48, 64x64)

---

## [3.0.0] - 2025-01-21

### 🎉 Pełna Przebudowa Aplikacji

#### ✨ Nowe Funkcje

**Interfejs Użytkownika:**
- ✅ Całkowicie nowy interfejs z dark theme (wzorowany na Theme Dark Template)
- ✅ System 3 tabów: Ustawienia, Workflow, Edytor Promptów
- ✅ Logo "Nexus Navigation Architect" (50x50px)
- ✅ Profesjonalny branding i kolorystyka (#f97316 accent orange)
- ✅ Progress bar z determinate progress (% wykonania)
- ✅ Logi w czasie rzeczywistym z kolorowaniem

**Workflow:**
- ✅ Dodano Krok 1: Pobranie listy produktów z sitemap (SitemapParser)
- ✅ Dodano Krok 2: Pobranie opisów produktów (Jina AI Reader)
- ✅ Pełny workflow 1-5 w jednej aplikacji
- ✅ Wizualna indykacja statusu kroków (✅ Wykonane / ⏸️ Do wykonania)
- ✅ Automatyczne wykrywanie wykonanych kroków

**Zarządzanie Projektami:**
- ✅ System folderów projektowych (`projekty/{nazwa}/`)
- ✅ Automatyczne backupy przed nadpisaniem plików
- ✅ Zapisywanie statusu projektu (`project_settings.json`)
- ✅ Wczytywanie/zapisywanie projektów
- ✅ Tworzenie nowych projektów z GUI

**Edytowalne Prompty:**
- ✅ Edytor promptów dla kroków 3, 4, 5
- ✅ Zapisywanie konfiguracji promptów do projektu
- ✅ Wczytywanie konfiguracji promptów z projektu
- ✅ Reset do domyślnych promptów
- ✅ Domyślne prompty w `config/default_prompts.json`

**Architektura:**
- ✅ Modułowa architektura (`utils/` package)
- ✅ `ProjectManager` - zarządzanie projektami
- ✅ `PromptManager` - zarządzanie promptami
- ✅ `OpenRouterClient` - klient API OpenRouter
- ✅ `JinaClient` - klient API Jina Reader
- ✅ `SitemapParser` - parser sitemap XML

**API Integration:**
- ✅ OpenRouter API dla modeli AI (kroki 3-5)
- ✅ Jina AI Reader API dla pobierania treści (krok 2)
- ✅ Wsparcie dla Jina AI API key

**UX Improvements:**
- ✅ Determinate progress bars (% postępu zamiast indeterminate)
- ✅ Callback progress dla każdego kroku
- ✅ Lepsze komunikaty błędów
- ✅ Walidacja zależności między krokami
- ✅ Walidacja API keys przed startem

#### 🔧 Zmiany Techniczne

**Nowe Zależności:**
- `beautifulsoup4>=4.12.0` - parsing XML/HTML (sitemap)
- `lxml>=4.9.0` - parser XML
- `Pillow>=10.0.0` - przetwarzanie obrazków (logo)

**Struktura Plików:**
```
config/
  default_prompts.json       # Domyślne prompty systemowe
utils/
  __init__.py
  project_manager.py         # Zarządzanie projektami
  prompt_manager.py          # Zarządzanie promptami
  openrouter_client.py       # OpenRouter API client
  jina_client.py             # Jina AI API client
  sitemap_parser.py          # Sitemap parser
assety/
  logo.png                   # Oryginalne logo (511x472)
  logo_small.png             # Zmniejszone logo (50x50)
projekty/                    # Foldery projektów
  {nazwa_projektu}/
    products.txt
    content_website.json
    product_extraction.json
    categories_structure.json
    categories_final.json
    prompts_config.json
    project_settings.json
    backups/
```

**Refaktoryzacja:**
- ✅ Wydzielono logikę biznesową do osobnych klas
- ✅ Separation of concerns (GUI vs Logic)
- ✅ Lepsze nazewnictwo zmiennych i funkcji
- ✅ Dokumentacja w kodzie (docstrings)

#### 📚 Dokumentacja

- ✅ `README.md` - kompletna dokumentacja projektu
- ✅ `QUICKSTART.md` - szybki start dla użytkowników
- ✅ `CHANGELOG.md` - historia zmian
- ✅ `CONTEXT_FOR_AI.md` - kontekst dla AI (updated)

#### 🐛 Naprawione Błędy

- ✅ Poprawiono błędy JSON w kroku 5 (regex extraction)
- ✅ Poprawiono problemy z wielowątkowością
- ✅ Poprawiono czyszczenie markdown content
- ✅ Poprawiono obsługę błędów API

#### ⚠️ Breaking Changes

- ❗ Zmiana nazwy aplikacji: "Budowa Kategorii E-commerce" → "Nexus Navigation Architect"
- ❗ Nowa struktura plików - projekty w folderach
- ❗ Wymagane dodatkowe API key (Jina AI) dla kroku 2
- ❗ Nowa architektura - stary kod w `app_old.py`

---

## [2.5.0] - 2025-01-15 (Poprzednia wersja)

### Dodano
- Wybór modeli z combobox dla kroków 3-5
- Automatyczne sugestie modeli
- Dynamiczne pobieranie listy modeli z OpenRouter

### Zmieniono
- Migracja z Gemini API na OpenRouter API

---

## [2.0.0] - 2025-01-10

### Dodano
- Pierwsza wersja desktop (migracja z Google Colab)
- GUI z Tkinter
- Kroki 3-5 workflow

---

## [1.0.0] - 2024-12-15

### Początkowa wersja
- Google Colab notebook
- Wszystkie 5 kroków
- Gemini API

---

## Planowane na przyszłość (TODO)

### Version 3.1
- [ ] Export do CSV/XML
- [ ] Import do PrestaShop/WooCommerce
- [ ] Porównywarka wyników (diff viewer)
- [ ] Statystyki kategorii (liczba, głębokość, etc.)

### Version 3.2
- [ ] Wizualizacja drzewa kategorii
- [ ] Preview kategorii przed zapisem
- [ ] Edycja manualna kategorii
- [ ] Merge kategorii z różnych projektów

### Version 3.3
- [ ] Multi-language support (EN/PL)
- [ ] Własne templates promptów
- [ ] Biblioteka promptów
- [ ] A/B testing promptów

### Version 4.0
- [ ] Web version (FastAPI + React)
- [ ] Cloud storage projektów
- [ ] Współdzielenie projektów
- [ ] API dla integracji

---

**Nexus Navigation Architect** - Professional SEO Category Builder 🚀
