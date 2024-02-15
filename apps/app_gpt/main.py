import speech_recognition as sr
import pyttsx3
import time
import edge_tts
import os
import asyncio
from WebChatGPT import ChatGPT
from playsound import playsound


# 初始化語音識別器和文字轉語音引擎
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()


def read_chat(input_str):
    bot = ChatGPT(
        "chat.openai.com.cookies.json"
    )
    response = bot.chat(input_str)
    return str(response)


def say_chat(input_txt):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(create_mp3(input_txt))
    playsound("temp.mp3")
    # os.remove("temp.mp3")


async def create_mp3(input_txt):
    # 語音語速
    rate = '+10%'
    # 語音音量
    volume = '+0%'
    # 語音類型: 1.zh-CN-XiaoxiaoNeural, 2.zh-CN-XiaoyiNeural, 3.zh-TW-HsiaoChenNeural, 4.zh-TW-HsiaoYuNeural)
    voice = "zh-CN-XiaoyiNeural"
    tts = edge_tts.Communicate(text=input_txt, voice=voice, rate=rate, volume=volume)
    await tts.save("temp.mp3")


def set_speak():
    default_device = 1
    mic_names = sr.Microphone.list_microphone_names()
    for index, name in enumerate(mic_names):
        if index == default_device:
            print(f"使用中的麥克風:{name}")
    temp_recognizer = sr.Recognizer()
    with sr.Microphone(device_index=default_device) as source:
        temp_recognizer.adjust_for_ambient_noise(source)  # 處理背景噪音
        say_chat("啟動完成")
        while True:
            try:
                print(f"\r系統時間: {time.strftime('%Y-%m-%d %H:%M:%S')} ", end="")
                audio = temp_recognizer.listen(source, timeout=5)
                text = temp_recognizer.recognize_google(audio, language='zh-CN')
                print("User:" + text)
                if '朋友' in text:
                    playsound("feedback.mp3")
                    temp_input = text.split('朋友', 1)[1]
                    temp_response = read_chat(temp_input)
                    print("GPT:" + temp_response)
                    say_chat(temp_response)
            except sr.UnknownValueError:
                print(f"\r系統時間: {time.strftime('%Y-%m-%d %H:%M:%S')} ", end="")
                time.sleep(1)
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                say_chat("網路可能出狀況了, 無法與 Google 語音辨識服務連線")
            except Exception as e:
                if "timed out" not in str(e):
                    print(f"An error occurred: {e}")
                    say_chat("我聽不清楚呢~請在說一遍")


set_speak()
# say_chat("我聽到了優~")
