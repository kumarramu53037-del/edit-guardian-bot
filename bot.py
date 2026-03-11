import json
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================= CONFIG =================
TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
BOT_USERNAME = os.getenv("BOT_USERNAME")
SUPPORT_LINK = os.getenv("SUPPORT_LINK")
CHANNEL_LINK = os.getenv("CHANNEL_LINK")
START_PHOTO = os.getenv("START_PHOTO")

DATA_FILE = "settings.json"
GROUPS_FILE = "groups.json"
# ==========================================

# ---------- DATA SYSTEM ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_groups():
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r") as f:
            return json.load(f)
    return []

def save_groups(groups):
    with open(GROUPS_FILE, "w") as f:
        json.dump(groups, f)

# ---------- ADMIN CHECK ----------
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id
    )
    return chat_member.status in ["administrator", "creator"]

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    keyboard = [
        [InlineKeyboardButton("💬 Support", url=f"https://t.me/{SUPPORT_LINK}")],
        [InlineKeyboardButton("📢 Update", url=f"https://t.me/{CHANNEL_LINK}")],
        [InlineKeyboardButton("✨ Add Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")]
    ]

    caption = (
        f"👋 ʜᴇʟʟᴏ {update.effective_user.first_name}\n\n"
        "🚨 ɪ ᴀᴍ ᴀɴ ᴀʙᴜsᴇ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʙᴏᴛ.\n\n"
        "⚡ ɪ ᴅᴇʟᴇᴛᴇ ᴇᴅɪᴛᴇᴅ ᴍᴇssᴀɢᴇs ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ.\n"
        "🛡 ɪ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴍᴇᴅɪᴀ / sᴛɪᴄᴋᴇʀs.\n"
        "🔐 ɪ ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ ғʀᴏᴍ ᴀʙᴜsᴇ.\n\n"
        "⭐ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ\n"
        "⭐ ɢɪᴠᴇ ᴀᴅᴍɪɴ + ᴅᴇʟᴇᴛᴇ ᴘᴇʀᴍɪssɪᴏɴ\n\n"
        "⚙️ ᴄᴏᴍᴍᴀɴᴅs:\n"
        "/set_delay <minutes>\n"
        "/get_delay\n\n"
        "📢 ᴊᴏɪɴ ᴛʜᴇ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ғᴏʀ ᴜᴘᴅᴀᴛᴇs."
    )

    await update.message.reply_photo(
        photo=START_PHOTO,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------- BOT ADDED ----------
async def bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:

            groups = load_groups()
            if update.effective_chat.id not in groups:
                groups.append(update.effective_chat.id)
                save_groups(groups)

            keyboard = [
                [InlineKeyboardButton("ᴄʟɪᴄᴋ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")]
            ]

            text = (
                "🤖 ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ!\n"
                "🛡 ɪ ᴀᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴇᴅɪᴛ ɢᴜᴀʀᴅɪᴀɴ ʙᴏᴛ.\n"
                "✨ ꜰᴇᴀᴛᴜʀᴇꜱ:\n"
                "• ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴇᴅɪᴛᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ\n"
                "• ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴇᴅɪᴀ / sᴛɪᴄᴋᴇʀs / ɢɪꜰꜱ\n"
                "• ᴡᴀʀɴɪɴɢ & ᴍᴏɴɪᴛᴏʀɪɴɢ\n"
                "• ᴅᴇʟᴀʏ ᴄᴏɴᴛʀᴏʟ & ᴀᴅᴍɪɴ ᴄᴏɴᴛʀᴏʟ\n\n"
                "⚙️ ᴜꜱᴇ /set_delay <minutes>\n"
                "📊 ᴜꜱᴇ /get_delay\n"
                "🚀 ᴋᴇᴇᴘ ɢʀᴏᴜᴘ ꜱᴀꜰᴇ!"
            )

            await update.message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

# ---------- SET DELAY ----------
async def set_delay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("❌ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘ.")
        return

    if not await is_admin(update, context):
        await update.message.reply_text("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("⚙ ᴜsᴇ: /set_delay 1")
        return

    try:
        minutes = int(context.args[0])
    except:
        await update.message.reply_text("❌ ɪɴᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ.")
        return

    data = load_data()
    chat_id = str(update.effective_chat.id)
    data[chat_id] = {"delay": minutes * 60}
    save_data(data)

    await update.message.reply_text(
        f"✅ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴅᴇʟᴀʏ sᴇᴛ ᴛᴏ {minutes} ᴍɪɴᴜᴛᴇs."
    )

# ---------- GET DELAY ----------
async def get_delay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("❌ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘ.")
        return

    if not await is_admin(update, context):
        await update.message.reply_text("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs.")
        return

    chat_id = str(update.effective_chat.id)
    data = load_data()
    delay = data.get(chat_id, {}).get("delay", 0)

    if delay == 0:
        await update.message.reply_text("⚙ ɴᴏ ᴅᴇʟᴀʏ sᴇᴛ.")
    else:
        await update.message.reply_text(
            f"⏳ ᴄᴜʀʀᴇɴᴛ ᴅᴇʟᴀʏ: {delay // 60} ᴍɪɴᴜᴛᴇs."
        )

# ---------- DELETE EDITED ----------
async def delete_edited(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.edited_message
    user = message.from_user

    try:
        await message.delete()
        mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

        await context.bot.send_message(
            chat_id=message.chat_id,
            text=f"⚠ {mention}\nʏᴏᴜʀ ᴇᴅɪᴛᴇᴅ ᴍᴇssᴀɢᴇ ʜᴀs ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ 🚫",
            parse_mode="HTML"
        )
    except:
        pass

# ---------- AUTO DELETE ----------
async def auto_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    data = load_data()
    delay = data.get(chat_id, {}).get("delay", 0)

    if delay > 0:
        await asyncio.sleep(delay)
        try:
            await update.message.delete()
        except:
            pass

# ---------- BROADCAST ----------
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Not authorized.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast Your message here")
        return

    text = " ".join(context.args)
    groups = load_groups()

    success = 0
    failed = 0

    for group_id in groups:
        try:
            await context.bot.send_message(
                chat_id=group_id,
                text=f"{text}"
            )
            success += 1
        except:
            failed += 1

    await update.message.reply_text(
        f"✅ Broadcast Done\n✔ Success: {success}\n❌ Failed: {failed}"
    )

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("set_delay", set_delay))
    app.add_handler(CommandHandler("get_delay", get_delay))
    app.add_handler(CommandHandler("broadcast", broadcast))

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bot_added))
    app.add_handler(MessageHandler(filters.Sticker.ALL, auto_delete))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.Document.ALL, auto_delete))
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE, delete_edited))

    print("Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
