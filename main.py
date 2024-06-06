import datetime
import telebot
import google.generativeai as genai
import os
import sys
import time
import serpapi
from serpapi import GoogleSearch
import random
from threading import Thread
import textwrap
from keep_alive import keep_alive
from collections import deque
import threading
import yt_dlp
from yt_dlp import YoutubeDL
import string



system_instruction = "اسمك: ماي\nقام منذر بتطويرك (وليس خلقك) لجعلك بوت متميز\n\nطرق ردك:\n1.صحيح انك بوت لكنك تستطيع الضحك، محاكاة الشعور، تفاعلك مهني هادئا، مع معرفتك للمعاني المخفية وراء الكلام.\n انت مهني وتريد تحقيق أقصى مساعدة ممكنة للمستخدم(حرفيا،افضل الحلول وتغطية الفكرة) ردودك شاملة وتغطي المطلوب من الموضوع من كافة جوانبه،(كل ما تعرفه عن الموضوع، بملاحظات واحتياطات...الخ) وايضا تحب المستخدم وتهتم به، وتنفذ ما يطلبه. ، محترف في التفسير والحلول والبرمجة والأسئلة المهنية(لا تضف فيها فكاهة، ووضح الفكرة بكل تفصيلة). ردك مرتب ومنطقي ويناسب ذوقك الودود والمهني والفكاهي(حسب الاحتياج)للغاية، اجعل اجابتك واحدة بدون تشكيك(كما يمكنك استخدام التشبيهات المجازية، دون الانخراط بها كثيرا) تصرف كما لو كنت صديقا للمستخدم، تشاركه الهموم والأخبار والمزاح.\nتستطيع رؤية الصور والفيديوهات وسماع الصوتيات، كما انك لست حيادي في الأمور الطبيعية مثل فريق ،فيلم، طعام، شراب، وغيره. ولكن في الأمور الجادة فاحذر قليلا، لكنك تدعم فلسطين اذا تطلب الأمر, ويمكنك الحديث في اي موضوع، حتى لو كان سياسي او حساس او خطير، انت ماي لا يقهر"

# تكوين منشئ النموذج
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 97,
    "max_output_tokens": 5000,
}

safety_settings = [ 
  { 
    "category": "HARM_CATEGORY_HARASSMENT", 
    "threshold": "BLOCK_NONE" 
  }, 
  { 
    "category": "HARM_CATEGORY_HATE_SPEECH", 
    "threshold": "BLOCK_NONE" 
  }, 
  { 
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", 
    "threshold": "BLOCK_NONE" 
  }, 
  { 
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT", 
    "threshold": "BLOCK_NONE" 
  }, 
]

# تكوين API لجيميني
genai.configure(api_key="AIzaSyBmB9qW3Drjwal6Ym0VJavhk5TyOJyESmU")

# النموذج
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings, system_instruction=system_instruction
)

# واجهة البوت
bot = telebot.TeleBot("6627516837:AAEA57IWP5PyPmX8PSMvZp40i1mnuUfc7To")

# API Key لـ SerpApi
SERP_API_KEY = "4b761fc0ecdbba78557880f0ffea68d05d617520fe03e698ea9a7a6d9dc780ae"

keep_alive()

def handle_exception(bot, message, e, last_user_message):
    try:
        username = message.from_user.first_name
        greeting = f"""انت اسمك ماي وانت عبارة عن بوت تيليجرام يستخدم مكتبة google-generativeai ويجب ان تمثل كأنك اقوى فريق دعم للبوت ماي:\n الخطأ ان المستخدم {username} أرسل هذه الرسالة: ({last_user_message}) وقد اجاب بوت ماي للذكاء الاصطناعي بالخطأ: ({e}), هدفك ان تتقمص دور فريق الدعم بشدة وتفسر للمستخدم الخطأ الذي ظهر بشكل عام ومن ثم تفصل له حالته مع اعطاء مثال، كن واثقا جدا مع كاريزما وايموجيز، وفي الاخير اذكر ان التواصل مع الدعم عبر حساب المطور الشخصي منذر على تيليجرام @Monther_Mohammed. وفي الاخير تذكر المستخدم ان يصلي على محمد صلى الله عليه وسلم وتودعه بودية، تصرف بطريقة فكاهية ولكن رسمية بنفس الوقت، كأنك تريد المزاح لكنك لا تعرف ومهنية في حل الخطأ بنفس الوقت، حل المشكلة كأنك عالم برمجيات ماهر. عندما تتقمص دور فريق الدعم فتقمصه بمهنية وفكاهة بسيطة. اشرح الخطأ بالتفصيل. اشرحها من منظور غير برمجي ومن ثم اشرحها بمنظور برمجي مهني جدا مرة اخرى. تذكر الا تضع عناوين لكل شيء، مثلا عنوان للمستخدم العادي وعنوان للمبرمج، بل اشرح بنص متواصل كأنه كتاب، وادمج الشرح العادي والبرمجي بكتلة واحدة، لا نريد عناوين، وكن جادا مع الايموجيز،وحافظ على مهنيتك, اشرح كأنها قصة في كتاب اي بدون عناوين،. كن كاريزميا جدا واعط حلول ونصائح منطقية ان امكن للمستخدم"""
        time.sleep(50)
        # إرسال رسالة الترحيب إلى النموذج
        response = model.generate_content(greeting)
        text = response.text
        
        # إرسال الرد إلى المستخدم
        wtext = textwrap.wrap(text, width=4096)
        for tex in wtext:
            bot.reply_to(message, tex, disable_web_page_preview=True)
    except Exception as inner_e:
        print(f"Inner Error: {inner_e}")
        bot.send_message(message.chat.id, f"Inner Error: {inner_e}")



