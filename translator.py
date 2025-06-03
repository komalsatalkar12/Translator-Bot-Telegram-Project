    # translator.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from deep_translator import GoogleTranslator

# Dictionary of supported languages with their codes and display names
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'zh': 'Chinese',
    'hi': 'Hindi',
    'ar': 'Arabic'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌍 Welcome to the Translation Bot!\n\n"
        "Use /selectlang to choose target language\n"
        "Then just send me any text to translate!"
    )

async def select_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create buttons in rows of 2
    buttons = []
    lang_codes = list(LANGUAGES.keys())
    
    for i in range(0, len(lang_codes), 2):
        row = []
        if i < len(lang_codes):
            code = lang_codes[i]
            row.append(InlineKeyboardButton(LANGUAGES[code], callback_data=code))
        if i+1 < len(lang_codes):
            code = lang_codes[i+1]
            row.append(InlineKeyboardButton(LANGUAGES[code], callback_data=code))
        buttons.append(row)
    
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Please select target language:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Store selected language in user context
    lang_code = query.data
    context.user_data['target_lang'] = lang_code
    context.user_data['lang_name'] = LANGUAGES.get(lang_code, lang_code)
    
    await query.edit_message_text(
        f"✅ Language set to: {LANGUAGES.get(lang_code, lang_code)}\n"
        "Now send me any text and I'll translate it for you!"
    )

async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'target_lang' not in context.user_data:
        await update.message.reply_text("Please select a language first using /selectlang")
        return
    
    text_to_translate = update.message.text
    target_lang = context.user_data['target_lang']
    lang_name = context.user_data['lang_name']
    
    try:
        # Detect source language automatically and translate to target
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text_to_translate)
        
        await update.message.reply_text(
            f"🌐 Translation to {lang_name}:\n\n{translated}"
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ Translation failed. Error: {str(e)}\n"
            "Please try again or select another language."
        )

def main():
    # Create the Application with your bot token
    application = Application.builder().token("7726143990:AAFXS3GJP-cyliA-3O15fCw9dJHDJVJmcu4").build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("selectlang", select_lang))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))
    
    # Run the bot
    print("Translation Bot is running...")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )
    

if __name__ == "__main__":
    main()