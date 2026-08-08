import traceback

from telegram import Update, BotCommand

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config.settings import settings
from database.database import SessionLocal

from services.user_service import get_or_create_user

from services.conversation_service import (
    save_message,
    get_recent_messages,
)

from services.atlas_service import AtlasService


# ============================================================
# ATLAS INTELLIGENCE ENGINE
# ============================================================

atlas_service = AtlasService()


# ============================================================
# /start COMMAND
# ============================================================

async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    telegram_user = update.effective_user

    if not update.message:
        return

    db = SessionLocal()

    try:
        user = get_or_create_user(
            db=db,
            telegram_id=str(telegram_user.id),
            username=telegram_user.username,
            first_name=telegram_user.first_name,
        )

        telegram_id = str(telegram_user.id)

        save_message(
            db=db,
            telegram_id=telegram_id,
            role="user",
            message="/start",
        )

        first_name = (
            user.first_name
            or telegram_user.first_name
            or "there"
        )

        response = (
            f"Hello {first_name}! 👋\n\n"
            "I'm Atlas, your AI Financial Assistant.\n\n"
            "You can ask me naturally about:\n"
            "• Companies\n"
            "• Markets\n"
            "• Financial news\n"
            "• Financial concepts\n"
            "• Company research\n\n"
            "Commands:\n"
            "• /news — Latest financial news\n"
            "• /help — Show available commands\n\n"
            "What would you like to research today?"
        )

        save_message(
            db=db,
            telegram_id=telegram_id,
            role="assistant",
            message=response,
        )

        await update.message.reply_text(response)

    except Exception as error:

        print("\n" + "=" * 70)
        print("ATLAS /start ERROR")
        print("=" * 70)
        print(f"Error: {error}")
        traceback.print_exc()
        print("=" * 70 + "\n")

        await update.message.reply_text(
            "Atlas encountered an internal error.\n"
            "Please check the terminal for details."
        )

    finally:
        db.close()


# ============================================================
# /news COMMAND
# ============================================================

async def news_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    telegram_user = update.effective_user

    if not update.message:
        return

    db = SessionLocal()

    try:
        telegram_id = str(telegram_user.id)

        get_or_create_user(
            db=db,
            telegram_id=telegram_id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
        )

        save_message(
            db=db,
            telegram_id=telegram_id,
            role="user",
            message="/news",
        )

        print("\n" + "=" * 70)
        print("ATLAS NEWS COMMAND")
        print("=" * 70)

        print(
            f"Telegram User: "
            f"{telegram_user.username or telegram_user.id}"
        )

        print("Request: Latest financial news")

        response = atlas_service.process_message(
            user_message="Show me the latest financial news",
            conversation_history=[],
        )

        print("News response generated successfully.")
        print("=" * 70 + "\n")

        save_message(
            db=db,
            telegram_id=telegram_id,
            role="assistant",
            message=response,
        )

        await update.message.reply_text(response)

    except Exception as error:

        print("\n" + "=" * 70)
        print("ATLAS NEWS ERROR")
        print("=" * 70)
        print(f"Error: {error}")
        print("\nFULL TRACEBACK:")
        traceback.print_exc()
        print("=" * 70 + "\n")

        await update.message.reply_text(
            "📰 I couldn't retrieve the latest "
            "financial news right now.\n\n"
            "Please try again shortly."
        )

    finally:
        db.close()


# ============================================================
# /help COMMAND
# ============================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    response = (
        "🤖 Atlas — AI Financial Assistant\n\n"

        "Here are some things you can ask me:\n\n"

        "📊 Markets\n"
        "• What's Apple's stock price?\n"
        "• How is NVIDIA doing?\n"
        "• Show me Microsoft's stock price\n\n"

        "📰 Financial News\n"
        "• /news\n"
        "• Show me the latest financial news\n"
        "• What's the latest news about Apple?\n\n"

        "🏢 Company Research\n"
        "• Give me a quick rundown on Apple\n"
        "• Tell me about NVIDIA\n"
        "• What's happening with Microsoft?\n\n"

        "📚 Financial Concepts\n"
        "• What is an IPO?\n"
        "• Explain P/E ratio\n"
        "• What is market capitalization?\n\n"

        "Commands:\n"
        "/start — Start Atlas\n"
        "/news — Latest financial news\n"
        "/help — Show this help message"
    )

    await update.message.reply_text(response)