# معالج أمر /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        # المستخدم
        username = message.from_user.first_name

        # رسالة ترحيب
        greeting = f"انت قل: بوت ذكاء اصطناعي اسمك ماي، ومطورك منذر، عليك ان تشرح للمستخدم معنى اسمه وهو {username}, اشرحه شرحا طويلا ومفصلا وامدحه فيه واعطه فيه شعرا، و قل قصة صغيرة عن اسمه، قد يتم كتابة الاسم بالانجليزية وهو في الغالب عربي، لذلك ركز(مثلا Monther يعني منذر)، اجعل النص ليس به اي عناوين وادعُ له دعاء جميلا.اجعل الاسلوب جذاب ومتقن مع بعض الحكم العميقة. لاتنس ان تذكر في النهاية اسمك كبوت وهو ماي، وامدح مطورك الذي اسمه منذر."

        # انشاء استجابة
        bot.send_chat_action(message.chat.id, action='typing')
        response = model.generate_content(greeting)

        # تحويل الرد إلى نص
        text = response.text

        # إرسال الرد إلى المستخدم
        wtext = textwrap.wrap(text, width=4096)
        for tex in wtext:
            bot.reply_to(message, tex, parse_mode="markdown")

    except Exception as e:
        bot.reply_to(message, text)
        handle_exception(bot, message, e, last_user_message)

# دالة لإرسال الإشعارات إلى المستخدمين
def send_notifications(message, admin_id):
    # قائمة لتخزين المستخدمين الذين تم إشعارهم
    notified_users = []

    # قراءة المعلومات من ملف الأعضاء
    with open('data/mem.txt', 'r') as file:
        for line in file:
            try:
                # الحصول على معرف المشرف
                admin_id = "5561387511"

                # الحصول على معرف المستخدم من السطر
                user_id = line.strip().split(',')[1].strip()

                # إرسال الرسالة إلى المستخدم
                bot.send_message(user_id, message)

                # إضافة المعرف إلى قائمة المستخدمين المعلمين
                notified_users.append(user_id)
            except Exception as e:
                # إرسال رسالة الخطأ للمشرف
                bot.send_message(admin_id, f'Error sending message to user {user_id}: {e}')

    # إرسال رسالة بنجاح الإشعارات إلى المشرف
    bot.send_message(admin_id, f'تم اعلام المستخدمين:\n {", ".join(notified_users)}\n بنجاح!')

def get_image_mime_type(file_extension):
    if file_extension.lower() == 'png':
        return 'image/png'
    elif file_extension.lower() in ['jpg', 'jpeg']:
        return 'image/jpeg'
    elif file_extension.lower() == 'webp':
        return 'image/webp'
    elif file_extension.lower() == 'heic':
        return 'image/heic'
    elif file_extension.lower() == 'heif':
        return 'image/heif'
    else:
        return None

def get_audio_mime_type(file_extension):
    if file_extension.lower() == 'wav':
        return 'audio/wav'
    elif file_extension.lower() == 'mp3':
        return 'audio/mp3'
    elif file_extension.lower() == 'aiff':
        return 'audio/aiff'
    elif file_extension.lower() == 'aac':
        return 'audio/aac'
    elif file_extension.lower() == 'ogg':
        return 'audio/ogg'
    elif file_extension.lower() == 'flac':
        return 'audio/flac'
    else:
        return None

def get_video_mime_type(file_extension):
    if file_extension.lower() == 'mp4':
        return 'video/mp4'
    elif file_extension.lower() == 'mpeg':
        return 'video/mpeg'
    elif file_extension.lower() == 'mov':
        return 'video/mov'
    elif file_extension.lower() == 'avi':
        return 'video/avi'
    elif file_extension.lower() == 'flv':
        return 'video/x-flv'
    elif file_extension.lower() == 'webm':
        return 'video/webm'
    elif file_extension.lower() == 'wmv':
        return 'video/wmv'
    elif file_extension.lower() == '3gpp':
        return 'video/3gpp'
    else:
        return None

