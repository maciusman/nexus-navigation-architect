# Instrukcja Uruchomienia - Budowa Kategorii E-commerce SEO 3.0 (OpenRouter)

## Co ta aplikacja robi?

Aplikacja automatycznie buduje strukturę kategorii dla sklepu e-commerce na podstawie opisów produktów. Proces składa się z 5 kroków:

1. ✅ Pobranie listy produktów z sitemap (WYKONANE - plik `products.txt`)
2. ✅ Pobranie opisów produktów (WYKONANE - plik `content_website.json`)
3. 🔄 Ekstrakcja parametrów z opisów produktów (DO WYKONANIA)
4. 🔄 Budowa wstępnej struktury kategorii (DO WYKONANIA)
5. 🔄 Finalizacja i optymalizacja kategorii (DO WYKONANIA)

## Wymagania

- Python 3.8 lub nowszy
- Klucz API OpenRouter

## Krok 1: Instalacja Pythona

### Jeśli nie masz Pythona:

1. Wejdź na: https://www.python.org/downloads/
2. Pobierz najnowszą wersję Pythona (3.11 lub nowszą)
3. **WAŻNE**: Podczas instalacji zaznacz opcję "Add Python to PATH"
4. Kliknij "Install Now"

### Sprawdź czy Python jest zainstalowany:

1. Otwórz Terminal/Wiersz polecenia (Windows: naciśnij `Win + R`, wpisz `cmd`, naciśnij Enter)
2. Wpisz: `python --version`
3. Powinieneś zobaczyć wersję Pythona (np. "Python 3.11.5")

## Krok 2: Uzyskanie klucza API OpenRouter

1. Wejdź na: https://openrouter.ai/keys
2. Zaloguj się (możesz użyć konta Google, GitHub lub email)
3. Kliknij "Create Key"
4. Opcjonalnie: Ustaw nazwę klucza i limit kredytów
5. Skopiuj wygenerowany klucz (będzie potrzebny w aplikacji)

**WAŻNE**: OpenRouter to płatna usługa, ale daje dostęp do wszystkich modeli AI (OpenAI, Anthropic, Google, Meta, etc.) bez limitów darmowych API. Koszt jest bardzo niski - płacisz tylko za to, co używasz.

## Krok 3: Instalacja wymaganych bibliotek

1. Otwórz Terminal/Wiersz polecenia
2. Przejdź do folderu z aplikacją:
   ```
   cd "x:\Aplikacje\SEO - 3.0 - Budowa kategorii ecommerce"
   ```

3. Zainstaluj wymagane biblioteki:
   ```
   pip install -r requirements.txt
   ```

## Krok 4: Uruchomienie aplikacji

1. W tym samym oknie terminala wpisz:
   ```
   python app.py
   ```

2. Otworzy się okno aplikacji

## Krok 5: Użycie aplikacji

### Interfejs aplikacji zawiera:

1. **Pole "OpenRouter API Key"**:
   - Wklej tutaj swój klucz API OpenRouter
   - Kliknij "Załaduj modele" aby pobrać listę wszystkich dostępnych modeli

2. **Wybór Modeli dla Każdego Kroku**:
   - **Krok 3 - Ekstrakcja parametrów**: Wybierz model (💡 zalecane: szybkie/tanie modele jak Gemini Flash, GPT-4o-mini)
   - **Krok 4 - Budowa struktury**: Wybierz model (💡 zalecane: szybkie modele)
   - **Krok 5 - Finalizacja**: Wybierz model (💡 zalecane: modele reasoning jak o1, QwQ, DeepSeek)

3. **Ustawienia**:
   - **Wątki ekstrakcji**: Ilość równoległych zapytań (1-30, domyślnie 1)
   - **Powtórzenia (ekstrakcja)**: Ile razy powtórzyć w razie błędu (1-5, domyślnie 4)
   - **Rozmiar paczki**: Ile produktów przetwarzać jednocześnie (10-100, domyślnie 100)
   - **Wątki (batch)**: Wątki dla przetwarzania paczek (1-10, domyślnie 10)

4. **Przyciski**:
   - **Start Przetwarzania**: Rozpoczyna automatyczny proces
   - **Stop**: Zatrzymuje przetwarzanie
   - **Otwórz wynik**: Otwiera plik z wynikiem

