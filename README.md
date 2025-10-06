# Fartebot – Vector Store Chatbot

[![Project Status](https://img.shields.io/badge/status-experimental-orange)]()
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Dette prosjektet er et tidlig utkast til **Fartebot**, en chatbot som er koblet opp mot en **Vector Store**.  
Målet er å utforske hvordan boten fungerer med utvalgte datasett og spesifikke funksjonskall som gir mer fokuserte svar.

---

## 📑 Innholdsfortegnelse
- [Om prosjektet](#-om-prosjektet)
- [Funksjonskall](#-funksjonskall)
- [Sikkerhet og personvern](#-sikkerhet-og-personvern)
- [Installasjon og oppsett](#-installasjon-og-oppsett)
- [Anbefalt Python-versjon](#-anbefalt-python-versjon)
- [Lisens](#-lisens)

---

## 💡 Om prosjektet
Fartebot er utviklet som en utforskningsplattform for å teste:
- Hvordan chatboten integreres med en Vector Store.
- Hvordan den responderer på spørsmål basert på spesifikke datasett.
- Hvordan funksjonskall kan brukes for mer målrettede svar.

Dette er et eksperimentelt prosjekt og er fortsatt under utvikling.

---

## ⚙️ Funksjonskall
Prosjektet har foreløpig ett hovedfunksjonskall:
- **Refusjon**: Dersom brukeren stiller spørsmål relatert til refusjon, vil boten benytte det tilpassede funksjonskallet for å levere mer presise svar.

---

## 🔒 Sikkerhet og personvern
Dette prosjektet samler **ikke** inn personopplysninger under vanlig bruk.  

⚠️ Viktig:
- Chatboten bruker **OpenAI sin språkmodell**.
- Ikke del sensitiv eller personlig informasjon når du tester prosjektet.

---

## ⚙️ Installasjon og oppsett

### Forutsetninger
- En gyldig **OpenAI API-nøkkel**.
- Python installert (se [anbefalt Python-versjon](#-anbefalt-python-versjon)).
- Et virtuelt Python-miljø anbefales.

### Installasjon
1. Klon repoet:
   ```bash
   git clone https://github.com/<brukernavn>/<repo-navn>.git
   cd <repo-navn>