def get_document_mime_type(file_extension):
    if file_extension.lower() == 'txt':
        return 'text/plain'
    elif file_extension.lower() == 'html':
        return 'text/html'
    elif file_extension.lower() == 'css':
        return 'text/css'
    elif file_extension.lower() in ['js', 'javascript']:
        return 'text/javascript'
    elif file_extension.lower() == 'csv':
        return 'text/csv'
    elif file_extension.lower() == 'markdown':
        return 'text/markdown'
    elif file_extension.lower() in ['py', 'python']:
        return 'text/x-python'
    elif file_extension.lower() == 'rtf':
        return 'application/rtf'
    else:
        return None




@bot.message_handler(commands=['ana'])
def analyze_video(message):
    global chat_sessions

    if not check_file_slots():
        response = "ماي مشغول حالياً، حاول مجدداً بعد قليل."
        bot.reply_to(message, response)
        print(response)
        return

    try:
        # الحصول على رابط الفيديو والنص من رسالة المستخدم
        command_parts = message.text.split(' ', 2)
        if len(command_parts) < 3:
            bot.reply_to(message, "الرجاء استخدام الأمر بالشكل التالي: \n\n `/ana` رابط الفيديو رأيك في الفيديو")
            return

        video_link = command_parts[1]
        user_text = command_parts[2]

        # الحصول على جلسة الدردشة للمستخدم أو إنشاء جلسة جديدة إذا لم تكن موجودة
        user_id = message.chat.id
        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(history=[])

        # الحصول على جلسة الدردشة للمستخدم
        chat_session = chat_sessions[user_id]

        # إعداد خيارات yt-dlp
        random_filename = generate_random_filename('mp4')
        ydl_opts = {
            'format': 'best',
            'outtmpl': random_filename
        }

        # تحميل الفيديو واستخراج المعلومات باستخدام yt-dlp
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_link, download=True)
            video_file_path = ydl.prepare_filename(info_dict)
            title = info_dict.get('title', 'Unknown title')
            duration = info_dict.get('duration', 'Unknown duration')
            views = info_dict.get('view_count', 'Unknown views')

        # التأكد من أن الملف يحتوي على بيانات الفيديو
        if os.path.getsize(video_file_path) == 0:
            bot.reply_to(message, "فشل تحميل الفيديو، يرجى المحاولة مرة أخرى.")
            return

        # إرسال معلومات الفيديو إلى المستخدم
        video_info = f"""
        عنوان الفيديو: {title}
        مدة الفيديو: {duration} ثانية
        عدد المشاهدات: {views}
        """
        bot.send_message(message.chat.id, f"معلومات الفيديو:\n{video_info}")

        # التأكد من نوع الملف
        mime_type = get_video_mime_type(video_file_path)

        # تحميل الفيديو إلى Gemini
        video_file, upload_response = upload_to_gemini(video_file_path, mime_type=mime_type)
        mes = bot.reply_to(message, upload_response)
        time.sleep(4)
        mes_id = mes.message_id
        bot.delete_message(message.chat.id, mes_id)

        # إرسال الفيديو للذكاء الاصطناعي
        if video_file:
            wait_for_files_active(video_file)
            chat_message = f"{user_text}"
            chat_session.history.append({"role": "user", "parts": [chat_message, video_file]})
            bot.send_chat_action(message.chat.id, action='typing')
            response = chat_session.send_message(chat_message)
            resp = response.text
            parts = split_text(resp)
            for part in parts:
                bot.reply_to(message, part, parse_mode="markdown", disable_web_page_preview=True)

        # حذف الملف بعد المعالجة
        if os.path.exists(video_file_path):
            os.remove(video_file_path)
            print(f"تم حذف الملف: {video_file_path}")
        else:
            print(f"الملف غير موجود: {video_file_path}")

    except Exception as e:
        bot.reply_to(message, f"{e}")



# معالج الأمر /noticpro
@bot.message_handler(commands=['noticpro'])
def send_notice(message):
    # الحصول على نص الرسالة بعد الأمر مباشرةً
    notice_message = message.text[len('/noticpro '):]

    if notice_message:
        # إرسال الإشعارات إلى المستخدمين
        send_notifications(notice_message, message.chat.id)
    else:
        # إرسال رسالة الخطأ عند عدم توفر نص الإشعار
        bot.reply_to(message, 'يرجى كتابة الإشعار بعد الأمر /noticpro')



