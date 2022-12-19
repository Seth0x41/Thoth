

import logging
import sqlite3
from xml.dom.minidom import Document
from telegram import __version__ as TG_VER
import re
import os
from math import ceil
from random import randint
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


# Enable logging
logging.basicConfig(filename="logs.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# STAGES
SELECTNG_LEVEL,SELECTING_DEPARTMENT,SELECTING_CLASS,DISPLAY_COURSES,SHOW_COURSES,SHOW_LECTURES,SELECTING_COURSES,CHOISING,SELECTING_LECTURE=range(9)
SETTINGS,EDIT_DEPARTMENT,EDIT_COURSES,EDIT_LEVEL,BACK_COURSES=range(5)
department=None


# Generated Buttons
def levels_buttons(last_level=4)-> list:
    """Creating Level Buttons by default 4 levels."""
    buttons=[[],]
    for level in range(1,last_level+1):
        buttons[0].append(InlineKeyboardButton(text=level, callback_data=str(level)))
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard

def departments_buttons():
    """Fatching Departments names from database and generating inline keyboard buttons"""
    cur.execute(f"SELECT department_name FROM department")
    rows = cur.fetchall()
    department_buttons=[[],]
    counter=0
    for row in range(1,len(rows)):
            department_buttons[0].append(InlineKeyboardButton(rows[row][0], callback_data=rows[row][0]))

    keyboard = InlineKeyboardMarkup(department_buttons)
    return keyboard
            

def courses_buttons(department_name:int)->list:
    """Fatching courses from database."""
    cur.execute(f"SELECT courses.course_name FROM courses CROSS JOIN department_courses ON department_courses.course_id=courses.course_id and department_courses.department_id=(SELECT department.department_id FROM department WHERE department.department_name='{department_name}')")
    rows = cur.fetchall()
    courses=[[],[],]
    median_length=len(rows)/2
    for row in range(len(rows)):
        if row < median_length:
            
            courses[0].append(InlineKeyboardButton(rows[row][0], callback_data=rows[row][0]))
        else:
            courses[1].append(InlineKeyboardButton(rows[row][0], callback_data=rows[row][0]))
    courses.append([InlineKeyboardButton("إنهاء", callback_data=str("Done"))])
    keyboard = InlineKeyboardMarkup(courses)
    return keyboard

def enrollment_courses_buttons(chat_id)->list:
    """Fatching courses from database."""
    cur.execute(f"SELECT courses.course_name FROM courses,students INNER JOIN enrollment ON enrollment.course_id=courses.course_id AND enrollment.student_id = students.student_id and students.chat_id='{chat_id}'")
    rows = cur.fetchall()
    courses=[[],[],]
    median_length=len(rows)/2
    for row in range(len(rows)):
        if row < median_length:
            
            courses[0].append(InlineKeyboardButton(rows[row][0], callback_data=rows[row][0]))
        else:
            courses[1].append(InlineKeyboardButton(rows[row][0], callback_data=rows[row][0]))
    keyboard = InlineKeyboardMarkup(courses)
    return keyboard

def lectures_buttons(course):
    course_path=os.getcwd()+"\\"+"courses"+"\\"+course
    lectures=os.listdir(course_path)
    if lectures:
        lectures_buttons=[[],[],]
        median_length=len(lectures)/2
        for lecture in range(len(lectures)):
            if lecture < median_length:
                lectures_buttons[0].append(InlineKeyboardButton(lectures[lecture], callback_data=lectures[lecture]))
            else:
                lectures_buttons[1].append(InlineKeyboardButton(lectures[lecture], callback_data=lectures[lecture]))
        keyboard = InlineKeyboardMarkup(lectures_buttons)
        return keyboard
    else:
        return None

def get_chat_id(level):
    if not level:
        cur.execute("SELECT chat_id FROM students")
        chat_ids=cur.fetchall()
    else:
        cur.execute(f"SELECT chat_id FROM students WHERE student_level={level}")
        chat_ids=cur.fetchall()

def create_connection(db_file):
    """ Sqlite Database Connecting"""
    try:
        global db
        db = sqlite3.connect(db_file)
        global cur
        cur = db.cursor()
        logger.info(f"Database Connected!")
    except Exception as e:
        logger.error(f"Database Error: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starting The Conversation by asking the user about his level and store it in database."""
    user = update.message.from_user
    chat_id = update.message.chat_id
    full_name=user.full_name

    try:
        # Check if The user is Exist or Not
        # cur.execute('select exists(select 1 from students where chat_id = ?)',(chat_id,))
        # [exists] = cur.fetchone() 
        # if exists:
        #     logger.info(f"User {full_name} Restarted The Bot.")
        #     restarted_message="""انا شايفك بتحاول ترستر البوت تاني، لو حابب توصل للداتا بتاعتك تقدر تضغط على /material وهتلاقي كل الداتا الي تخصك، ولو بتواجه اي مشكلة ياريت تبلغنا على الجروب بتاعنا @MathAndCS."""
        #     await context.bot.send_message(chat_id=update.effective_chat.id, text=restarted_message)
        # else:
        cur.execute("INSERT INTO students(chat_id,full_name) VALUES(?,?) ",(chat_id,full_name))
        db.commit()
        logger.info(f"User {full_name} Joined The Bot.")
        start_massage=f"""أهلًا يا {full_name}،
    أنا اسمي تحوت 🤓، وظيفتي إني أكون مٌساعد ليك طول فترة الكلية سواءًا كان إني أقدملك محاضرات، أو اني اقدملك أي داتا انتَ ممكن تحتاجها طول سنين دراستك 🫡.
    الهدف إلي اتبنيت عشانه هو إننا نساعد بعض، الداتا إلي موجودة على البوت أصحابك هم إلي كاتبينها وهم إلي موفرينها تقدر تعرفهم من خلال /Honorary_board، وده مجرد إمتنان وشكر مننا ليهم .. فـ لو حابب تساعدنا بإنك توفر داتا ياريت تبعتلنا الداتا دي على الجروب.
    وكمان المشروع ده اوبن سورس، لو حبيت تضيف أو تعدل أو تعيد استخدامه في المستقبل تقدر تلاقي الكود بتاعه هنا /source_code.
    وأنا اسف اني طولت عليك ..
    ممكن تضغط على الأمر /go عشان تبدأ الاستخدام.
    الجروب بتاعنا: @MathAndCS"""
        await context.bot.send_message(chat_id=update.effective_chat.id, text=start_massage)
    except Exception as e:
        logger.error(f"Error Message : {e}")

    return SELECTNG_LEVEL


async def select_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starting The Conversation by asking the user about his level and store it in database."""
    user = update.message.from_user

    full_name=user.full_name
    level_message="""جميل، ممكن تعرفني انتَ في سنة كام؟"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=level_message,reply_markup=levels_buttons())

    return SELECTING_DEPARTMENT



async def first_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This function for prepared year.
    """
    query = update.callback_query
    keyboard = [
        [
            InlineKeyboardButton("علمي رياضة", callback_data=str("math")),
            InlineKeyboardButton("علمى علوم", callback_data=str("science")),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="ممكن تختار شعبتك؟", reply_markup=reply_markup
    )
    return DISPLAY_COURSES


async def departments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Function to insert student level and display departments"""
    query = update.callback_query
    await query.answer()
    student_level= int(query.data)
    chat_id = query.from_user.id
    cur.execute(f"UPDATE students SET student_level={student_level} WHERE chat_id={chat_id}")
    db.commit()
    await query.edit_message_text(text="تمام، دلوقتي اختار القسم بتاعك", reply_markup=departments_buttons())
    return DISPLAY_COURSES
    
async def display_courses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    department_name= query.data
    chat_id = query.from_user.id
    cur.execute(f"UPDATE students Set (dapartment_id)=(SELECT department.department_id FROM department WHERE department.department_name='{department_name}') WHERE chat_id='{chat_id}'")
    db.commit()
    await query.edit_message_text(text="جميل، دلوقتي تقدر تختار المواد الي انتَ حابب تسجلها، وبعد ما تخلصهم كلهم اضغط على انهاء", reply_markup=courses_buttons(department_name))

    return SELECTING_COURSES

async def select_courses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    chat_id = query.from_user.id
    await query.answer()
    print("Iam Here")
    if query.data:
        if query.data != "Done":
            cur.execute(f"""SELECT courses.course_name FROM courses,students INNER JOIN enrollment ON enrollment.course_id=courses.course_id and enrollment.student_id=students.student_id and students.chat_id={chat_id};""")
            data = cur.fetchall()
            user_courses=[course[0] for course in data]
            if query.data in user_courses:
                await context.bot.send_message(query.from_user.id,text=f"{query.data} موجودة فعلاً")
            else:
                cur.execute(f"""SELECT students.student_id,courses.course_id FROM students,courses WHERE students.chat_id={chat_id} and courses.course_name='{query.data}'""")
                student_id,course_id = cur.fetchone()
                cur.execute(f"""INSERT INTO enrollment (course_id,student_id) VALUES(?,?)""",(course_id,student_id))
                db.commit()
                await context.bot.send_message(query.from_user.id,text=f"{query.data} إتضافت بنجاح")
        elif query.data =="Done":
            await query.delete_message()
            await context.bot.send_message(query.from_user.id,text="خلاص كده، شكرًا جدًا ليك، تقدر دلوقتي تضغط على /material عشان توصل للداتا المتوفرة للمستوي والقسم بتاعك.")
            # Return SHOW COURSES entry
            return SHOW_COURSES
        else:
            await context.bot.send_message(query.from_user.id,text=f"في مشكلة حصلت في الكود، ياريت تكلم حد من الأدمنز يصلحها")

async def show_courses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id

    await context.bot.send_message(text="هتذاكر إيه النهارده؟",chat_id=chat_id,reply_markup=enrollment_courses_buttons(chat_id))    
    return SHOW_LECTURES

async def show_lectures(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    course = query.data
    context.user_data["Course"]=course
    if lectures_buttons(course):
        await query.edit_message_text(text="اختار المحاضرة", reply_markup=lectures_buttons(course))
    else:
        await query.edit_message_text(text="للأسف، مفيش محاضرات متوفرة هنا للمادة دي :( \n لو تقدر توفر أي محاضرات ياريت تبلغنا")
    return SELECTING_LECTURE


async def select_lecture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query=update.callback_query
    chat_id = query.from_user.id
    course=context.user_data.get("Course")
    selected_lecture= query.data
    lecture_path=os.getcwd()+"\\"+"courses"+"\\"+course+"\\"+selected_lecture
    await context.bot.send_message(query.from_user.id,text=f"ثواني وهبعتلك المحاضرة")
    for file in os.listdir(lecture_path):
        # file path
        file_path=lecture_path+"\\"+file
        if file.endswith((".pdf")):
            await context.bot.send_document(chat_id,open(file_path,'rb'))
        if file.endswith((".jpg",".png")):
            await context.bot.send_photo(chat_id,open(file_path,'rb'))
        if file.endswith("txt"):
            with open(file_path,"r") as f:
                data= f.read()
                await context.bot.send_message(query.from_user.id,text=data)
        if file.endswith((".mp3",".wav")):
            await context.bot.send_audio(chat_id,open(file_path,'rb'))

    await context.bot.send_message(query.from_user.id,text=f"دي كل حاجة عندي للمحاضرة دي، لو محتاج حاجة تاني ياريت تضغط على /material")
    return SHOW_LECTURES

async def honorary_board(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open("Honorary board.txt","r") as f:
        data= f.read()
        await context.bot.send_message(update.effective_chat.id,text=data)    

async def source_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
    'Source Code:',
    reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(text='github', url='https://github.com/Seth0x41/Thout')],
    ])
)




