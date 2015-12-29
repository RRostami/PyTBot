# PyTBot
#### A Pure Python API Wrapper for Telegram Bot API
### Install
To Install using PIP: 
`pip install pytbot`

### Basics
```
import PyTBot
bot = PyTBot.bot(my_token)
res=bot.sendMessage(34823745,"hi") 
for update in bot.getUpdates_iter(limit=50):
	print("{} said: {}".format(update.sender.first_name,update.text))
```

