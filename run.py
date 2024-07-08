import argparse
import base64

import httpx
import requests
import subprocess
import discord
import json
import re
from anthropic import AnthropicVertex

parser = argparse.ArgumentParser()

parser.add_argument('--model', required=False, default='claude-3-5-sonnet@20240620', help='모델')
parser.add_argument('--project', required=True, help='프로젝트 아이디')
parser.add_argument('--token', required=True, help='봇 토큰')
parser.add_argument('--channel', required=True, help='채널 아이디')
parser.add_argument('--kor', required=False, default=true, help='한글입출력')
parser.add_argument('--limit', required=False, default=20, help='최대 컨텍스트')

args = parser.parse_args()

MODEL = args.model.replace('$', '')
PROJECT_ID = args.project.replace('$', '')
BOT_TOKEN = args.token.replace('$', '')
CHANNEL_ID = args.channel
KOR = args.kor
LIMIT = args.limit

HANGEUL = "\n[Respond Language Instruction]\n- Be sure to respond in native Korean. Any language input is recognized as Korean and always responds in Korean. Write realistic, native Korean dialogue, taking care not to make it feel like a translation of English.\n"
PROMPT = ""

def load_prompt():
  with open('prompt.json') as file:
    pmpt = json.load(file)
  order = pmpt["formatingOrder"]
  temp = pmpt["promptTemplate"]
  sys_prompt = ""
  with open('char.json') as file:
    cht = json.load(file)
  ch_name = cht["data"]["name"]
  ch_desc = cht["data"]["description"]
  for tmp in temp:
    tp = tmp["type"]
    if tp == "description":
      txt = re.sub('\{\{slot\}\}', ch_desc, tmp["text"])
    elif tp == "authornote":
      txt = tmp["text"] + HANGEUL
    else:
      txt = tmp["text"]
    txt = re.sub('\{\{char\}\}', ch_name, txt)
    txt = re.sub('\{\{user\}\}', "User", txt)
    sys_prompt = sys_prompt + re.sub('^\{\{#if.*\{\{\/if\}\}', '', txt)
  PROMPT = sys_prompt
      
      
 
 
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        channel = self.get_channel(CHANNEL_ID)
        await self.change_presence(status=discord.Status.online)

    async def on_message(self, message):
        if message.author == self.user or message.author.bot:
            return
        try:
          m = []
          role = "assistant"
          async for msg in message.channel.history(limit=LIMIT):
            t = msg.content
            c = ""
            if msg.author == self.user or message.author.bot:
              if role == "assistant":
                m.insert(0, {"role": "user", "content": "."})
              role = "assistant"
              c = role
            else:
              if role == "user":
                m.insert(0, {"role": "assistant", "content": "."})
              role = "user"
              c = role
            if t.split()[0] == "!new":
              m.insert(0, {"role": c, "content": t.replace("!new", "")})
              break
            m.insert(0, {"role": c, "content": msg.content})
          async with message.channel.typing():
            await message.channel.send(generate(m))
        except Exception as e:
          message.channel.send(e)
          

def generate(context):
  client = AnthropicVertex(region='us-east5', project_id=PROJECT_ID)
  message = client.messages.create(
    max_tokens=12000,
    messages=context,
    system = PROMPT,
    model=MODEL,
    top_p = 1.0,
    temperature = 1.0,
  )
  res_content = message.content
  response = res_content[0].text

  return response


intents = discord.Intents.default()
intents.message_content = True
dc_client = MyClient(intents=intents)
dc_client.run(BOT_TOKEN)