5. **Okno logów**: Pokazuje postęp przetwarzania

### Proces przetwarzania:

1. Wprowadź klucz API OpenRouter
2. Kliknij "Załaduj modele" - aplikacja pobierze aktualną listę wszystkich dostępnych modeli
3. Wybierz modele dla każdego kroku (aplikacja automatycznie zasugeruje odpowiednie)
4. (Opcjonalnie) Dostosuj ustawienia
5. Kliknij "Start Przetwarzania"
6. Aplikacja wykona automatycznie kroki 3-5:
   - Wyekstrahuje parametry z każdego produktu
   - Zbuduje wstępną strukturę kategorii
   - Zoptymalizuje i sfinalizuje strukturę

7. Po zakończeniu zobaczysz komunikat "Proces zakończony!"

## Pliki wynikowe

Aplikacja tworzy następujące pliki:

- `product_extraction.json` - Wyekstrahowane parametry produktów (Krok 3)
- `categories_structure.json` - Wstępna struktura kategorii (Krok 4)
- `categories_final.json` - **FINALNA STRUKTURA KATEGORII** (Krok 5) ⭐

## Uwagi i rozwiązywanie problemów

### Problem: "Python nie jest rozpoznawany jako polecenie"
**Rozwiązanie**: Python nie został dodany do PATH. Przeinstaluj Pythona zaznaczając "Add Python to PATH"

### Problem: "Błąd API - Invalid API Key"
**Rozwiązanie**: Sprawdź czy klucz API jest poprawny. Skopiuj go ponownie z https://openrouter.ai/keys

### Problem: "Nie udało się załadować modeli"
**Rozwiązanie**:
- Sprawdź klucz API
- Sprawdź połączenie internetowe
- Upewnij się, że masz środki na koncie OpenRouter

### Problem: Aplikacja się zawiesza
**Rozwiązanie**:
- Zmniejsz liczbę wątków do 1
- Sprawdź połączenie internetowe
- Sprawdź saldo konta OpenRouter

### Problem: "Brak pliku content_website.json"
**Rozwiązanie**: Upewnij się, że plik `content_website.json` znajduje się w tym samym folderze co `app.py`

## Wsparcie techniczne

Jeśli masz problemy:
1. Przeczytaj logi w aplikacji - często wskazują na przyczynę problemu
2. Sprawdź czy wszystkie pliki są w odpowiednim folderze
3. Upewnij się, że masz aktywne połączenie internetowe
4. Sprawdź czy klucz API OpenRouter jest aktywny i ma środki

## Dodatkowe informacje

- Proces może zająć od kilku minut do kilkudziesięciu minut w zależności od liczby produktów
- Aplikacja zapisuje wyniki na bieżąco - możesz ją bezpiecznie zamknąć i wznowić później
- Im więcej wątków, tym szybsze przetwarzanie, ale większy koszt API
- Rekomendowane ustawienia dla dużych katalogów:
  - Wątki ekstrakcji: 1-5
  - Rozmiar paczki: 50-100
  - Wątki batch: 5-10

## Modele AI dostępne

**Aplikacja używa OpenRouter** - masz dostęp do wszystkich modeli:
- **Szybkie/tanie**: Gemini Flash, GPT-4o-mini, Claude Haiku
- **Zaawansowane**: GPT-4o, Claude Sonnet, Gemini Pro
- **Reasoning**: OpenAI o1/o1-mini, Qwen QwQ, DeepSeek-R1

Aplikacja automatycznie pobiera aktualną listę modeli i sugeruje odpowiednie dla każdego kroku.

## Zalety OpenRouter

✅ **Jeden klucz API** - dostęp do wszystkich dostawców (OpenAI, Anthropic, Google, Meta, etc.)
✅ **Brak limitów** - płatne, ale bez ograniczeń darmowych API
✅ **Niskie koszty** - płacisz tylko za użycie, często taniej niż bezpośrednio u dostawcy
✅ **Aktualne modele** - zawsze masz dostęp do najnowszych modeli
✅ **Pełna kontrola** - wybierasz dokładnie który model dla którego zadania
