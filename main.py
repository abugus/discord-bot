import os
import sys
import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# === СЛОВАРЬ ПРЕДУПРЕЖДЕНИЙ ===
warnings = {}

# === ЗАПУСК ===
@bot.event
async def on_ready():
    print(f'✅ Бот запущен как {bot.user}')

# === !привет ===
@bot.command()
async def привет(ctx):
    await ctx.send("Да не сплю я, не сплю!")

# === Приветствие и автоматическая роль при входе ===
@bot.event
async def on_member_join(member):
    channel_id = 1375585953573245069
    role_id = 1375786616660164679

    channel = bot.get_channel(channel_id)
    role = member.guild.get_role(role_id)

    if role:
        await member.add_roles(role)
        print(f"✅ Роль '{role.name}' выдана {member.name}")

    if channel:
        await channel.send(
            f"👋 Салам, {member.mention}! Добро пожаловать на сервер!\n"
            f"Напиши одному из смотрящих, чтобы тебе выдали роль бедварсер."
        )
    else:
        print("❌ Канал не найден. Проверь ID!")

# === !очистить <количество> сообщений ===
@bot.command()
@commands.has_permissions(manage_messages=True)
async def очистить(ctx, количество: int = 5):
    await ctx.channel.purge(limit=количество + 1)
    await ctx.send(f"🧹 Удалено {количество} сообщений.", delete_after=3)

# === !варн @участник причина ===
@bot.command()
@commands.has_permissions(kick_members=True)
async def варн(ctx, участник: discord.Member, *, причина="Без причины"):
    if участник not in warnings:
        warnings[участник] = []
    warnings[участник].append(причина)

    количество = len(warnings[участник])
    await ctx.send(
        f"⚠️ {участник.mention} получил предупреждение: {причина} (всего: {количество})"
    )

    if количество >= 3:
        try:
            await участник.send("🚫 Ты получил 3 предупреждения и был забанен.")
        except:
            pass  # ЛС могли быть закрыты

        await участник.ban(reason="3 предупреждения")
        await ctx.send(f"🔨 {участник.mention} был забанен за 3 предупреждения.")

# === !очиститьварны @участник ===
@bot.command()
@commands.has_permissions(kick_members=True)
async def очиститьварны(ctx, кого: discord.Member = None):
    if кого:
        if кого in warnings:
            del warnings[кого]
            await ctx.send(f"🧽 Предупреждения для {кого.mention} очищены.")
        else:
            await ctx.send("ℹ️ У пользователя нет предупреждений.")
    else:
        await ctx.send("❌ Укажи пользователя. Пример: !очиститьварны @user")

# === keep_alive и запуск ===
keep_alive()

if __name__ != "__main__":
    sys.exit("⛔ Бот был импортирован как модуль. Выход.")

bot.run(os.environ['TOKEN'])