# ============================================================
# NORMAL MESSAGE HANDLER
# ============================================================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    telegram_user = update.effective_user

    if not update.message:
        return

    if not update.message.text:
        return

    db = SessionLocal()

    try:
        telegram_id = str(telegram_user.id)

        get_or_create_user(
            db=db,
            telegram_id=telegram_id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
        )

        user_message = update.message.text.strip()

        if not user_message:
            return

        # ----------------------------------------------------
        # Save user message
        # ----------------------------------------------------

        save_message(
            db=db,
            telegram_id=telegram_id,
            role="user",
            message=user_message,
        )

        # ----------------------------------------------------
        # Get conversation history
        # ----------------------------------------------------

        recent_messages = get_recent_messages(
            db=db,
            telegram_id=telegram_id,
            limit=10,
        )

        conversation_history = [
            {
                "role": message.role,
                "message": message.message,
            }
            for message in recent_messages
        ]

        # ----------------------------------------------------
        # Send message to Atlas
        # ----------------------------------------------------

        print("\n" + "=" * 70)
        print("ATLAS PROCESSING")
        print("=" * 70)

        print(
            f"User: {user_message}"
        )

        print(
            f"Telegram ID: {telegram_id}"
        )

        print(
            "Sending message to AtlasService..."
        )

        response = atlas_service.process_message(
            user_message=user_message,
            conversation_history=conversation_history,
        )

        print(
            "Atlas response generated successfully."
        )

        print("=" * 70 + "\n")

        # ----------------------------------------------------
        # Save Atlas response
        # ----------------------------------------------------

        save_message(
            db=db,
            telegram_id=telegram_id,
            role="assistant",
            message=response,
        )

        # ----------------------------------------------------
        # Send response to Telegram
        # ----------------------------------------------------

        await update.message.reply_text(
            response
        )

    except Exception as error:

        print("\n" + "=" * 70)
        print("ATLAS TELEGRAM ERROR")
        print("=" * 70)

        print(
            f"Error: {error}"
        )

        print("\nFULL TRACEBACK:")

        traceback.print_exc()

        print("=" * 70 + "\n")

        try:
            await update.message.reply_text(
                "Atlas encountered an internal error.\n\n"
                "Please check the terminal for the "
                "detailed error."
            )
        except Exception:
            pass

    finally:
        db.close()


# ============================================================
# TELEGRAM COMMAND MENU
# ============================================================

async def post_init(
    application: Application,
):
    try:
        await application.bot.set_my_commands(
            [
                BotCommand(
                    "start",
                    "Start Atlas",
                ),
                BotCommand(
                    "news",
                    "Latest financial news",
                ),
                BotCommand(
                    "help",
                    "Show help",
                ),
            ]
        )

        print(
            "Telegram command menu configured successfully."
        )

    except Exception as error:

        print(
            "Warning: Could not configure Telegram "
            f"command menu: {error}"
        )


# ============================================================
# CREATE BOT APPLICATION
# ============================================================

def create_bot() -> Application:

    if not settings.TELEGRAM_BOT_TOKEN:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN is missing from the .env file."
        )

    application = (
        Application.builder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # --------------------------------------------------------
    # /start
    # --------------------------------------------------------

    application.add_handler(
        CommandHandler(
            "start",
            start_command,
        )
    )

    # --------------------------------------------------------
    # /news
    # --------------------------------------------------------

    application.add_handler(
        CommandHandler(
            "news",
            news_command,
        )
    )

    # --------------------------------------------------------
    # /help
    # --------------------------------------------------------

    application.add_handler(
        CommandHandler(
            "help",
            help_command,
        )
    )

    # --------------------------------------------------------
    # Normal text messages
    # --------------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    return application


# ============================================================
# RUN BOT
# ============================================================

def run_bot():

    application = create_bot()

    print("\n" + "=" * 70)

    print(
        "ATLAS TELEGRAM BOT IS STARTING..."
    )

    print("=" * 70)

    print(
        "Bot is running and waiting for Telegram messages."
    )

    print(
        "Available commands:"
    )

    print(
        "  /start"
    )

    print(
        "  /news"
    )

    print(
        "  /help"
    )

    print(
        "Press Ctrl+C to stop the bot."
    )

    print("=" * 70 + "\n")

    application.run_polling(
        drop_pending_updates=True
    )


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":
    run_bot()