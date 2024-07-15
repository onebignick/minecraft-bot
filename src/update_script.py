import requests
from dotenv import load_dotenv
import os

load_dotenv()

APP_ID = os.environ.get("APP_ID")
SERVER_ID = os.environ.get("SERVER_ID")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

url = f"https://discord.com/api/v10/applications/{APP_ID}/guilds/{SERVER_ID}/commands"
print(url)

json = [
    {
        "name": "start_server",
        "description": "Starts the server",
        "options": []
    },
    {
        "name": "stop_server",
        "description": "Stops the server",
        "options": []
    },
    {
        "name": "reboot_server",
        "description": "Reboots the server",
        "options": []
    },
]

headers = {"Authorization": f"Bot {BOT_TOKEN}"}
response = requests.put(url, headers=headers, json=json)
print(response.json())
