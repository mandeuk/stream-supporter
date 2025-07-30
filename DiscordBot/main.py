import discord #모듈 설치 필요 pip install -U discord.py
from discord.ext import commands
import json

#다른 파일 import
import scan_live_youtube
import db

#config 파일 불러오기
with open('config.json', 'r') as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
dbcnx = None


@bot.event
async def on_ready():
    if not dbcnx:
        dbcnx = await db.connect_db()

    # test_channel_id = 1201193468106657863  # Replace with your actual channel ID
    # test_channel = bot.get_channel(test_channel_id)
    
    # if test_channel:
    #     await test_channel.send('전자마골 가동 준비 완료')
    # else:
    #     print(f"Couldn't find the channel with ID {test_channel_id}")
    # await scan_live_youtube.check_activities()
    # #bot.loop.create_task(scan_live_youtube.scan_live_youtube(bot))

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