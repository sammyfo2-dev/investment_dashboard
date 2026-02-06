from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.config import get_settings

settings = get_settings()
scheduler = BackgroundScheduler()


def daily_price_update():
    """
    Update prices for all watchlist items
    Runs daily at configured hour (default 6 AM)
    """
    print(f"Running daily price update at {settings.DAILY_UPDATE_HOUR}:00...")
    # This will be implemented in Phase 5
    # For now, just a placeholder
    pass


def start_scheduler():
    """Start the background scheduler"""
    if not scheduler.running:
        # Schedule daily price update
        scheduler.add_job(
            daily_price_update,
            CronTrigger(
                hour=settings.DAILY_UPDATE_HOUR,
                minute=0,
                timezone=settings.TIMEZONE
            ),
            id='daily_price_update',
            replace_existing=True
        )

        scheduler.start()
        print(f"Scheduler started. Daily updates at {settings.DAILY_UPDATE_HOUR}:00 {settings.TIMEZONE}")


def stop_scheduler():
    """Stop the background scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        print("Scheduler stopped")
