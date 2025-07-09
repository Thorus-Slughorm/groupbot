import logging
import datetime
import asyncio
import os
from telegram import Update, ChatAdministratorRights
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === CONFIG ===
BOT_TOKEN = os.getenv("2038791818:AAGPsmMabUdGJROMQAHhAipuVKNmS0ut4aw")  # Loaded from Render environment
WAIT_TIME = 3  # seconds between group creations
TOTAL_GROUPS = 50

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Send /create50 and I’ll generate 50 supergroups just for you."
    )

# /create50
async def create50(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    await update.message.reply_text(f"🛠 Creating {TOTAL_GROUPS} supergroups...")

    for i in range(1, TOTAL_GROUPS + 1):
        group_title = f"{date_str}_Group_{i}"
        try:
            # Create group with bot + user
            group = await context.bot.create_chat(title=group_title, members=[user.id])

            # Promote user to full admin
            await context.bot.promote_chat_member(
                chat_id=group.id,
                user_id=user.id,
                privileges=ChatAdministratorRights(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_invite_users=True,
                    can_change_info=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                    is_anonymous=False
                )
            )

            # Create group invite link
            invite_link = await context.bot.create_chat_invite_link(chat_id=group.id)

            # Leave the group
            await context.bot.leave_chat(chat_id=group.id)

            # Send link to user
            await update.message.reply_text(f"✅ Group {i}: {group_title}\n🔗 {invite_link.invite_link}")

        except Exception as e:
            logger.error(f"❌ Error in group {i}: {e}")
            await update.message.reply_text(f"❌ Failed to create Group {i}: {str(e)}")

        await asyncio.sleep(WAIT_TIME)

    await update.message.reply_text("🎉 Done! All 50 groups created.")

# === MAIN ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("create50", create50))
    print("🤖 Bot is running...")
    app.run_polling()
