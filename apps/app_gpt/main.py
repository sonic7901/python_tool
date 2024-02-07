from WebChatGPT import ChatGPT
import speech_recognition as sr
import pyttsx3

# 初始化語音識別器和文字轉語音引擎
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()


def read_chat(input_str):
    bot = ChatGPT(
        "chat.openai.com.cookies.json"
    )
    response = bot.chat(input_str)
    return str(response)


def set_speak():
    print(sr.Microphone.list_working_microphones())
    while True:
        with sr.Microphone(device_index=1) as source:
            # 調整麥克風收音閾值
            recognizer.adjust_for_ambient_noise(source)
            print("GPT: 聆聽中...")
            audio = recognizer.listen(source)
            try:
                text_start = recognizer.recognize_google(audio, language='zh-TW')
                print("User：", text_start)
                if "朋友" in text_start:
                    print("User：", text_start)
                    temp_response = read_chat(text_start)
                    print("GPT:" + temp_response)
                    tts_engine.say(temp_response)
                    tts_engine.runAndWait()
            except Exception as e:
                print("GPT: 無法識別")
                tts_engine.say("抱歉，我沒聽懂，請再試一次")
                print(e)


set_speak()