async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE)-> str:
    await update.message.reply_text("تمام، سلام")
    return ConversationHandler.END



if __name__ == '__main__':
    create_connection("Telegrambot.db")
    application = Application.builder().token("TOKEN").read_timeout(47).get_updates_read_timeout(42).build()

    first_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start',start)],
    states={
        SELECTNG_LEVEL:[
            CommandHandler("go",select_level)
        ],

        SELECTING_DEPARTMENT:[
            CallbackQueryHandler(departments, pattern=f"^"+str(2)+"|"+str(3)+"|"+str(4)+"$"),
            CallbackQueryHandler(first_level,pattern="^" + str(1) + "$")
        ],


        DISPLAY_COURSES:[
          CallbackQueryHandler(display_courses)
        ],
        SELECTING_COURSES:[
         CallbackQueryHandler(select_courses)       
        ],
        SHOW_COURSES:[
        CallbackQueryHandler(show_courses,pattern="^Done$"),
        CommandHandler("material",show_courses)
        ],
        SHOW_LECTURES:[
            CallbackQueryHandler(show_lectures)
        ],
        SELECTING_LECTURE:[
            CallbackQueryHandler(select_lecture)
        ],

    },
    
        fallbacks=[CommandHandler('cancel',cancel)],
        allow_reentry=True
    
    )


    secound_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('material',show_courses)],
    states={
 SHOW_LECTURES:[
            CallbackQueryHandler(show_lectures)
        ],
        SELECTING_LECTURE:[
            CallbackQueryHandler(select_lecture)
        ],
    },
    
        fallbacks=[CommandHandler('cancel',cancel)],
        allow_reentry=True
    
    )

    application.add_handler(first_conv_handler)

    
    application.add_handler(secound_conv_handler)



    application.add_handler(CommandHandler("Honorary_board",honorary_board))
    application.add_handler(CommandHandler("source_code",source_code))
    application.add_handler(CommandHandler("material",show_courses))
    application.run_polling()