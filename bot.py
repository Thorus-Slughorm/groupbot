import logging
import datetime
import asyncio
from telegram import Update, ChatAdministratorRights
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === CONFIG ===
BOT_TOKEN = "2038791818:AAGPsmMabUdGJROMQAHhAipuVKNmS0ut4aw"  # Replace this with your actual bot token
WAIT_TIME = 3  # seconds between group creations
TOTAL_GROUPS = 50

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to the SuperGroup Generator Bot!\n"
        "Send /create50 and I will create 50 Telegram supergroups for you, "
        "name them by today’s date, and give you full admin access."
    )

# /create50 handler
async def create50(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    await update.message.reply_text(f"🚀 Creating {TOTAL_GROUPS} supergroups for you...")

    for i in range(1, TOTAL_GROUPS + 1):
        group_title = f"{date_str}_Group_{i}"
        try:
            # Create a group with bot + user
            group = await context.bot.create_chat(title=group_title, members=[user.id])

            # Promote the user to full admin
            await context.bot.promote_chat_member(
                chat_id=group.id,
                user_id=user.id,
                privileges=ChatAdministratorRights(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_change_info=True,
                    can_promote_members=True,
                    is_anonymous=False
                )
            )

            # Create invite link
            invite_link = await context.bot.create_chat_invite_link(chat_id=group.id)

            # Leave the group to make the user feel like the owner
            await context.bot.leave_chat(chat_id=group.id)

            # Send the group link to the user
            await update.message.reply_text(f"✅ Group {i}: {group_title}\n🔗 {invite_link.invite_link}")

        except Exception as e:
            logger.error(f"Error creating group {i}: {e}")
            await update.message.reply_text(f"❌ Failed to create Group {i}: {str(e)}")

        await asyncio.sleep(WAIT_TIME)

    await update.message.reply_text("🎉 Done! All 50 groups have been created and sent to you.")

# === MAIN ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("create50", create50))

    print("🤖 Bot is running...")
    app.run_polling()
