from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from app.database import supabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def check_assignment_reminders():
    """Check for assignments due in 2 days and send reminders to students"""
    try:
        today = datetime.now().date()
        two_days_from_now = (datetime.now() + timedelta(days=2)).date()
        
        # Get assignments due in 2 days
        assignments = supabase.table("assignments").select("*").eq("due_date", two_days_from_now.isoformat()).execute()
        
        if not assignments.data:
            logger.info("No assignments due in 2 days")
            return
        
        logger.info(f"Found {len(assignments.data)} assignments due in 2 days")
        
        for assignment in assignments.data:
            # Get students who haven't submitted
            student_assignments = supabase.table("student_assignments").select("student_id").eq("assignment_id", assignment["id"]).eq("submitted", False).execute()
            
            if student_assignments.data:
                logger.info(f"Assignment '{assignment['title']}' has {len(student_assignments.data)} pending submissions")
                
                # Here you would typically send notifications
                # This could be push notifications, emails, or in-app notifications
                # For now, we'll just log the reminders
                for sa in student_assignments.data:
                    logger.info(f"Reminder: Student {sa['student_id']} - Assignment '{assignment['title']}' due in 2 days")
                    
                    # Create a notification record
                    notification_data = {
                        "student_id": sa["student_id"],
                        "assignment_id": assignment["id"],
                        "message": f"Assignment '{assignment['title']}' is due in 2 days!",
                        "created_at": datetime.now().isoformat()
                    }
                    supabase.table("notifications").insert(notification_data).execute()
                    
    except Exception as e:
        logger.error(f"Error checking assignment reminders: {str(e)}")


def start_scheduler():
    """Start the background scheduler"""
    # Run the reminder check every day at 9 AM
    scheduler.add_job(
        check_assignment_reminders,
        trigger=IntervalTrigger(hours=24),
        id="assignment_reminder_job",
        name="Check assignment reminders",
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Scheduler started successfully")


def shutdown_scheduler():
    """Shutdown the scheduler"""
    scheduler.shutdown()
    logger.info("Scheduler shut down")
