
# Python Logging Guide

Logging is *essential* for tracking events in your software[^1^][1]. This guide will help you set up and use logging in Python.

---

## Basic Setup

1. **Import the logging module**:
    ```python
    import logging
    ```
    The `logging` module provides functions and classes to implement a flexible logging system.

2. **Create a logger**:
    ```python
    logger = logging.getLogger(__name__)
    ```
    - `getLogger(name)`: Retrieves or creates a logger. The `name` typically reflects the module's name, making logs easier to trace.

3. **Set the logging level**:
    ```python
    logger.setLevel(logging.DEBUG)
    ```
    - `setLevel(level)`: Configures the minimum severity level of logs the logger will handle. Levels include:
        - `DEBUG`: Detailed information, typically for diagnosing problems.
        - `INFO`: General events to confirm that things are working as expected.
        - `WARNING`: Indications of potential issues or important runtime events.
        - `ERROR`: Errors preventing some functionality from working.
        - `CRITICAL`: Severe errors that may stop the application.

4. **Create a handler**:
    ```python
    handler = logging.StreamHandler()
    ```
    - Handlers determine where logs are output, such as the console (`StreamHandler`) or a file (`FileHandler`).

5. **Create a formatter and set it for the handler**:
    ```python
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    ```
    - `Formatter`: Customizes the log message format, adding details like timestamps, logger names, and log levels.

6. **Add the handler to the logger**:
    ```python
    logger.addHandler(handler)
    ```
    - `addHandler(handler)`: Connects the logger to the specified output destination.

---

## Logging Messages

Use the logger to log messages at different severity levels:
```python
logger.debug('This is a debug message')  # Use for detailed diagnostic information.
logger.info('This is an info message')  # Use for routine operations like program startup.
logger.warning('This is a warning message')  # Use for unusual but non-critical events.
logger.error('This is an error message')  # Use when something goes wrong.
logger.critical('This is a critical message')  # Use for severe, often unrecoverable issues.
```

---

## Logging to a File

To log messages to a file instead of the console:
```python
logging.basicConfig(
    filename='app.log', 
    filemode='w', 
    format='%(name)s - %(levelname)s - %(message)s'
)
```
- `basicConfig()`: Configures the root logger to log messages to a specified file with a custom format.
- `filename`: Specifies the file where logs will be saved.
- `filemode`: Defines how the file is opened (`'w'` to overwrite, `'a'` to append).

---

## Advanced Configuration

### Setting Logging Level from Command Line
```python
import logging
import sys

loglevel = sys.argv[1].upper()
numeric_level = getattr(logging, loglevel, None)
if not isinstance(numeric_level, int):
    raise ValueError(f'Invalid log level: {loglevel}')
logging.basicConfig(level=numeric_level)
```
- `getattr(logging, loglevel)`: Retrieves the numeric value for a log level by its string name.
- Dynamically sets the logging level from a command-line argument.

---

### Formatting Log Messages
```python
logging.basicConfig(
    format='%(asctime)s %(message)s', 
    datefmt='%m/%d/%Y %I:%M:%S %p'
)
```
- `format`: Customizes log messages to include timestamps, levels, or any other relevant information.
- `datefmt`: Customizes the date and time format for timestamps.

---

### Using Multiple Handlers
```python
file_handler = logging.FileHandler('file.log')
console_handler = logging.StreamHandler()

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
```
- Handlers (`FileHandler` and `StreamHandler`) allow logging to multiple destinations.
- Each handler can have its own format and level.

---

## Conclusion

This guide covers the *basics of logging* in Python. For more advanced usage, refer to the [official documentation](https://docs.python.org/3/library/logging.html).

---

[^1^]: Logging is crucial for debugging and understanding the flow of your application.

[1]: https://docs.python.org/3/library/logging.html
```