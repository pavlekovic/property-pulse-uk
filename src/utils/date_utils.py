from datetime import datetime, timedelta
from pathlib import Path

def last_month_ym ():
    
    # log today's date
    today = datetime.now()

    # Find first day of the current month
    first_this_month = datetime(today.year, today.month, 1)
    
    # Find the last day of the previous month by subtracting one day from first_this_month
    last_month_day = first_this_month - timedelta(days=1)
    
    # Return last month as YYYY-MM
    return last_month_day.strftime("%Y-%m")