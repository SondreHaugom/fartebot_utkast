from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")


client = OpenAI(api_key=OPENAI_API_KEY)


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

def refund_instructions(info_from_docs):
    """
    info_from_docs: tekst hentet fra vector store om hvordan man gjennomfører refusjon
    """
    return {
        "instructions": f"Her er veiledningen hentet fra vector store:\n\n{info_from_docs}\n\n"
                        "Merk: Dette er kun informasjon. Ingen refusjon er gjennomført."
    }



def chat_with_gpt():
    response_ID = None

    while True: 
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]: 
            break
        response = client.responses.create(
            model="gpt-4.1", 
            input= user_input,
            previous_response_id=response_ID,
            instructions= " Du er en hjelpsom kundeserviceassistent. Bruk tilgjengelige verktøy for å hjelpe kunden med deres forespørsel. Hvis du trenger informasjon om refusjonsprosessen, bruk 'refund_instructions' funksjonen.",
            tools=tools  
           
        )
        response_ID = response.id
        print("Bot:", response.output_text)

        while any(item.type == "function_call" for item in response.output): 

            input_list = []

            for item in response.output: 
                if item.type == "function_call": 
                    print(f"--> kaller funksjon: {item.name}")

                    if item.name == "refund_instructions":
                        try: 
                            arguments = json.loads(item.arguments)

                            info_from_docs = arguments.get("info_from_docs", "Ingen innformasjon funnet.")

                            result = refund_instructions(info_from_docs)

                        except json.JSONDecodeError as e:
                            result = {"error": f"Feil ved parsing av argumenter: {str(e)}"}

                        input_list.append({
                            "type": "function_call_output", 
                            "call_id": item.call_id, 
                            "output": json.dumps(result)
                        })

                        response = client.responses.create(
                            model="gpt-4.1", 
                            input= input_list, 
                            previous_response_id=response_ID,   
                            tools=tools
                        )
                        response_ID = response.id
                        print("Bot:", response.output_text)


chat_with_gpt()

