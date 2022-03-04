# Thoth Telegram Bot
---
The main goal of this bot is making it easier getting lecture notes, lecture schedule, etc without asking anyone for it.

### Thoth Commands:
`start` - sending Start message and the main commands with their usage.
`help` - sending video about how to use this bot.
`schedule` - sending lecture schedule as png file that locate at Subjects/schedule.png
`roadmap` - sending teach yourself cs repo.
`collaborators` - sending names of our collaborators and how they helped us.
`source_code` - sending this repo url :D
`subjects` - sending to the user an Inline Keyboard Buttons to select the course name that listed from Subjects folder and after that sending to the user list of all available lectures from this course such `محاضرة 3` `محاضرة 2` `محاضرة 1` in the directory `Subjects/Topology/` once the user select his lecture and sending it in a message `محاضرة 1` the bot sendig all the content of `محاضرة 1` folder.

### Adding more courses
once you want adding new courses to this bot, all you want is creating new folder in Subject directory with course name, and adding it's lecture in other folders.

### Adding lectures
to add lectures to your course and for now all you need is creating a new folder in your course name folder with that name structure ` محاضرة `+ `number of that lecture`.
### Adding new command
this bot was built with  [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) so accoring to [Official documentation](https://pytba.readthedocs.io/en/latest/index.html) 
```python 
## This is just example to creating a simple `commandName` 
# command and handle user message and reply to it.

@bot.message_handler(commands=['commandName'])
def FunctionName(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""") 
```
