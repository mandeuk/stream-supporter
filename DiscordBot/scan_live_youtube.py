import discord
import datetime
import asyncio
import os
import google.auth
import requests
import json

from discord.ext import commands
from googleapiclient.discovery import build
from datetime import datetime

#config 파일 불러오기
with open('config.json', 'r') as f:
    config = json.load(f)

async def scan_live_youtube(bot: discord.ext.commands.Bot):
    test_channel_id = 1201193468106657863
    test_channel = bot.get_channel(test_channel_id)
    is_magol_live = False

    while True:
        now = datetime.datetime.now(datetime.timezone.utc)
        #print(f'while loop {now.second}')
        if now.second == 1 or now.second == 6 or now.second == 11 or now.second == 16 or now.second == 21 or now.second == 26 or now.second == 31 or now.second == 36 or now.second == 41 or now.second == 46 or now.second == 56:
            #유튜브 채널 스캔
            print('유튜브 채널 스캔')
            #is_magol_live = await check_live_status()
            try:
                content = requests.get('https://www.youtube.com/@SBSRunningMan/live').text
                ENCODED = str(content).encode("ascii", "ignore")
                print(f'content -> {content}')
                print('@@@@@')
                print(f'content -> {ENCODED}')
                print('@@@@@')
                print(f'content -> {ENCODED.decode()}')

                if 'hqdefault_live.jpg' in ENCODED.decode():
                    print('Channel Is Live')
                    is_magol_live = True
                else:
                    print("Channel Isn't Live")
                    is_magol_live = False
            except Exception as error:
                print(f'Error!!!! -> {error}')
            
            if test_channel and is_magol_live == True:
                print('scan')
                await test_channel.send(f'현재 라이브 방송 중입니다 {now.hour}:{now.minute}:{now.second}')
            else:
                print('방송 중이지 않습니다')
                # print(f"Couldn't find the channel with ID {test_channel_id}")
                # print("Available channels:")
                # for channel in bot.get_all_channels():
                #     print(f"{channel.name} - {channel.id}")
                #     #await test_channel.send('유튜브를 스캔합니다')
        
        await asyncio.sleep(1)


# YouTube API 관련 설정
api_key = config['google']['api_key']  # Google API Console에서 생성한 API 키
channel_id = config['google']['channel_id']  # 확인하려는 채널의 ID

# YouTube API 클라이언트 생성
youtube = build('youtube', 'v3', developerKey=api_key)

checking_live = True

#현재시간 기록용
check_time_iso = datetime.now().isoformat()

async def check_live_status():
    print('check_live_status() in')

    # 채널의 생방송 상태 확인
    # response = youtube.channels().list(
    #     part='snippet, contentDetails, statistics',
    #     id=channel_id
    # ).execute()
    response = youtube.channels().search(
        part='snippet',
        channelId = channel_id
    ).execute()

    #youtube.channel().search

    print(f'response -> {response}')

    # 채널 정보 추출
    channel_info = response['items'][0]
    print(f'channel_info -> {channel_info}')
    
    # 생방송 중인지 확인
    live_status = channel_info['snippet']['liveBroadcastContent']
    print(f'live_status -> {live_status}')

    print('check_live_status() out')
    if live_status == 'live':
        print(f"{channel_info['snippet']['title']} 채널은 현재 생방송 중입니다.")
        return True
    else:
        print(f"{channel_info['snippet']['title']} 채널은 현재 생방송 중이 아닙니다.")
        return False

async def start_check_live_status():
    # Connect to DB

    while checking_live:
        activities = await check_activities()

        #if activities have value
        #iv activity is upload state
        #check_video
        #if current viewer
        #send notification to discord
    
    return

async def check_activities():
    response = youtube.activities().list(
        part='id,snippet,contentDetails',
        channelId = channel_id,
        publishedAfter="abc"
    ).execute()

    print(f'response -> {response}')

async def check_video(video_id):
    request = youtube.videos().list(
        part="id,liveStreamingDetails",
        id=video_id
    )

    response = request.execute()
    print(response)