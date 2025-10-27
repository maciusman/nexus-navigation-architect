# 📦 Migration Guide: v2.5 → v3.0

## Dla użytkowników starszych wersji aplikacji

Jeśli używałeś wcześniejszej wersji aplikacji (app_old.py), ten przewodnik pomoże Ci migrować do nowej wersji **Nexus Navigation Architect 3.0**.

---

## 🔄 Co się zmieniło?

### Nazwa Aplikacji
- **Stara:** "Budowa Kategorii E-commerce - SEO 3.0"
- **Nowa:** "Nexus Navigation Architect - SEO Category Builder 3.0"

### Struktura Plików
- **Stara:** Wszystkie pliki w głównym folderze
- **Nowa:** Projekty w osobnych folderach (`projekty/{nazwa}/`)

### Nowe Funkcje
- ✅ Pełny workflow (kroki 1-5) zamiast tylko 3-5
- ✅ System projektów z backupami
- ✅ Edytowalne prompty
- ✅ Dark theme UI
- ✅ Progress bars z % postępu

---

## 📋 Krok po kroku: Migracja danych

### Scenariusz 1: Mam pliki z poprzedniej wersji

Jeśli masz w głównym folderze pliki:
```
product_extraction.json
categories_structure.json
categories_final.json
```

**Kroki:**

1. **Uruchom nową aplikację**
   ```bash
   python app.py
   ```

2. **Tab: Ustawienia**
   - Kliknij "Nowy projekt"
   - Nazwa: `migrated-project` (lub inna)

3. **Skopiuj stare pliki**
   ```bash
   copy product_extraction.json "projekty\migrated-project\"
   copy categories_structure.json "projekty\migrated-project\"
   copy categories_final.json "projekty\migrated-project\"
   ```

4. **Tab: Workflow**
   - Kliknij "Odśwież Status"
   - Kroki 3-5 będą oznaczone ✅ jako wykonane

5. **Gotowe!**
   - Możesz teraz uruchomić dowolny krok ponownie
   - Lub edytować prompty i przetworzyć od nowa

---

### Scenariusz 2: Chcę zachować starą wersję

**Backup starej aplikacji:**
```bash
# Stara aplikacja jest już zabezpieczona jako app_old.py
# Możesz ją uruchomić:
python app_old.py
```

**Używanie obu wersji:**
- **Stara (app_old.py):** Pracuje na plikach w głównym folderze
- **Nowa (app.py):** Pracuje na projektach w `projekty/`

**NIE KONFLIKTUJĄ SIĘ!** Możesz używać obu równocześnie.

---

### Scenariusz 3: Mam wiele projektów (różne sklepy)

**Przed migracją (stary system):**
```
Aplikacje/SEO/
├── app_old.py
├── sklep1_products.txt
├── sklep1_extraction.json
├── sklep1_categories.json
├── sklep2_products.txt
├── sklep2_extraction.json
└── sklep2_categories.json
```

**Po migracji (nowy system):**
```
Aplikacje/SEO/
├── app.py
├── app_old.py (backup)
└── projekty/
    ├── sklep1/
    │   ├── products.txt
    │   ├── product_extraction.json
    │   ├── categories_structure.json
    │   └── categories_final.json
    └── sklep2/
        ├── products.txt
        ├── product_extraction.json
        ├── categories_structure.json
        └── categories_final.json
```

**Kroki:**

1. Utwórz projekty:
   ```bash
   mkdir "projekty\sklep1"
   mkdir "projekty\sklep2"
   ```

2. Skopiuj pliki:
   ```bash
   copy sklep1_products.txt "projekty\sklep1\products.txt"
   copy sklep1_extraction.json "projekty\sklep1\product_extraction.json"
   # etc.
   ```

3. W aplikacji:
   - **Wybierz** folder `projekty\sklep1`
   - Status kroków zaktualizuje się automatycznie

---

## 🔑 Nowe Wymagania API

### Stara wersja:
- ✅ OpenRouter API Key (dla kroków 3-5)

### Nowa wersja:
- ✅ OpenRouter API Key (dla kroków 3-5)
- ⭐ **Jina AI API Key** (dla kroku 2) - **NOWE!**

**Gdzie uzyskać Jina AI Key:**
1. https://jina.ai/reader
2. Zarejestruj się (FREE tier)
3. Skopiuj API key

**Uwaga:** Jeśli nie planujesz używać kroku 2, Jina AI key nie jest wymagany.

---

## 🎨 Nowy Interfejs

### Stary interfejs:
- Jeden długi formularz
- Tylko kroki 3-5
- Brak systemu projektów

### Nowy interfejs:
- **Tab 1: Ustawienia** - API keys, projekty
- **Tab 2: Workflow** - wszystkie 5 kroków
- **Tab 3: Edytor Promptów** - edycja promptów

