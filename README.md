# Thoth Telegram Bot
---
The main goal of this bot is to make it easier to get lecture notes, lecture schedules, etc without asking anyone for them.

### Thoth Commands:
`start` - sending the Start message and the main commands with their usage.
`help` - sending a video about how to use this bot.
`schedule` - sending lecture schedule as a png file that locates at Subjects/schedule.png
`roadmap` - sending teach yourself cs repo.
`collaborators` - sending names of our collaborators and how they helped us.
`source_code` - sending this repo URL :D
`subjects` - sending to the user an Inline Keyboard Buttons to select the course name that is listed from the Subjects folder and after that sending to the user list of all available lectures from this course such `محاضرة 3` `محاضرة 2` `محاضرة 1` in the directory `Subjects/Topology/` once the user selects his lecture and sending it in a message `محاضرة 1` the bot sending all the content of `محاضرة 1` folder.

### Adding more courses
once you want to add new courses to this bot, all you want is to create a new folder in the Subject directory with the course name and add its lecture in other folders.

### Adding lectures
to add lectures to your course and for now, all you need is to create a new folder in your course name folder with that naming structure ` محاضرة `+ `number of that lecture`.
### Adding new command
this bot was built with  [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) so according to [Official documentation](https://pytba.readthedocs.io/en/latest/index.html) 
```python 
## This is just an example of creating a simple `commandName` 
# command and handle user message and reply to it.

@bot.message_handler(commands=['commandName'])
def FunctionName(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""") 
```
