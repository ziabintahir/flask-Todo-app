## GET /api/tasks
Returns all tasks.

## POST /api/tasks
Creates a task.

Request JSON:
{
  "title": "Task",
  "description": "Desc",
  "due_date": "YYYY-MM-DD",
  "status": "pending"
}

## PUT /api/tasks/{id}
Updates a task.

## DELETE /api/tasks/{id}
Deletes a task.