**Nauka nowego UI:** ~5 minut (jest intuicyjny!)

---

## 📝 Edytowalne Prompty - Nowa Funkcja!

### Co to daje?

**Przed (stara wersja):**
- Prompty na sztywno w kodzie
- Zmiana = edycja kodu Python

**Teraz (nowa wersja):**
- Tab "Edytor Promptów"
- Edycja bez kodowania
- Zapisywanie własnych konfiguracji

### Przykład użycia:

1. Tab "Edytor Promptów"
2. Wybierz "Krok 5: Finalizacja"
3. Dodaj do promptu:
   ```
   IMPORTANT: Focus on brand names in category structure.
   Ensure each brand has its own subcategory.
   ```
4. Zapisz konfigurację (💾)
5. Uruchom krok 5 ponownie

**Wynik:** Struktura kategorii z podziałem na marki!

---

## ⚠️ Potencjalne Problemy

### Problem 1: "ModuleNotFoundError: No module named 'utils'"

**Rozwiązanie:**
```bash
# Upewnij się że jesteś w odpowiednim folderze
cd "x:\Aplikacje\SEO - 3.0 - Budowa kategorii ecommerce"
python app.py
```

### Problem 2: "No module named 'PIL'"

**Rozwiązanie:**
```bash
pip install -r requirements.txt
```

### Problem 3: "File does not exist: config/default_prompts.json"

**Rozwiązanie:**
- Sprawdź czy folder `config/` istnieje
- Sprawdź czy plik `default_prompts.json` jest w `config/`
- Jeśli brak, pobierz ponownie projekt

### Problem 4: Stara aplikacja nie działa

**Rozwiązanie:**
```bash
# Stara aplikacja jest w app_old.py
python app_old.py
```

---

## 🆕 Nowe Możliwości

### 1. Krok 1: Sitemap Parser

**Użycie:**
- Podaj URL sitemap
- Ustaw filtr (np. `.html`)
- Automatyczne pobranie listy produktów

**Korzyści:**
- Nie musisz ręcznie tworzyć `products.txt`
- Automatyczna filtracja URL-i

### 2. Krok 2: Jina Reader

**Użycie:**
- Automatyczne pobieranie treści ze stron
- Konwersja HTML → Markdown
- Multi-threading (szybkie!)

**Korzyści:**
- Nie musisz ręcznie tworzyć `content_website.json`
- Oszczędność czasu

### 3. Backupy

**Automatyczne backupy przed nadpisaniem:**
```
projekty/moj-sklep/backups/
├── product_extraction_20250121_143052.json
├── categories_structure_20250121_145123.json
└── categories_final_20250121_150230.json
```

**Korzyści:**
- Bezpieczeństwo danych
- Porównywanie wersji
- Testowanie różnych modeli

### 4. Projekty

**Organizacja:**
```
projekty/
├── sklep-electronics/
├── sklep-fashion/
└── sklep-home/
```

**Korzyści:**
- Łatwe przełączanie między projektami
- Brak konfliktów
- Osobne konfiguracje promptów

---

## 🎓 Polecane workflow dla migrujących

### Jeśli już masz wyniki z kroków 3-5:

1. **Migruj dane** (jak wyżej)
2. **Wypróbuj edytor promptów:**
   - Edytuj prompt kroku 5
   - Uruchom krok 5 ponownie
   - Porównaj wyniki z backupem
3. **Testuj różne modele:**
   - o1-mini vs QwQ vs DeepSeek
   - Porównaj jakość
   - Wybierz najlepszy

### Jeśli zaczynasz nowy projekt:

1. **Użyj pełnego workflow (kroki 1-5)**
2. **Skonfiguruj prompty** przed uruchomieniem
3. **Zapisz konfigurację** w projekcie
4. **Reuse** dla podobnych projektów

---

## 📞 Potrzebujesz pomocy?

1. **Przeczytaj** `README.md` - pełna dokumentacja
2. **Przeczytaj** `QUICKSTART.md` - szybki start
3. **Sprawdź logi** - aplikacja pokazuje szczegółowe błędy
4. **Stara wersja** - zawsze możesz wrócić do `app_old.py`

---

## ✅ Checklist Migracji

- [ ] Zainstalowałem nowe zależności (`pip install -r requirements.txt`)
- [ ] Uzyskałem Jina AI API key (jeśli planuję używać kroku 2)
- [ ] Utworzyłem nowy projekt
- [ ] Skopiowałem stare pliki do folderu projektu
- [ ] Odświeżyłem status kroków
- [ ] Przetestowałem uruchomienie
- [ ] Stworzyłem backup starych danych
- [ ] Przeczytałem README.md i QUICKSTART.md

---

**Gratulacje! Jesteś gotowy do używania Nexus Navigation Architect 3.0! 🎉**

*Happy Building!* 🚀
