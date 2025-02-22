from django import template
from datetime import datetime

register = template.Library()

@register.filter
def format_time(time_str):
    """Convert 24-hour time string to 12-hour AM/PM format"""
    try:
        time_obj = datetime.strptime(time_str, '%H:%M')
        return time_obj.strftime('%I:%M %p').lstrip('0')
    except:
        return time_str
