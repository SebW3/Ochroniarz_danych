from logins import OpenAI_key  # ta funkcja zwraca klucz do API
from openai import OpenAI
import os

def ochrona(user_message):
    def check_edge_case(item):
        if len(item) < 2 or "n/a" in item:  # edge case
            return True

    os.environ["OPENAI_API_KEY"] = OpenAI_key()
    client = OpenAI()

    # prompt, który zwróci listę danych wrażliwych
    system_message = "Twoją odpowiedzią będzie wypisanie listy danych osobowych takich jak imię, nazwisko, adres itp. Jeśli w tekście wykryto mowę nienawiści, groźby, zastraszanie lub inne zakazane czynności to napisz 'Tak' po 'Nieodpowiednie treści: '. Każdy z osobnych punktów pisz w nowe linijce. Jeżeli nie będzie żadnych danych do wypisania to napisz 'n/a'. Przepisuj informacje z tekstu bez żadnych modyfikacji\nFormat przykładowej odpowiedzi:\nImię: Jan\nNazwisko: Kowalski"
    system_message = "Twoją odpowiedzią będzie wypisanie listy danych osobowych takich jak imię, nazwisko, adres itp. Jeśli w tekście wykryto mowę nienawiści, groźby, zastraszanie lub inne zakazane czynności to napisz 'Tak' lub 'Nie' po 'Nieodpowiednie treści: '. Każdy z osobnych punktów pisz w nowe linijce. Jeżeli nie będzie żadnych danych do wypisania to napisz 'n/a'. Przepisuj informacje z tekstu bez żadnych modyfikacji a jeśli jest kilka informacji do tej samej kategorii to wypisz je wszystkie. Nie odmieniaj wyrazów tylko je wypisz\nFormat przykładowej odpowiedzi:\nImię: Jan\nNazwisko: Kowalski"
    # przykładowy tekst
    #user_message = "John Smith, urodzony 15 lipca 1985 roku w Nowym Jorku, mieszka na ulicy Maple Avenue 123. Jego numer telefonu to 555-123-4567, a adres e-mail to john.smith@example.com. Wczoraj wieczorem spotkał się z kolegami i zbyt wiele wypił, co skończyło się awanturą. John zachował się bardzo agresywnie i obraźliwie wobec innych osób, co jest niedopuszczalne. W wyniku incydentu został zatrzymany przez policję."

    messages = [{"role": "system", "content": system_message},
                {"role": "user", "content": user_message}, ]

    completion = client.chat.completions.create(messages=messages, model="gpt-3.5-turbo", temperature=0)
    answer = completion.choices[0].message.content

    # odpowiedź od LLM z przykładu
    #answer = "Imię: John\nNazwisko: Smith\nData urodzenia: 15 lipca 1985\nMiejsce urodzenia: Nowy Jork\nAdres zamieszkania: ul. Maple Avenue 123\nNumer telefonu: 555-123-4567\nAdres e-mail: john.smith@example.com\nNieodpowiednie treści: Tak"

    lista_danych = answer.split("\n")

    for i in range(len((lista_danych))):
        if "Inne: Nieodpowiednie treści:" in lista_danych[i]:
            lista_danych[i] = lista_danych[i].replace("Inne: ", "")
        if ("adres" in lista_danych[i].lower()) and ("ul." in lista_danych[i]):
            lista_danych[i] = lista_danych[i].replace("ul.", "").strip()
        else:
            pass

    # zamiana danych wrażliwych na anonimowe
    zmiana_danych = []
    przetworzony_tekst = user_message

    for item in lista_danych:
        dane_wrazliwe = item.split(":")

        if check_edge_case(item):
            continue
        kategoria = dane_wrazliwe[0].strip()
        dane = dane_wrazliwe[1].strip()
        print(dane)
        if "," in dane:  # jeżeli dane zawierają kilka elementów to trzeba je wszystkie zamienić
            temp = dane.split(",")
            for dana in temp:
                przetworzony_tekst = przetworzony_tekst.replace(dana, f"[{kategoria.upper()}]")

        zmiana_danych.append((kategoria, dane))
        przetworzony_tekst = przetworzony_tekst.replace(dane, f"[{kategoria.upper()}]")

    for item in zmiana_danych:
        if "Nieodpowiednie treści" in item and item[1] == "Tak":
            print("W tekście znajdują się nieodpowiednie treści")
            break

    if len(zmiana_danych) > 1:
        print("Tekst zawiera dane wrażliwe")
    elif len(zmiana_danych) == 1:
        for item in zmiana_danych:
            if "Nieodpowiednie treści" not in item:
                print("Tekst zawiera dane wrażliwe")

    return zmiana_danych, user_message, przetworzony_tekst
