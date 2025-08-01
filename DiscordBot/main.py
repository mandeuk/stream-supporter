import discord #모듈 설치 필요 pip install -U discord.py
from discord.ext import commands
import json

#다른 파일 import
import scan_live_youtube
import scan_live_chzzk # Import the new Chzzk scanner
import db

#config 파일 불러오기
with open('config.json', 'r') as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
dbcxn = None


@bot.event
async def on_ready():
    global dbcxn
    if not dbcxn:
        await db.connect_db()

    print(f'Logged in as {bot.user.name}')
    # Start the Chzzk live stream scanner as a background task
    bot.loop.create_task(scan_live_chzzk.scan_live_chzzk(bot))

@bot.command()
async def start(ctx):
    await ctx.send('가동 계시')

@bot.command()
async def scan(ctx):
    #보낸 사람의 권한 체크
    print(ctx)
    print(ctx.permissions)
    print(ctx.permissions.administrator)
    #await scan_live_youtube.scan_live_youtube(bot)
    #await ctx.send('가동 계시')



bot.run(config['discord']['bot_id'])