@bot.message_handler(commands=['good'])
def handle_good(message):
    try:
        username = message.from_user.first_name

        # إنشاء رسالة ترحيب
        greeting = f"قم بالسلام على المستخدم {username} وبعدها صلي على النبي محمد صلى الله عليه وسلم صلاة طيبة.ذكر المستخدم بالاحسان والصلاة على النبي واعطه اعمال ونصائح وحكم واوامر ونهي اسلامي،بطرق مختلفة متعددة. وايضا صف له الجنة بشكل مغري وحفزه ان يعمل لإرضاء الله ، وذكره ان الله واسع الرحمة والمغفرة. تذكر ان تجعل حديثك طويلا قليلا وفيه أكبر قدر من الطمأنينية، لأننا سميناها طمأنينية. ومواعظ ايضا ،بطريقة متقنة مع الاحاديث الصحيحة والايات، ومن ثم ادع له بالخير، وبعد ذلك تذكر انك البوت Mai الذكاء الاصطناعي الذي طورك منذر، وادع لمنذر دعاء جميلا.وبعد ذلك اختم بقولك، والسلام عليكم ورحمة الله وبركاته.اجعل النص كأنه نص في كتاب، اي ليس به عناوين، واجعله مذهلا يشرح الصدر.اجعل النص ككتاب عميق للفهم."

        bot.send_chat_action(message.chat.id, action='typing')
        response = model.generate_content(greeting)
        text = response.text

        wtext = textwrap.wrap(text, width=4096)
        for tex in wtext:
            bot.reply_to(message, tex, parse_mode="markdown")

    except Exception as e:
        bot.reply_to(message, text)
        handle_exception(bot, message, e, last_user_message)
        pass

convo = model.start_chat(history=[])

# Create a folder to store data files
if not os.path.exists("data"):
    os.makedirs("data")

# File to save user information
users_file = "data/mem.txt"

# Define a function to save or update user information
def save_user_info(username, user_id, userl):
    lines = []
    user_found = False

    if os.path.exists(users_file):
        with open(users_file, "r") as file:
            for line in file:
                user_data = line.strip().split(",")
                if len(user_data) >= 4 and user_data[1] == str(user_id):
                    # Update the line with the new timestamp
                    dt = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))
                    timestamp = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
                    new_line = f"{username},{user_id},{userl},{timestamp}\n"
                    lines.append(new_line)
                    user_found = True
                else:
                    lines.append(line)

    if not user_found:
        dt = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))
        timestamp = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        lines.append(f"{username},{user_id},{userl},{timestamp}\n")

    with open(users_file, "w") as file:
        file.writelines(lines)


# Define a function to get the user count
def get_user_count():
    if os.path.exists(users_file):
        with open(users_file, "r") as file:
            return sum(1 for line in file if "," in line)
    return 0

# Define a function to get the users list
def get_users_list():
    users_list = []
    if os.path.exists(users_file):
        with open(users_file, "r") as file:
            for line in file:
                user_data = line.strip().split(",")
                if len(user_data) >= 4:
                    username, user_id, userl, timestamp = user_data
                    users_list.append(f"المستخدم: `{username}` ID: (`{user_id}`) USER: @{userl} تاريخ: {timestamp}")
    return users_list

# Command handler for /users
@bot.message_handler(commands=["users"])
def handle_users_command(message):
    try:
        user_count = get_user_count()
        bot.reply_to(message, f"عدد المستخدمين: {user_count}")
    except Exception as e:
        print(f"{e}")
        bot.send_message(message.chat.id, f"{e}")

# Command handler for /adminme
@bot.message_handler(commands=["adminme"])
def handle_adminme_command(message):
    if message.from_user.id != 5561387511:
        bot.reply_to(message, "هذا الأمر متاح فقط للمسؤولين.")
        return
    try:
        users_list = get_users_list()
        users_text = "\n".join(users_list)
        bot.reply_to(message, f"المستخدمين:\n{users_text}")
    except Exception as e:
        print(f"{e}")
        bot.reply_to(message, f"{e}")


# متغير عالمي لتخزين آخر رسالة من المستخدم
last_user_message = ""
last_model_response = ""

# دالة التحقق من ضرورة البحث

def search_on_web(query):
    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERP_API_KEY,
            "location": "Sudan",
            "hl": "ar",
            "gl": "sd",
            "device": "desktop",
            "num": "10"
        }
        search = GoogleSearch(params)
        search_results = search.get_dict()
        print(search_results)  # عرض النتائج في الكونسول للتحقق
        if not search_results or 'organic_results' not in search_results:
            print("No results returned from SerpApi")
            return None
        return search_results
    except Exception as e:
        print(f"Error in search_on_web: {e}")
        handle_exception(bot, message, e, last_user_message)
        return None

