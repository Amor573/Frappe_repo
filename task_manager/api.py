# task_manager/api.py
import frappe
from frappe import _
from frappe.utils import cint, get_datetime
import redis
import json

# Create Task
@frappe.whitelist()
def create_task(task_name, description, assigned_to, due_date, status):
    # Create a new task
    task = frappe.get_doc({
        "doctype": "Task",
        "task_name": task_name,
        "description": description,
        "assigned_to": assigned_to,
        "due_date": due_date,
        "status": status
    })
    task.insert()
    return task.as_dict()

# Read Task
@frappe.whitelist()
def get_task(task_id):
    task = frappe.get_doc("Task", task_id)
    return task.as_dict()

# Update Task
@frappe.whitelist()
def update_task(task_id, task_name, description, assigned_to, due_date, status):
    task = frappe.get_doc("Task", task_id)
    task.task_name = task_name
    task.description = description
    task.assigned_to = assigned_to
    task.due_date = due_date
    task.status = status
    task.save()
    return task.as_dict()

# Delete Task
@frappe.whitelist()
def delete_task(task_id):
    task = frappe.get_doc("Task", task_id)
    task.delete()
    return {"message": _("Task deleted successfully")}


# Connect to Redis
redis_client = redis.StrictRedis.from_url(frappe.conf.redis_cache)

# Helper function to cache data in Redis
def set_cache(key, value, timeout=3600):
    """Cache the data in Redis with an expiry timeout"""
    redis_client.setex(key, timeout, json.dumps(value))

# Helper function to get cached data from Redis
def get_cache(key):
    """Get cached data from Redis"""
    cached_data = redis_client.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None

# Example API function using cache
def get_projects():
    cache_key = "projects_cache"

    # Try to fetch from cache
    cached_projects = get_cache(cache_key)
    if cached_projects:
        return cached_projects  # Return cached data

    # If not cached, fetch from database
    projects = frappe.get_all("Project", fields=["name", "status"])

    # Cache the result for next time
    set_cache(cache_key, projects)

    return projects

# Example of an API function that gets user tasks
def get_user_tasks(user):
    cache_key = f"user_tasks_cache_{user}"

    # Try to fetch from cache
    cached_tasks = get_cache(cache_key)
    if cached_tasks:
        return cached_tasks  # Return cached data

    # If not cached, fetch from database
    tasks = frappe.get_all("Task", filters={"assigned_to": user}, fields=["name", "status"])

    # Cache the result for next time
    set_cache(cache_key, tasks)

    return tasks

