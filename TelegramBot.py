from commands import *
SubjectPath = None
# assign current location of the bot and sending inline keyboard button to the user.
subject = os.path.dirname(os.path.abspath(__file__)) 
@bot.message_handler(commands=['subjects','المواد'])
def selectSubject(message):
    keyboard= types.InlineKeyboardMarkup()
    Button1 = types.InlineKeyboardButton(text='نظرية رسومات', callback_data="GraphicsTheory")
    Button2=telebot.types.InlineKeyboardButton(text='توبولوجي', callback_data="Topology")
    Button3=telebot.types.InlineKeyboardButton(text='هندسة تفاضلية', callback_data="DifferentialGeometry")
    Button4=telebot.types.InlineKeyboardButton(text='رسومات حاسب', callback_data="ComputerGraphics")
    Button5=telebot.types.InlineKeyboardButton(text='برمجة منطقية', callback_data="LogicalProgramming")
    Button6=telebot.types.InlineKeyboardButton(text='بحوث عمليات', callback_data="OperationsResarch")
    keyboard.add(Button1,Button2,Button3,Button4,Button5,Button6)
    bot.send_message(message.chat.id,"هتذاكر إيه؟", reply_markup=keyboard)  


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    ReturnedMessage = "هى دى المحاضرات الموجوده، ياريت تبعت رقم المحاضرة إلى انتَ محتاجها."
    global SubjectPath
    SubjectPath = os.path.dirname(os.path.abspath(__file__))+"/Subjects/" + call.data
    if os.path.exists(SubjectPath) == True:
        if len(os.listdir(SubjectPath)) == 0: # Check is empty..
            ReturnedMessage= "للأسف ملقتش محاضرات للمادة دى عندى، لو حابب تساعدنى إنى أضيفها ياريت تكلمنى"
        else:
            for FileName in sorted(os.listdir(SubjectPath)):
                bot.send_message(call.message.chat.id,text=FileName)
        
    else:
        ReturnedMessage= "للأسف المادة دى مش متسجلة عندى، لو شايف إن فى حاجة غلط ياريت تكلمنى"
    
    if call.message:
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=ReturnedMessage)

def Masseage_validation(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "محاضرة":
    return False
  else:
    return True
@bot.message_handler(func=Masseage_validation)
def processing(message):
    request = message.text.split()[1]
    LecturesFolder = f"{SubjectPath}/محاضرة {request}"
    bot.send_message(chat_id=message.chat.id,text="ثانية واحده وهنبعتهالك")
    if os.path.exists(LecturesFolder) == True:
        for lecture in sorted(os.listdir(LecturesFolder)):
            LecturePath= f"{LecturesFolder}/{lecture}"
            if lecture.endswith(".jpg") or lecture.endswith(".png"):
                photo = open(LecturePath, 'rb')
                bot.send_photo(message.chat.id, photo)
            elif lecture.endswith(".pdf"):
                doc = open(LecturePath, 'rb')
                bot.send_document(message.chat.id, doc)
            elif lecture.endswith(".txt"):
                with open(LecturePath,'rb') as f:
                    data = f.read()
                    bot.send_message(chat_id=message.chat.id,text=data)
            else:
                print("المحاضرة مفيهاش أى محتوي")
    else:
        bot.send_message(message.chat.id,"للأسف المحاضرة دى مش موجودة عندنا")

if __name__ == '__main__':
     bot.polling(none_stop=True)