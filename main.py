import os

import requests
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

TOKEN = os.environ.get("DISCORD")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

url = "https://api.groq.com/openai/v1/models"
headers = {
    "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",
    "Content-Type": "application/json"
}
response = requests.get(url, headers=headers).json()
models = []

for model in response.get("data", []):
    models.append(model["id"])
print(models)
modelss = []
model_choices = [app_commands.Choice(name=model, value=model) for model in models]

@bot.tree.command(name="ask", description="What would you like to ask?")
@app_commands.describe(message="Ask the AI a question", model='Choose a model')
@app_commands.choices(model=model_choices)
async def ask(interaction: discord.Interaction, message: str, model: str = "llama-3.3-70b-versatile"):
    chat = client.chat.completions.create(
        messages=[{"role": "user", "content": message}],
        model=model,
        temperature=0.6,
        max_tokens=1024,
        stream=False
    )
    await interaction.response.send_message(f"**{chat.choices[0].message.content}**")

bot.run(TOKEN)
