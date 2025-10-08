# nødvendige importeringer
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
# Hent API-nøkkel og Vector Store ID fra miljøvariabler
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

# Initialiser OpenAI-klienten
client = OpenAI(api_key=OPENAI_API_KEY)

# Definer verktøyene som skal brukes i chatten
tools = [
    {
        "type": "function",
        "name": "refund_instructions",
        "description": "Provides customers with information about how to request a refund based on vector store data.",
        "parameters": {
            "type": "object",
            "properties": {
                "info_from_docs": {
                    "type": "string",
                    "description": "Relevant guidance text retrieved from the vector store about how to request a refund."
                }
            },
            "required": ["info_from_docs"]
        }
    },
    {
        "type": "file_search",
        "vector_store_ids": [VECTOR_STORE_ID]
    }, 
]

# Funksjon for å gi refusjonsinstruksjoner
def refund_instructions(info_from_docs):
    """
    info_from_docs: tekst hentet fra vector store om hvordan man gjennomfører refusjon
    """
    return {
        "instructions": f"Her er veiledningen hentet fra vector store:\n\n{info_from_docs}\n\n"
                        "Merk: Dette er kun informasjon. Ingen refusjon er gjennomført."
    }


# Hovedfunksjon for chat med GPT
def chat_with_gpt():
    # setter response_ID til None ved start
    response_ID = None

    # starter en løkke for kontinuerlig chat
    while True: 
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]: 
            break
        # sender brukerinput til GPT-modellen
        response = client.responses.create(
            model="gpt-4.1", 
            input= user_input,
            previous_response_id=response_ID,
            instructions= """ 
            Du er en hjelpsom kundeserviceassistent.
            Hvis brukeren spør om refusjoner eller angrerett:
                1. Bruk file_search for å hente relevant informasjon fra vector store.
                2. Send den hentede teksten som 'info_from_docs' til refund_instructions.
                3. Presentér deretter resultatet for brukeren.
            Hvis spørsmålet ikke handler om refusjon, svar som vanlig.
""",
            tools=tools  
           
        )
        # oppdaterer response_ID for å spore samtalen
        response_ID = response.id
        # printer svaret fra boten
        print("Bot:", response.output_text)

        # sjekker om det er noen funksjonskall i svaret
        while any(item.type == "function_call" for item in response.output): 
            # initialiserer en tom liste for input til neste kall
            input_list = []
            # går gjennom alle elementene i svaret
            for item in response.output: 
                # sjekker om elementet er et funksjonskall
                if item.type == "function_call": 
                    # printer ut funksjonsnavnet som kalles
                    print(f"--> kaller funksjon: {item.name}")

                    # sjekker hvilket funksjonsnavn som kalles
                    if item.name == "refund_instructions":
                        # henter argumenter og kaller funksjonen
                        try: 
                            # parserer argumentene fra JSON-streng
                            arguments = json.loads(item.arguments)
                            # henter info_from_docs argumentet
                            info_from_docs = arguments.get("info_from_docs", "Ingen innformasjon funnet.")
                            # definerer en variabel med verdien fra funksjonskallet
                            result = refund_instructions(info_from_docs)

                        # håndterer feil ved parsing av JSON    
                        except json.JSONDecodeError as e:
                            result = {"error": f"Feil ved parsing av argumenter: {str(e)}"}

                        # legger til funksjonskallresultatet i input_list for neste GPT-kall
                        input_list.append({
                            "type": "function_call_output", 
                            "call_id": item.call_id, 
                            "output": json.dumps(result)
                        })
                        # oppretter en response med resultatet fra funksjonskallet
                        response = client.responses.create(
                            model="gpt-4.1",
                            input=input_list,
                            previous_response_id=response_ID,
                            tools=tools
                        )
                        # oppdaterer response_ID for å spore samtalen
                        response_ID = response.id
                        # printer svaret fra boten
                        print("Bot:", response.output_text)

# kjører chat-funksjonen
chat_with_gpt()