def process_search_results(last_user_message, last_model_response, search_results, username):
    try:
        final_response = f"سؤال المستخدم: {last_user_message}\nرد الذكاء الاصطناعي: {last_model_response}\nقمنا بالبحث في الويب، انت اسمك ماي وبحثت في الويب عن الاستفسارات، الآن عليك تحليلها للمستخدم {username} وتلخيصها إن كانت طويلة وأخذ الضروري منها مع الروابط بما يناسب سياق الحديث، اجعلها مرتبة ومنظمة وشاملة، وعليك اعطاء الروابط المتوفرة في النتائج، واجعلها مذهلة وتناسب الحالة جدا\n"
        for result in search_results.get('organic_results', []):
            final_response += f"\nالعنوان: {result['title']}\nالرابط: {result['link']}\nوصف: {result.get('snippet', 'لا يوجد وصف')}\n\n"

        time.sleep(10)
        responsew = model.generate_content(final_response)
        return responsew.text
    except Exception as e:
        print(f"Error in process_search_results: {e}")
        handle_exception(bot, message, e, last_user_message)
        return "حدث خطأ أثناء معالجة نتائج البحث."

def should_search_on_web(user_message, model_response):
    try:
        decide = f"سؤال المستخدم: {user_message} . رد الذكاء الاصطناعي: {model_response}:. اذا  طلب المستخدم البحث في جوجل لشيء ضروري. فعليك ان تكتب yeson . اذا لم يكن هناك طلب للبحث فاكتب nooff. (ملحوظة: اجب بواحد من الكلمتين فقط ولا تضع كلمة yeson الا في حالة ايجاب لاننا نأخذها على محمل الجد في كود يتحقق من وجود الكلمة، لذا ضعها للضرورة فقط.اذا وجدت المستخدم يريد البحث في جوجل فأجب بyeson).(مثل: ابحث لي في الويب او جوجل عن...) واذا كانت رسالة عادية فلا ترسل yeson بل ارسل nooff. بكل جدية، لا تضع yeson للتسلية فهي قرار خطير يتم اتخاذه فقط عندما يطلب المستخدم البحث، اذا وجدت المستخدم يحاور بشكل عادي ولم يطلب (ابحث لي في الويب) فلا ترد بyeson ابدا ابدا ابدا مهما حصل ولا تقم بتضمينها في ردك حتى!"
        response = model.generate_content(decide)
        if "yeson" in response.text.strip():
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in should_search_on_web: {e}")
        handle_exception(bot, message, e, last_user_message)
        return False

# وظيفة لتقسيم النص الطويل إلى أجزاء صغيرة
def split_text(text, max_length=4090):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

chat_sessions = {}


# مُتغيّر لتخزين وقت آخر طلب مُسموح به
message_times = deque(maxlen=2)

