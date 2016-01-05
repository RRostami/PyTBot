# PyTBot
##### A Pure Python API Wrapper for Telegram Bot API
Including all-new Inline API
### Install
To Install using PIP: 
`pip install pytbot`

### Basics
```
import PyTBot
bot = PyTBot.bot(my_token)
for update in bot.getUpdates_iter(limit=50):
	print("{} said: {}".format(update.sender.first_name,update.text))
	res=bot.sendMessage(update.sender.id,"hi") 
```
Note : getUpdates_iter Automatically keeps track of read messages, so you will only get new messages with each call


### Working With Updates