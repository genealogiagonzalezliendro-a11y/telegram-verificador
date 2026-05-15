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
            "🔒 Bienvenido al sistema de verificación de LOS COMUNES.\n\n"
    "Este proceso es obligatorio para ingresar al grupo.\n\n"

    "La información enviada será revisada manualmente por una persona.\n"
    "No envíes información falsa, memes, contenido inválido o cualquier cosa fuera de los requisitos.\n\n"

    "Las solicitudes inválidas serán rechazadas y el usuario podrá ser baneado de la federación de grupos.\n\n"
            
            "PARA COMENZAR DIME TU EDAD👀"
        ),

        "ask_video": (
            "Perfecto.\n\n"
            "Ahora enviá un VIDEO DESNUDO permanente parado "
            "haciendo estas señas con las manos:\n"
            "👌🤟"
        ),

        "invalid_video": "Tenés que enviar un video válido.",

        "sent": "Solicitud enviada para revisión.",

        "approved": "Tu solicitud fue aprobada.",

        "rejected": "Tu solicitud fue rechazada.",
    },

    "en": {
        "welcome": (
            "🔒 Welcome to the LOS COMUNES verification system.\n\n"
    "This process is mandatory to join the group.\n\n"

    "The submitted information will be manually reviewed by a real person.\n"
    "Do not send fake information, memes, invalid content or anything unrelated to the requirements.\n\n"

    "Invalid requests will be rejected and the user may be banned from the federation of groups.\n\n"
            
            "TO BEGIN, TELL YOUR AGE 👀"
        ),

        "ask_video": (
            "Perfect.\n\n"
            "Now send a permanent  NAKED VIDEO standing up "
            "doing these hand signs:\n"
            "👌🤟"
        ),

        "invalid_video": "You must send a valid video.",

        "sent": "Request sent for review.",

        "approved": "Your request was approved.",

        "rejected": "Your request was rejected.",
    },

    "pt": {
        "welcome": (
             "🔒 Bem-vindo ao sistema de verificação do LOS COMUNES.\n\n"
    "Este processo é obrigatório para entrar no grupo.\n\n"

    "As informações enviadas serão revisadas manualmente por uma pessoa real.\n"
    "Não envie informações falsas, memes, conteúdo inválido ou qualquer coisa fora dos requisitos.\n\n"

    "Solicitações inválidas serão rejeitadas e o usuário poderá ser banido da federação de grupos.\n\n"
            
            "PARA COMEçAR, DIGA SUA IDADE👀"
        ),

        "ask_video": (
            "Perfeito.\n\n"
            "Agora envie um VÍDEO NU permanente em pé "
            "fazendo estes sinais:\n"
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
        ~filters.COMMAND,
        handle_message
    )
)

app.add_handler(CommandHandler("aprobar", aprobar))
app.add_handler(CommandHandler("rechazar", rechazar))

print("Bot iniciado...")

app.run_polling()
