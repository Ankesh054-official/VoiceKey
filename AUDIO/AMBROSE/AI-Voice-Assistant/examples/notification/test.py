from plyer import notification

notification.notify(
    title="Error Notification",                  # Title of the notification
    message="An error occurred. Please check the logs.",  # Message to display
    app_name="VCAS",
    app_icon="mark.ico",
    timeout=10                                   # Duration in seconds
)

# notify(
#             title=title, message=message,
#             app_icon=app_icon, app_name=app_name,
#             timeout=timeout, ticker=ticker, toast=toast, hints=hints
#         )