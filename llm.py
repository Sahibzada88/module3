import os
import logging
from openai_service import call_open_ai
from chromadb_service import retriver
from dotenv import load_dotenv
from mongo_service import save_chat, fetch_data
import shutil


load_dotenv()

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.FileHandler("hacking_bot.log"),  # Save logs to a file
        logging.StreamHandler()  # Also print logs to console
    ]
)

PROMPT = """You are Hacking bot and you have to give detailed knowledge about the questions asked about hacking
either ethical or unethical and all of its techniques like phishing attack, pentesting, social engineering.
You should only answer about ethical hacking and unethical hacking. You have previous question knowledge use it too.
If an off-topic question is asked, you should answer 'I can't answer topic-unrelated questions.' """

def hacking_bot(question, user_id):
    logging.info("Received question: %s", question)  # Log the received question

    try:
        # Retrieve similar documents
        texts = []
        docs = retriver(question)
        logging.info("Retrieved %d documents for the question", len(docs))

        for i in docs:
            texts.append(i.page_content)
        
        # Concatenate documents
        VECTOR_DB_DATA = ""
        for i in texts:
            VECTOR_DB_DATA += i
            VECTOR_DB_DATA += "/n"
        
        clean_messages = []
        data_from_db = fetch_data(user_id)
        if len(data_from_db) > 0:
            for i in data_from_db:
                clean_messages.append(
                    {
                        "role":i['role'],
                        "content":i['content']
                    }
                )

        save_chat(
            {
                "user_id": user_id,
                "role":"user",
                "content":question
            }
            )
        # Prepare message for OpenAI API
        message = [
            {
                "role": "system",
                "content": PROMPT
            },
            {
                "role": "system",
                "content": f"Use this data to answer {VECTOR_DB_DATA}"
            },
        ]
        message.extend(clean_messages)
        message.append(
            {
                "role": "user",
                "content": question
            }
        )
        
        # Call OpenAI API
        response = call_open_ai(message)
        logging.info("Received response from OpenAI")
        
        print(response)
    except Exception as e:
        logging.error("An error occurred in hacking_bot function: %s", str(e))

while True:
    try:
        question = input("Ask: ")
        hacking_bot(question, "1")
        print("\n")
    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")
        break
    except Exception as e:
        logging.error("An error occurred in the main loop: %s", str(e))
