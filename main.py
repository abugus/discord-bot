import os
import discord
from discord.ext import commands
from keep_alive import keep_alive  # импортируем веб-сервер

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Чтобы видеть вход новых участников

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Бот запущен как {bot.user}')

@bot.command()
async def привет(ctx):
    await ctx.send("Привет! Я готов к работе.")

@bot.event
async def on_member_join(member):
    channel_id = 1375585953573245069
    channel = bot.get_channel(channel_id)

    if channel:
        await channel.send(f"👋 Привет, {member.mention}! Добро пожаловать на наш сервер!\nНапиши одному из смотрящих, чтобы тебе выдали роль.")
    else:
        print("❌ Канал не найден. Проверь ID!")

# 🔴 ВАЖНО: сначала запускаем веб-сервер
keep_alive()

# 🔑 Убедись, что токен сохранён в Secrets → "TOKEN"
bot.run(os.environ['TOKEN'])
