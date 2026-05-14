import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ChatJoinRequestHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TOKEN")

pending_users = {}

GROUP_ID = -1003968636484
ADMIN_ID = 8011642705


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot iniciado correctamente."
    )

async def idgrupo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Chat ID: {update.effective_chat.id}"
    )

async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user

    pending_users[user.id] = {
        "step": "age",
        "username": user.username,
    }

    try:
        await context.bot.send_message(
            chat_id=user.id,
            text="Hola. Para ingresar enviá tu edad."
        )
    except:
        print("El usuario no inició el bot.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in pending_users:
        return

    step = pending_users[user_id]["step"]

    if step == "age":
        pending_users[user_id]["age"] = update.message.text
        pending_users[user_id]["step"] = "photo"

        await update.message.reply_text(
            "Ahora enviá una foto verificadora."
        )

    elif step == "photo":
        if update.message.photo:
            age = pending_users[user_id]["age"]
            username = pending_users[user_id]["username"]

            await context.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=update.message.photo[-1].file_id,
                caption=(
                    f"Solicitud nueva\n\n"
                    f"Usuario: @{username}\n"
                    f"Edad: {age}\n\n"
                    f"/aprobar {user_id}\n"
                    f"/rechazar {user_id}"
                )
            )

            await update.message.reply_text(
                "Solicitud enviada para revisión."
            )

            pending_users[user_id]["step"] = "done"

        else:
            await update.message.reply_text(
                "Enviá una foto válida."
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
        "Tu solicitud fue aprobada."
    )

    await update.message.reply_text("Usuario aprobado.")


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
        "Tu solicitud fue rechazada."
    )

    await update.message.reply_text("Usuario rechazado.")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("idgrupo", idgrupo))
app.add_handler(ChatJoinRequestHandler(join_request))
app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))
app.add_handler(CommandHandler("aprobar", aprobar))
app.add_handler(CommandHandler("rechazar", rechazar))

print("Bot iniciado...")

app.run_polling()
