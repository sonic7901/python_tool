from WebChatGPT import ChatGPT
bot = ChatGPT(
    "<path-to-openai-cookies.json>"
)
response = bot.chat('<Your prompt>')

print(response)
#Ouput : What can I do for you today?