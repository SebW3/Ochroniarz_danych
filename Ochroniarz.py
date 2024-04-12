from logins import OpenAI_key
from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = OpenAI_key()
client = OpenAI()

system_message = "Twoją odpowiedzią będzie wypisanie listy danych osobowych takich jak imię, nazwisko, adres itp. Jeśli w tekście wykryto mowę nienawiści, groźby, zastraszanie lub inne zakazane czynności to przepisz ją po 'Nieodpowiednie treści: ', jeśli jest kilka elementów to oddziel je średnikami. Każdy z osobnych punktów pisz w nowe linijce"
# TODO zmienić format w jakim zwraca info o mowie nienawiści

# temporary for testing
user_message = "Jestem Grzegorz Brzęczyszczykiewicz. Lubię pić piwo. Stoły są robione z drewna. Nienawidzę psów! Zjadłbym kebsa. Skrzywdzę wszystkich wegetarian. Mam konto w banku i jego numer to 666 6969 000"

user_message = "John Smith, urodzony 15 lipca 1985 roku w Nowym Jorku, mieszka na ulicy Maple Avenue 123. Jego numer telefonu to 555-123-4567, a adres e-mail to john.smith@example.com. Wczoraj wieczorem spotkał się z kolegami i zbyt wiele wypił, co skończyło się awanturą. John zachował się bardzo agresywnie i obraźliwie wobec innych osób, co jest niedopuszczalne. W wyniku incydentu został zatrzymany przez policję."

messages = [ {"role": "system", "content": system_message},
             {"role": "user", "content": user_message}, ]


# completion = client.chat.completions.create(messages=messages, model="gpt-3.5-turbo", temperature=0)
# print(completion.choices[0].message.content)
# answer = completion.choices[0].message.content
#
print(user_message)
answer = "Imię: John\nNazwisko: Smith\nData urodzenia: 15 lipca 1985\nMiejsce urodzenia: Nowy Jork\nAdres: Maple Avenue 123\nNumer telefonu: 555-123-4567\nAdres e-mail: john.smith@example.com\n\nNieodpowiednie treści: Zachowanie agresywne i obraźliwe wobec innych osób; Zatrzymanie przez policję"
print(answer)
lista_danych = answer.split("\n")
print(lista_danych)
for item in lista_danych:
    dane_wrazliwe = item.split(":")
    if len(dane_wrazliwe) < 2:  # egde case
        continue
    kategoria = dane_wrazliwe[0].strip()
    dane = dane_wrazliwe[1].strip()
    user_message = user_message.replace(dane, f"[{kategoria.upper()}]")
print(user_message)