import discord
import datetime
import asyncio
import requests
import json

import db # Import the database module

#config 파일 불러오기
with open('config.json', 'r') as f:
    config = json.load(f)

chzzk_channel_id = config['chzzk']['channel_id']
discord_notification_channel_id = int(config['chzzk']['discord_notification_channel_id'])

async def scan_live_chzzk(bot: discord.ext.commands.Bot):
    notification_channel = bot.get_channel(discord_notification_channel_id)
    
    while True:
        now = datetime.datetime.now()
        # Check every 10 seconds for demonstration. Adjust as needed.
        if now.second % 10 == 0: 
            print(f'Chzzk 채널 스캔 중... {now.hour}:{now.minute}:{now.second}')
            
            current_chzzk_live_status = False
            try:
                api_url = f"https://api.chzzk.naver.com/polling/v1/channels/{chzzk_channel_id}/live-status"
                response = requests.get(api_url)
                data = response.json()

                if data and data.get('content') and data['content'].get('status') == 'OPEN':
                    current_chzzk_live_status = True
                    print(f"Chzzk Channel '{chzzk_channel_id}' Is Live!")
                else:
                    current_chzzk_live_status = False
                    print(f"Chzzk Channel '{chzzk_channel_id}' Isn't Live.")
                
                # Get last known status from DB
                db_status = await db.get_chzzk_stream_status(chzzk_channel_id)

                if current_chzzk_live_status and (not db_status or not db_status['is_live']):
                    # Stream just went live, send notification
                    if notification_channel:
                        await notification_channel.send(f'치지직 라이브 방송 시작! {now.hour}:{now.minute}:{now.second}')
                    # Update DB: set is_live to True and record notification time
                    await db.update_chzzk_stream_status(chzzk_channel_id, True, str(discord_notification_channel_id), now)
                elif not current_chzzk_live_status and db_status and db_status['is_live']:
                    # Stream just went offline
                    # Update DB: set is_live to False and clear last_notified_at
                    await db.update_chzzk_stream_status(chzzk_channel_id, False, str(discord_notification_channel_id), None)
                elif db_status is None:
                    # First time seeing this channel, record its current status
                    await db.update_chzzk_stream_status(chzzk_channel_id, current_chzzk_live_status, str(discord_notification_channel_id), now if current_chzzk_live_status else None)

            except Exception as error:
                print(f'Error checking Chzzk live status: {error}')
        
        await asyncio.sleep(1)
