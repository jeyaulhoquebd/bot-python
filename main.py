import logging
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# বট টোকেন সরাসরি সেট করুন
BOT_TOKEN = "8550627399:AAGV4Nl1Thtqnbbo3Ys3sT2ZiojA52hWva8"

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ওয়েবসাইট থেকে পোস্ট ডেটা ফেচ করার ফাংশন
def get_website_posts():
    try:
        posts = [
            "📖 কুরআন অধ্যয়ন: সূরা আল-ফাতিহার তাফসীর",
            "🤲 দৈনিক দোয়া: আজকের বিশেষ দোয়া",
            "📚 হাদিস শিক্ষা: রোজার গুরুত্ব সম্পর্কিত হাদিস",
            "💡 ইসলামিক জ্ঞান: যাকাতের নিয়মাবলী",
            "🎧 অডিও লেকচার: ইসলামে পরিবারের গুরুত্ব",
            "📝 ব্লগ: আধুনিক সমস্যার ইসলামিক সমাধান"
        ]
        return posts
    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        return ["ওয়েবসাইট থেকে পোস্ট লোড করতে সমস্যা হচ্ছে।"]

# সাহায্য মেনু
async def show_help(query):
    help_text = """
🆘 **সাহায্য কেন্দ্র**

📌 **বট ব্যবহার:**
• /start - বট পুনরায় শুরু করুন
• ভাষা পরিবর্তন করতে "ভাষা পরিবর্তন" বাটন ব্যবহার করুন

🔧 **সমস্যা সমাধান:**
• যদি বাটন কাজ না করে, /start কমান্ড দিন
• কোনো সমস্যা হলে Admin-কে Contact করুন

📞 **Contact:**
Email: ofthequran2025@gmail.com
    """
    
    keyboard = [
        [InlineKeyboardButton("🔙 মূল মেনু", callback_data="bangla")],
        [InlineKeyboardButton("🏠 হোম", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')

# About মেনু
async def show_about(query):
    about_text = """
🕌 **কুরআন ডিসকাশন বট সম্পর্কে**

**Our Mission:**
ইসলামিক জ্ঞান সহজভাবে মানুষের কাছে পৌঁছে দেওয়া।

**সেবাসমূহ:**
• 📖 কুরআন শিক্ষা
• 📚 হাদিস Study
• 🤲 দৈনিক দোয়া
• 💡 ইসলামিক Guidance

**Developer:** Quran Discussion Team
**Website:** https://dev-discussionquran.pantheonsite.io/
    """
    
    keyboard = [
        [InlineKeyboardButton("🌐 আমাদের ওয়েবসাইট", url="https://dev-discussionquran.pantheonsite.io/")],
        [
            InlineKeyboardButton("🔙 মূল মেনু", callback_data="bangla"),
            InlineKeyboardButton("🏠 হোম", callback_data="back_to_main")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(about_text, reply_markup=reply_markup, parse_mode='Markdown')

# বাংলা মেনু দেখানো
async def show_main_menu_bangla(query):
    menu_text = """
🌙 **স্বাগতম! কুরআন ডিসকাশন বটে**

নিচের অপশনগুলো থেকে আপনার পছন্দের সেবা নির্বাচন করুন:

✨ **আমাদের সেবাসমূহ:**
• 📖 কুরআন শিক্ষা ও তাফসীর
• 📚 হাদিস Database
• 🤲 দৈনিক দোয়া ও জিকির
• 💡 ইসলামিক Guidance
• 🌐 সোশ্যাল মিডিয়া Updates
    """
    
    keyboard = [
        [
            InlineKeyboardButton("📱 সোশ্যাল মিডিয়া", callback_data="social_media"),
            InlineKeyboardButton("🌐 ওয়েবসাইট", callback_data="website")
        ],
        [
            InlineKeyboardButton("📖 কুরআন Study", callback_data="quran"),
            InlineKeyboardButton("🤲 দোয়া Collection", callback_data="dua")
        ],
        [
            InlineKeyboardButton("🔧 সাহায্য", callback_data="help"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("🔄 ভাষা পরিবর্তন", callback_data="back_to_main")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        menu_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ইংরেজি মেনু দেখানো
async def show_main_menu_english(query):
    menu_text = """
🌙 **Welcome to Quran Discussion Bot**

Please choose from our services below:

✨ **Our Services:**
• 📖 Quran Learning & Tafsir
• 📚 Hadith Database
• 🤲 Daily Duas & Zikr
• 💡 Islamic Guidance
• 🌐 Social Media Updates
    """
    
    keyboard = [
        [
            InlineKeyboardButton("📱 Social Media", callback_data="social_media"),
            InlineKeyboardButton("🌐 Website", callback_data="website")
        ],
        [
            InlineKeyboardButton("📖 Quran Study", callback_data="quran"),
            InlineKeyboardButton("🤲 Dua Collection", callback_data="dua")
        ],
        [
            InlineKeyboardButton("🔧 Help", callback_data="help"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("🔄 Change Language", callback_data="back_to_main")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        menu_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# সোশ্যাল মিডিয়া দেখানো
async def show_social_media(query):
    social_media_text = """
📱 **আমাদের সোশ্যাল মিডিয়া**

🔗 **Follow us on:**

🐦 **Twitter/X:** 
https://x.com/the_quran36741

📘 **Facebook (Coming Soon)**
📷 **Instagram (Coming Soon)**
🎥 **YouTube (Coming Soon)**

🚀 **আমাদের আরো সোশ্যাল মিডিয়া চ্যানেল খুব শীঘ্রই আসছে! ইনশাআল্লাহ**

💫 **আমাদের সাথে Connected থাকুন নিয়মিত ইসলামিক Content এর জন্য!**
    """
    
    keyboard = [
        [
            InlineKeyboardButton("🐦 Twitter Visit", url="https://x.com/the_quran36741"),
            InlineKeyboardButton("🌐 Website", callback_data="website")
        ],
        [
            InlineKeyboardButton("📖 কুরআন Study", callback_data="quran"),
            InlineKeyboardButton("🔙 মূল মেনু", callback_data="bangla")
        ],
        [
            InlineKeyboardButton("🏠 হোম", callback_data="back_to_main")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        social_media_text, 
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ওয়েবসাইট পোস্ট দেখানো
async def show_website_posts(query):
    posts = get_website_posts()
    
    posts_text = "🌐 **আমাদের ওয়েবস이트ের সর্বশেষ পোস্ট:**\n\n"
    
    for i, post in enumerate(posts[:3], 1):
        posts_text += f"**{i}. {post}**\n\n"
    
    posts_text += "🔗 **ওয়েবসাইট লিঙ্ক:** https://dev-discussionquran.pantheonsite.io/\n\n"
    posts_text += "📚 **ওয়েবসাইট ভিজিট করে আরও জ্ঞান অর্জন করুন!**"
    
    keyboard = [
        [
            InlineKeyboardButton("🌐 ওয়েবসাইট Visit", url="https://dev-discussionquran.pantheonsite.io/"),
            InlineKeyboardButton("📖 আরও পোস্ট", callback_data="more_posts")
        ],
        [
            InlineKeyboardButton("📱 সোশ্যাল মিডিয়া", callback_data="social_media"),
            InlineKeyboardButton("🔙 মূল মেনু", callback_data="bangla")
        ],
        [
            InlineKeyboardButton("🏠 হোম", callback_data="back_to_main")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        posts_text, 
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# আরও পোস্ট দেখানো
async def show_more_posts(query):
    posts = get_website_posts()
    
    posts_text = "🌐 **আমাদের ওয়েবসাইটের অন্যান্য পোস্ট:**\n\n"
    
    for i, post in enumerate(posts[3:], 4):
        posts_text += f"**{i}. {post}**\n\n"
    
    posts_text += "✨ **আরও অনেক Educational Content এর জন্য আমাদের ওয়েবসাইট Visit করুন!**"
    
    keyboard = [
        [
            InlineKeyboardButton("🌐 ওয়েবসাইট Visit", url="https://dev-discussionquran.pantheonsite.io/"),
            InlineKeyboardButton("📱 সোশ্যাল মিডিয়া", callback_data="social_media")
        ],
        [
            InlineKeyboardButton("📖 প্রথম পেজ", callback_data="website"),
            InlineKeyboardButton("🔙 মূল মেনু", callback_data="bangla")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        posts_text, 
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ভাষা সিলেকশনে ফিরে যাওয়া
async def show_language_selection(query):
    selection_text = """
🌍 **ভাষা নির্বাচন / Language Selection**

দয়া করে আপনার পছন্দের ভাষা নির্বাচন করুন:
Please choose your preferred language:

🇧🇩 **বাংলা** - Bangla
🌍 **English** - ইংরেজি
    """
    
    keyboard = [
        [
            InlineKeyboardButton("🇧🇩 বাংলা - Bangla", callback_data="bangla"),
            InlineKeyboardButton("🌍 English - ইংরেজি", callback_data="english")
        ],
        [
            InlineKeyboardButton("📞 সাহায্য - Help", callback_data="help"),
            InlineKeyboardButton("ℹ️ About - সম্পর্কে", callback_data="about")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        selection_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Quran Study Section
async def show_quran_study(query):
    quran_text = """
📖 **কুরআন Study Section**

🚧 **এই Sectionটি Development Under রয়েছে**

ইনশাআল্লাহ খুব শীঘ্রই আমরা কুরআনের বিভিন্ন সূরার তাফসীর এবং শিক্ষা Add করব।

এখনকার জন্য আমাদের Website এবং Social Media Follow করুন।
    """
    
    keyboard = [
        [
            InlineKeyboardButton("🌐 ওয়েবসাইট", callback_data="website"),
            InlineKeyboardButton("📱 সোশ্যাল মিডিয়া", callback_data="social_media")
        ],
        [
            InlineKeyboardButton("🔙 মূল মেনু", callback_data="bangla")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(quran_text, reply_markup=reply_markup, parse_mode='Markdown')

# Dua Collection
async def show_dua_collection(query):
    dua_text = """
🤲 **দোয়া Collection**

🚧 **এই Sectionটি Development Under রয়েছে**

ইনশাআল্লাহ খুব শীঘ্রই আমরা বিভিন্ন দোয়া এবং জিকির Add করব।

এখনকার জন্য আমাদের Website Visit করুন Regular Update এর জন্য।
    """
    
    keyboard = [
        [
            InlineKeyboardButton("🌐 ওয়েবসাইট Visit", url="https://dev-discussionquran.pantheonsite.io/"),
            InlineKeyboardButton("📖 কুরআন Study", callback_data="quran")
        ],
        [
            InlineKeyboardButton("🔙 মূল মেনু", callback_data="bangla")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(dua_text, reply_markup=reply_markup, parse_mode='Markdown')

# স্টার্ট কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        
        welcome_text = f"""
🕌 **আসসালামু আলাইকুম {user.first_name}!** 🤲

**কুরআন ডিসকাশন বটে** স্বাগতম! 
আপনার আধ্যাত্মিক Journey এ আমরা আপনার সাথে আছি।

নিচ থেকে আপনার পছন্দের ভাষা নির্বাচন করুন:
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🇧🇩 বাংলা - Bangla", callback_data="bangla"),
                InlineKeyboardButton("🌍 English - ইংরেজি", callback_data="english")
            ],
            [
                InlineKeyboardButton("📞 সাহায্য - Help", callback_data="help"),
                InlineKeyboardButton("ℹ️ About - সম্পর্কে", callback_data="about")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        await update.message.reply_text("❌ একটি ত্রুটি ঘটেছে। দয়া করে আবার চেষ্টা করুন।")

# বাটন ক্লিক হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    try:
        if query.data == "bangla":
            await show_main_menu_bangla(query)
        elif query.data == "english":
            await show_main_menu_english(query)
        elif query.data == "social_media":
            await show_social_media(query)
        elif query.data == "website":
            await show_website_posts(query)
        elif query.data == "back_to_main":
            await show_language_selection(query)
        elif query.data == "help":
            await show_help(query)
        elif query.data == "about":
            await show_about(query)
        elif query.data == "more_posts":
            await show_more_posts(query)
        elif query.data == "quran":
            await show_quran_study(query)
        elif query.data == "dua":
            await show_dua_collection(query)
    except Exception as e:
        logger.error(f"Error in button handler for {query.data}: {e}")
        await query.message.reply_text("❌ একটি ত্রুটি ঘটেছে। দয়া করে /start দিয়ে আবার শুরু করুন।")

# এরর হ্যান্ডলার
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception occurred:", exc_info=context.error)
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ একটি ত্রুটি ঘটেছে। অনুগ্রহ করে /start দিয়ে আবার শুরু করুন।"
            )
    except Exception as e:
        logger.error(f"Error in error handler: {e}")

# মেইন ফাংশন
def main():
    try:
        # টোকেন ভ্যালিডেশন
        if not BOT_TOKEN or "8550627399" not in BOT_TOKEN:
            print("❌ Error: Invalid BOT_TOKEN!")
            return
        
        print("🚀 বট শুরু হচ্ছে...")
        print(f"✅ টোকেন সঠিকভাবে সেট করা হয়েছে")
        
        # অ্যাপ্লিকেশন তৈরি
        application = Application.builder().token(BOT_TOKEN).build()
        
        # হ্যান্ডলার যোগ করা
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_error_handler(error_handler)
        
        logger.info("🤖 বট সফলভাবে চালু হয়েছে!")
        print("🕌 Quran Discussion Bot is now running!")
        print("📍 Press Ctrl+C to stop the bot")
        
        # বট চালু করা
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Error starting bot: {e}")

if __name__ == '__main__':
    main()