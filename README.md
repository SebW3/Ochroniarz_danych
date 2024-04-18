# Ochroniarz_danych
Aplikacja, która zwraca informację, że wprowadzony tekst może zawierać wrażliwe dane. Poinformuje też czy w tekście znajdują się jakieś nieodpowiednie treści takie jak mowa nienawiści, groźby, zastraszanie i inne niedozwolone czynności

#### Wymagane biblioteki
- openai
- pyqt5

### Uruchamianie
1. Zainstalować wymagane biblioteki
2. Uruchomić "GUI.py"
3. Wpisać tekst do sprawdzenia w lewe górne pole tekstowe
4. Nacisnąć przycisk "Sprawdź"

## Opis działania
### Ochroniarz.py
#### ochrona(user_message)
To jest główna funkcja programu, która przetwarza wiadomość użytkownika i zwraca trzy wartości:
- listę tupli zawierającą dane wrażliwe i ich kategorie
- oryginalną wiadomość
- oryginalną wiadomość z zastąpionymi danymi

#### Proces działania
Funkcja pobiera tekst, który ma przetworzyć w celu znalezienia danych wrażliwych i czy tekst zawiera nieodpowiednie treści
1. Tekst jest wysyłany do API OpenAI wraz z odpowiednim zapytaniem. Zwracana jest lista zawierające kategorie i odpowiadające im dane wrażliwe. Jest też zwracana informacja o nieodpowiednich treściach
2. Usuwanie edge case
3. Model nie zawsze zwraca poprawne odpowiedzi czy występują nieodpowiednie treści więc odpowiedź i/lub tekst jest ponownie przetwarzany w celu sprawdzenia poprawności
4. Wyświetlana jest wiadomość czy treść zawiera dane wrażliwe i nieodpowiednie treści
<br>

Przy każdorazowym sprawdzeniu tekstu aplikacja wyśle 1-3 zapytania

### GUI.py
Jest to interfejs dla łatwego korzystania z wyżej wymienionej funkcji.<br>
Po uruchomieniu pliku pojawi się okno z trzema polami tekstowymi i dwoma przyciskami. W pole "Wpisz tekst" należy podać tekst, który ma zostać sprawdzony. Naciśnięcie przycisku <b>"Sprawdź"</b> uruchomi funkcję ochrona(user_message) z pliku Ochroniarz.py co spowoduje sprawdzenie podanego tekstu. Wszystkie informacje, które znalazł, zostaną wyświetlone w tabelce po prawej stronie. W dolnym polu tekstowym będzie wprowadzony tekst, ale ze zmienionymi danymi na anonimowe. Można zmieniać z anonimowych na rzeczywiste i z powrotem za pomocą przycisku <b>"Konwersja"</b>
1. Wpisz tekst
2. Naciśnij przycisk <b>"Sprawdź"</b>

### Limity
##### Wykrywanie nieodpowiednich treści
Model jest przewrażliwiony i uznaje za dużo rzeczy za nieodpowiednie treści dlatego jest funkcja "double_check()", która sprawdza, czy to, co wykrył jest zgodne z tekstem czy nie Zazwyczaj będzie poprawnie zwracał informację o występowaniu tych treści

##### Zdrobnienia i odmiany
Model nie zawsze wypisuje wszystkich odmian imion, przez co zamiana tekstu na anonimowy nie jest możliwa, ponieważ używam do tego funkcji .replace() Czasami wypisuje wersję słowa bez odmiany a w tekście jest odmieniona

##### Precyzja
Im dłuższy tekst, tym mniejsza precyzja programu
