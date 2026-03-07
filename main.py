import os
from dotenv import load_dotenv
from google import genai
import argparse
from cli_runtime import run_chatbot_loop

load_dotenv()

parser = argparse.ArgumentParser(description="Chatbot CLI")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

working_directory = os.getcwd()

run_chatbot_loop(client, working_directory, args.verbose)
