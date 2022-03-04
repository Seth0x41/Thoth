
from telebot import types
import os
import telebot
API_KEY= 'Your Bot token Here!'
bot = telebot.TeleBot(API_KEY)

# Common messages
# this is the start message, it returns Hello message and how to use the bot
@bot.message_handler(commands=["تحوت","start"])
def start(message):
    bot.send_message(message.chat.id,"""أهلاً، عامل ايه؟
أنا هيكون اسمى تحوت، هساعدك الفترة الجاية إنك تلاقى المحاضرات بتاعتك وهكون حلقة وصل بينك وبين زمايلك
أنا اتبرمجت على أوامر معينة إنى انفذها، ولو لقيت عندى مشكلة ياريت تبعت على جروب التلجرام بتاعنا مشكلتى والى برمجنى هيصلحها.
فى شوية حاجات محتاج تعرفها عشان تعرف تتعامل معايا، أنا عندى ليستة أوامر عشان تساعدك تستخدمنى صح، هتلاقى موجود منها بالعربى وبالإنجليزي بينفذوا نفس الغرض
لكن الدعم من تلجرام بيكون للأمر بالإنجليزي، فهتلاقيه متلون وتقدر تضغط عليه بدون كتابته كل مرة.
الأومر:
-----------------
/تحوت 
/start


الأمرين دول لما بتستخدمهم أنا بعيد عليك الرسالة الى انتَ بتقرأها دلوقتى تانى.

-----------------
/المواد
/subjects


الأمرين دول هيظهر ليك المواد إلى علينا عشان تختار منها المحاضرات
بمجرد ما بتختار المادة أنا بعرضلك المحاضرات الموجودة عندى، المحاضرات دى ممكن تشمل ملفات pdf
وممكن صور وممكن كمان رسالة فيها لينكات مهمة.
مجرد ما بتختار المحاضرة إلى محتاجها، إكتبهالى فى رسالة
على سبيل المثال
`محاضرة 1`
وقتها انا هبعتلك كل المحاضرات المتوفرة عندى.
-----------------
/roadmap
/خريطة_التعلم
الأمرين دول هيوفرلك خريطة من البداية عن إزاى تذاكر وتتعلم هندسة برمجيات بطريقة كويسة وصحيحة
وكمان هيوفرلك مصادر كويسة تقدر تتعلم منها بطريقة مظبوطة.

-----------------
/الجدول
/schedule

الأمرين دول هيبعتلك جدول المحاضرات.
-----------------
/مساعدة
/help

الأمرين دول هيبعتلك فيديو عن طريقة الإستخدام للبوت

-------------
/الكود
/source_code

الأمرين دول هيبعتلك الكود بتاع البوت على جيتهاب، عشان لو حبيت تعدل عليه عشان يناسب القسم بتاعتك، ولو احتاجت أى مساعدة متترددش تبعتلنا.

------------
/collaborators
/المساهمين

البوت ده قايم على فكرة مشاركة المعلومة، المحاضرات إلى هتترفع على البوت ده هتكون مكتوبة بإيد زمايل ليكم فى نفس القسم
عشان كده عندنا أهم أمر موجود فى البوت ده.
هنكتب اسماء كل الأفراد الى بتساهم فى إنها تنشر علمها ومجهودها، ونوجهلهم الشكر كل مرة على المجهود العظيم إلى هيبذلوه.

------
جروب التلجرام:
https://t.me/MathAndCS
    
    """)

# This is what out subject command, it returns the subjects name and the correct format to use in other commands
@bot.message_handler(commands=["الجدول",'schedule'])
def schedule(message):
    photo = open('Subjects/schedule.png', 'rb')
    bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=["خريطة_التعلم",'roadmap'])
def Roadmap(message):
    bot.send_message(message.chat.id,"""
    المحتوى ده هيكون متجدد كل فترة، لكن مبدئيًا انتَ الى محتاجه كأساسيات موجود فى الريبو ده
    https://github.com/ounissi-zakaria/TeachYourselfCS-AR/blob/main/TeachYourselfCS-AR.md""")

@bot.message_handler(commands=["المساهمين",'collaborators'])
def collaborators(message):
    with open('collaborators.txt','rb') as f:
        data = f.read()
        bot.send_message(chat_id=message.chat.id,text=data)

@bot.message_handler(commands=["الكود",'source_code'])
def source_code(message):
    bot.send_message(chat_id=message.chat.id,text="https://github.com/Seth0x41/Thoth")
@bot.message_handler(commands=["مساعدة",'help'])
def HowToUse(message):
    bot.send_message(chat_id=message.chat.id,text="https://vimeo.com/684400996")