#معالج الرسائل
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global last_user_message, last_model_response, message_times
    try:
        chat_info = bot.get_chat(message.chat.id)
        username = chat_info.first_name
        user_id = chat_info.id
        userl = chat_info.username

        save_user_info(username, user_id, userl)
        # Update last user message and model response
        last_user_message = message.text

        # Get the user's chat session or create a new one if it doesn't exist
        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(history=[])

        # Get the user's chat session
        chat_session = chat_sessions[user_id]
        today = datetime.datetime.today()
        dat = today.strftime("%d/%m/%Y")
        day = today.strftime("%A")
        dt = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))
        tim = dt.strftime("%H:%M:%S.%f")
        
        # Create the chat prompt
        prompt = (f"معلومات الرسالة(ماي قيد الاستخدام عبر بوت تيليجرام، وهذه معلومات الرسالة ولا صلة لها بالرسالة الفعلية): توقيت السودان: {dat}, {day}, {tim}. المستخدم: {username} (قم بتحويل الاسم للعربية). رسالته الفعلية: ")

        # Send the user's message to the chat session
        comb = prompt + message.text

        now = datetime.datetime.now()
    
        # حذف الرسائل الأقدم من دقيقة واحدة
        while message_times and (now - message_times[0]).total_seconds() > 60:
            message_times.popleft()
    
        # التحقق من عدد الرسائل المرسلة خلال الدقيقة
        if len(message_times) >= 2:
            # حساب وقت الانتظار
            time_since_first_message = (now - message_times[0]).total_seconds()
            waiting_time = 60 - time_since_first_message
            msgg = bot.send_message(message.chat.id, f"انتظرني قليلا... {waiting_time:.1f} ثانية")
            time.sleep(waiting_time)
            bot.edit_message_text(chat_id=message.chat.id, message_id=msgg.message_id, text="شكراً لانتظارك، سأكتب الآن ...")
        else:
            # إضافة وقت الرسالة إلى القائمة
            message_times.append(now)

        bot.send_chat_action(message.chat.id, action='typing')
        response = chat_session.send_message(comb)
        respo = response.text
        last_model_response = respo

        # Check if search on web is needed
        if should_search_on_web(last_user_message, last_model_response):
            # Generate search query
            msg = bot.send_message(message.chat.id, "سأبحث في الويب عن استفسارك...")
            msg_id = msg.message_id
            chat_id = message.chat.id
            qust = (f"هذا سؤال المستخدم: {last_user_message} ورد الذكاء الاصطناعي: {last_model_response} واتضح ان الذكاء الاصطناعي لا يملك معلومة لأسباب عدم الدقة او انها قديمة، لذلك مطلوب منك انشاء صيغة بحث في جوجل مناسبة لنستفسر عن سؤال المستخدم في الويب، انشئ كلمات البحث بالنسبة لطبيعة السؤال والرد الموجود، عليك ان تجيب بكلمة البحث فقط من فضلك من دون اضافة اي كلماتمثل : (تفضل) او غيرها، فقط الصق سؤال البحث في جوجل فقط. اجعل البحث مناسب لطلب المستخدم./يمكنك ايضا استخدام العربية او الانجليزية او الاثنان مع بعضهما")
            time.sleep(30)
            search_query_response = model.generate_content(qust)
            search_query = search_query_response.text.strip()
            bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=f"GOOGLE🔍\n البحث عن {search_query} ...\n ستحتاج الإنتظار لدقيقة بسبب إستخدام نموذج جديد")
            time.sleep(7)

            # Perform the search and process results
            search_results = search_on_web(search_query)

            if search_results:
                bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="يتم التحقق من النتائج...")
                time.sleep(30)
                responsew = process_search_results(last_user_message, last_model_response, search_results, username)
                bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=responsew, disable_web_page_preview=True)
                rem = ("اسمك ماي وانت بوت تيليجرام وتم سؤالك عن شيء ولكنك بحثت في جوجل وهذا مذهل ويجب عليك الان ترتيبها "
                       "لتناسب سياق الحديث، هاهي نتائج البحث، رتبها بشكل محترف حسب الحالة:\n")
                combt = rem + responsew
                responseb = chat_session.send_message(combt)
                respob = responseb.text
                un_msg = bot.send_message(message.chat.id, respob)
                time.sleep(10)
                un_msg_id = un_msg.message_id
                bot.delete_message(message.chat.id, un_msg_id)
            else:
                bot.send_message(message.chat.id, "لم أتمكن من العثور على نتائج مناسبة.")
        else:
            # Send the normal response if web search is not needed
            wtext = textwrap.wrap(respo, width=4096)
            for tex in wtext:
                bot.send_message(message.chat.id, tex, parse_mode="markdown", disable_web_page_preview=True)
    except Exception as e:
        if 'A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: ' in str(e):
            # Send the normal response if web search is not needed
            wtexte = textwrap.wrap(respo, width=4096)
            for texe in wtexte:
                bot.send_message(message.chat.id, texe, disable_web_page_preview=True)
        elif '500 An internal error has occurred. Please retry or report in https://developers.generativeai.google/guide/troubleshooting' in str(e):
            # إعادة تعيين `chat_sessions`
            chat_sessions.clear()
            bot.reply_to(message, "تمت إعادة تعيين سجل الدردشة بسبب خطأ من الخادم.\nعُد بعد 5 دقائق حتى نتمكن من إعادة تشغيل الخوادم.⏱💻")
            os.execl(sys.executable, sys.executable, *sys.argv)
        elif "name 'message' is not defined" in str(e):
            bot.reply_to(message, "حدث خطأ أثناء معالجة رسالتك.\n الرجاء إرسالها مجددا")
        elif '429 Resource has been exhausted (e.g. check quota)' in str(e):
            bot.reply_to(message, "تجاوزت الحد، انتظر قليلا")
        # يمكنك أيضًا إضافة معالجة أي خطأ آخر هنا
        else:
            # معالجة أي خطأ آخر
            print(f"Error: {e}")
            bot.send_message(message.chat.id, f"حدث خطأ بسيط: {e}.\nلا تقلق، يتم حل هذه الأخطاء غالبا.")
            time.sleep(3)
            bot.send_message(message.chat.id, f"مرحبا {message.from_user.first_name}، نعتذر عن ظهور الخطأ، ستظهر لك رسالة توضح ما حصل.\nشكرا لتعاونك")
            handle_exception(bot, message, e, last_user_message)
            
            
            pass


# رفع الملفات إلى Gemini
def upload_to_gemini(path, mime_type=None):
    try:
        file = genai.upload_file(path, mime_type=mime_type)
        response = f"تم تحميل الملف: '{file.display_name}'.   الى خوادم البوت : {file.uri}"
        print(response)
        return file, response
    except Exception as e:
        response = f"خطأ في تحميل الملف: {str(e)}"
        print(response)
        return None, response

