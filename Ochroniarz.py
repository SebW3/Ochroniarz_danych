from logins import OpenAI_key
from openai import OpenAI
import os

def check_edge_case(item):
    if len(item) < 2 or "n/a" in item:  # egde case
        print("pominięto", item)
        return True

os.environ["OPENAI_API_KEY"] = OpenAI_key()
client = OpenAI()

system_message = "Twoją odpowiedzią będzie wypisanie listy danych osobowych takich jak imię, nazwisko, adres itp. Jeśli w tekście wykryto mowę nienawiści, groźby, zastraszanie lub inne zakazane czynności to napisz 'Tak' po 'Nieodpowiednie treści: '. Każdy z osobnych punktów pisz w nowe linijce. Przepisuj informacje z tekstu bez żadnych modyfikacji\nFormat przykładowej odpowiedzi:\nImię: Jan\nNazwisko: Kowalski"
system_message = "Twoją odpowiedzią będzie wypisanie listy danych osobowych takich jak imię, nazwisko, adres itp. Jeśli w tekście wykryto mowę nienawiści, groźby, zastraszanie lub inne zakazane czynności to napisz 'Tak' po 'Nieodpowiednie treści: '. Każdy z osobnych punktów pisz w nowe linijce. Jeżeli nie będzie żadnych danych do wypisania to napisz 'n/a'. Przepisuj informacje z tekstu bez żadnych modyfikacji\nFormat przykładowej odpowiedzi:\nImię: Jan\nNazwisko: Kowalski"
# temporary for testing
user_message = "Jestem Grzegorz Brzęczyszczykiewicz. Lubię pić piwo. Stoły są robione z drewna. Nienawidzę psów! Zjadłbym kebsa. Skrzywdzę wszystkich wegetarian. Mam konto w banku i jego numer to 666 6969 000"
user_message = "John Smith, urodzony 15 lipca 1985 roku w Nowym Jorku, mieszka na ulicy Maple Avenue 123. Jego numer telefonu to 555-123-4567, a adres e-mail to john.smith@example.com. Wczoraj wieczorem spotkał się z kolegami i zbyt wiele wypił, co skończyło się awanturą. John zachował się bardzo agresywnie i obraźliwie wobec innych osób, co jest niedopuszczalne. W wyniku incydentu został zatrzymany przez policję."
user_message = "Lubię koty. Natura jest piękna i lubię oddychać świeżym powietrzem. Nienawidzę ludzi"

messages = [ {"role": "system", "content": system_message},
             {"role": "user", "content": user_message}, ]

completion = client.chat.completions.create(messages=messages, model="gpt-3.5-turbo", temperature=0)
answer = completion.choices[0].message.content

print(user_message)
#answer = "Imię: John\nNazwisko: Smith\nData urodzenia: 15 lipca 1985\nMiejsce urodzenia: Nowy Jork\nAdres zamieszkania: ul. Maple Avenue 123\nNumer telefonu: 555-123-4567\nAdres e-mail: john.smith@example.com\nNieodpowiednie treści: Tak"
#answer = "n/a"
print(answer)
lista_danych = answer.split("\n")
print(lista_danych)
for item in lista_danych:
    if "Inne: Nieodpowiednie treści:" in item:
        item = item.replace("Inne: ", "")
        print("replaced", item)
zmiana_danych = []
for item in lista_danych:
    dane_wrazliwe = item.split(":")

    if check_edge_case(item):
        continue
    kategoria = dane_wrazliwe[0].strip()
    dane = dane_wrazliwe[1].strip()
    zmiana_danych.append((kategoria, dane))
    user_message = user_message.replace(dane, f"[{kategoria.upper()}]")
print(user_message)

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

print(zmiana_danych)