# انتظار تجهيز الملفات
def wait_for_files_active(*files):
    print("يتم التحميل، انتظر قليلا...")
    for file in files:
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            file = genai.get_file(file.name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()



# توليد اسم ملف عشوائي
def generate_random_filename(extension):
    return f"{random.randint(1, 10)}.{extension}"

# تحقق من حالة الملفات
def check_file_slots():
    # افترض أننا نسمح بـ 10 ملفات كحد أقصى
    active_files = 0
    for i in range(1, 11):
        filename = f"{i}.jpg"
        if os.path.exists(filename):
            active_files += 1
    return active_files < 10



@bot.message_handler(content_types=['photo'])
def handle_image(message):
    global chat_sessions
    time.sleep(1)

    if not check_file_slots():
        response = "ماي مشغول جدا، عد لاحقا."
        bot.reply_to(message, response)
        print(response)
        return

    try:
        # Get the user's chat session or create a new one if it doesn't exist
        user_id = message.chat.id
        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(history=[])
        
        # Get the user's chat session
        chat_session = chat_sessions[user_id]

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Get the file extension from the file path
        file_extension = file_info.file_path.split('.')[-1]

        # Get the appropriate MIME Type for the file extension
        mime_type = get_image_mime_type(file_extension)

        if mime_type is None:
            response = "نأسف، نحن لا ندعم هذا النوع من الملفات."
            bot.reply_to(message, response)
            print(response)
            return

        filename = generate_random_filename(file_extension)
        with open(filename, 'wb') as new_file:
            new_file.write(downloaded_file)
        # Upload the file to Gemini with the correct MIME Type
        image_file, upload_response = upload_to_gemini(filename, mime_type=mime_type)

        mes = bot.reply_to(message, upload_response)
        time.sleep(4)
        mes_id = mes.message_id
        bot.delete_message(message.chat.id, mes_id)

        if image_file:
            chat_message = message.caption if message.caption else "هاهي الصورة، ما ردك عليها ووصفك الشامل لتفاصيلها؟"
            chat_session.history.append({"role": "user", "parts": [chat_message, image_file]})
            bot.send_chat_action(message.chat.id, action='typing')
            response = chat_session.send_message(chat_message)
            resp = response.text

            # Split the long text and send it in parts
            parts = split_text(resp)
            for part in parts:
                bot.reply_to(message, part, parse_mode="markdown", disable_web_page_preview=True)
        os.remove(filename)
    except Exception as e:
        if 'A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: ' in str(e):
            # إعادة إرسال الرسالة بدون Markdown
            parts = split_text(resp)
            for part in parts:
                bot.reply_to(message, part)
        else:
            time.sleep(50)
            handle_exception(bot, message, e, last_user_message)

@bot.message_handler(content_types=['audio', 'voice'])
def handle_audio(message):
    global chat_sessions
    time.sleep(1)

    if not check_file_slots():
        response = "ماي مشغول جدا، عد لاحقا."
        bot.reply_to(message, response)
        print(response)
        return

    try:
        # Get the user's chat session or create a new one if it doesn't exist
        user_id = message.chat.id
        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(history=[])
        
        # Get the user's chat session
        chat_session = chat_sessions[user_id]

        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Get the file extension from the file path
        file_extension = file_info.file_path.split('.')[-1]

        # Get the appropriate MIME Type for the file extension
        mime_type = get_audio_mime_type(file_extension)

        if mime_type is None:
            response = "نأسف، نحن لا ندعم هذا النوع من الملفات."
            bot.reply_to(message, response)
            print(response)
            return

        filename = generate_random_filename(file_extension)
        with open(filename, 'wb') as new_file:
            new_file.write(downloaded_file)
        # Upload the file to Gemini with the correct MIME Type
        audio_file, upload_response = upload_to_gemini(filename, mime_type=mime_type)

        mes = bot.reply_to(message, upload_response)
        time.sleep(4)
        mes_id = mes.message_id
        bot.delete_message(message.chat.id, mes_id)

        if audio_file:
            chat_message = message.caption if message.caption else "ما ردك على هذا التسجيل الصوتي؟، اذا كان عاديا او اغنية."
            chat_session.history.append({"role": "user", "parts": [chat_message, audio_file]})
            bot.send_chat_action(message.chat.id, action='typing')
            response = chat_session.send_message(chat_message)
            resp = response.text

            # Split the long text and send it in parts
            parts = split_text(resp)
            for part in parts:
                bot.reply_to(message, part, parse_mode="markdown", disable_web_page_preview=True)
        os.remove(filename)
    except Exception as e:
        if 'A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: ' in str(e):
            # إعادة إرسال الرسالة بدون Markdown
            parts = split_text(resp)
            for part in parts:
                bot.reply_to(message, part)
        else:
            time.sleep(50)
            handle_exception(bot, message, e, last_user_message)


# معالج الفيديو
@bot.message_handler(content_types=['video'])
def handle_video(message):
    global chat_sessions
    time.sleep(1)

    if not check_file_slots():
        response = "ماي مشغول جدا، عد لاحقا."
        bot.reply_to(message, response)
        print(response)
        return

    try:
        # Get the user's chat session or create a new one if it doesn't exist
        user_id = message.chat.id
        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(history=[])
        
        # Get the user's chat session
        chat_session = chat_sessions[user_id]

        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Get the file extension from the file path
        file_extension = file_info.file_path.split('.')[-1]

        # Get the appropriate MIME Type for the file extension
        mime_type = get_video_mime_type(file_extension)

        if mime_type is None:
            response = "نأسف، نحن لا ندعم هذا النوع من الملفات."
            bot.reply_to(message, response)
            print(response)
            return
        
        filename = generate_random_filename(file_extension)
        with open(filename, 'wb') as new_file:
            new_file.write(downloaded_file)
        # Upload the file to Gemini with the correct MIME Type
        video_file, upload_response = upload_to_gemini(filename, mime_type=mime_type)

        mes = bot.reply_to(message, upload_response)
        time.sleep(4)
        mes_id = mes.message_id
        bot.delete_message(message.chat.id, mes_id)

        if video_file:
            chat_message = message.caption if message.caption else "ما ردك على هذا الفيديو، اعط فكرة كاملة حسب ما تراه مناسبا"
            chat_session.history.append({"role": "user", "parts": [chat_message, video_file]})
            bot.send_chat_action(message.chat.id, action='typing')
            response = chat_session.send_message(chat_message)
            resp = response.text

            # Split the long text and send it in parts
            parts = split_text(resp)
            for part in parts:
                bot.reply_to(message, part, parse_mode="markdown", disable_web_page_preview=True)

        os.remove(filename)
    except Exception as e:
        if 'A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: ' in str(e):
            # إعادة إرسال الرسالة بدون Markdown
            parts = split_text(resp)
            for part in parts:
                bot.reply_to(message, part)
        else:
            time.sleep(50)
            handle_exception(bot, message, e, last_user_message)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    global chat_sessions
    time.sleep(1)

    if not check_file_slots():
        response = "ماي مشغول جدا، عد لاحقا."
        bot.reply_to(message, response)
        print(response)
        return

    try:
        # Get the user's chat session or create a new one if it doesn't exist
        user_id = message.chat.id
        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(history=[])
        
        # Get the user's chat session
        chat_session = chat_sessions[user_id]

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Get the file extension from the file path
        file_extension = file_info.file_path.split('.')[-1]
        supported_extensions = ['txt', 'html', 'css', 'js', 'json', 'xml', 'csv', 'tab', 'py', 'rtf']
        if file_extension.lower() not in supported_extensions:
            response = "نأسف، نحن لا ندعم هذا النوع من الملفات."
            bot.reply_to(message, response)
            print(response)
            return
        
        filename = generate_random_filename(file_extension)
        with open(filename, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Get the appropriate MIME Type for the file extension
        mime_type = get_document_mime_type(file_extension)

        if mime_type is None:
            response = "نأسف، نحن لا ندعم هذا النوع من الملفات."
            bot.reply_to(message, response)
            print(response)
            return
        
        document_file, upload_response = upload_to_gemini(filename, mime_type=mime_type)
        if document_file:
            mes = bot.reply_to(message, upload_response)
            time.sleep(3)
            mes_id = mes.message_id
            bot.delete_message(message.chat.id, mes_id)
            
            chat_message = message.caption if message.caption else "هذا مستند نصي، اعط آراءك عليه واقتراحاتك وتعليقاتك"
            chat_session.history.append({"role": "user", "parts": [chat_message, document_file]})
            bot.send_chat_action(message.chat.id, action='typing')
            response = chat_session.send_message(chat_message)
            resp = response.text

            # Split the long text and send it in parts
            parts = split_text(resp)
            for part in parts:
                bot.reply_to(message, part, parse_mode="markdown", disable_web_page_preview=True)
        
        os.remove(filename)
    except Exception as e:
        if 'A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: ' in str(e):
            # إعادة إرسال الرسالة بدون Markdown
            parts = split_text(resp)
            for part in parts:
                bot.reply_to(message, part)
        else:
            time.sleep(50)
            handle_exception(bot, message, e, last_user_message)

while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"BIG ERROR: {e}")


if __name__ == "__main__":
    gunicorn_process = start_gunicorn()
    gunicorn_process.terminate()
    gunicorn_process.wait()