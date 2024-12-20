import threading
import queue
import logging

from . import list_apps, Application
from . import Recognizer
from . import Speak

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(threadName)s] %(message)s')


class Assistant:
    def __init__(self):
        super().__init__()
        self._SR = Recognizer()
        self._speaker = Speak()

        self._speak_lock = 0

        # Queues for producer-consumer threads
        self.audio_queue = queue.Queue()
        self.text_queue = queue.Queue()

        # Event to stop all threads
        self._stop_event = threading.Event()

    def listen(self):
        """Listens for audio and places audio data in the audio queue."""
        while not self._stop_event.is_set():
            try:
                audio_data = self._SR.get_audio()  # Simulate getting audio data
                if audio_data:
                    self.audio_queue.put(audio_data)
                    logging.info("Audio added to queue")
            except Exception as e:
                logging.error("Error in listening: %s", e)

    def recognize(self):
        """Takes audio from audio queue, recognizes it, and puts text in text queue."""
        logging.info("Starting recognition...")
        while not self._stop_event.is_set():
            try:
                audio_data = self.audio_queue.get(timeout=1)  # Waits for audio data
                text = self._SR.recognize(audio_data)  # Simulate recognition

                if text:
                    self.text_queue.put(text)
                    self.launch_application(text)
                    logging.info("Text recognized and added to text queue: %s", text)
                self.audio_queue.task_done()
            except queue.Empty:
                continue  # Continue if audio queue is empty
            except Exception as e:
                logging.error("Error in recognition: %s", e)

    def launch_application(self, text):
        """Launches an application if 'launch' is found in the recognized text."""
        if "launch" in text:
            for app_name in list_apps():
                if app_name in text.lower():
                    Application(app_name).launch()
                    logging.info(f"Launching application: {app_name}")
                    break

    def speak(self):
        """Takes recognized text from text queue and speaks it."""
        while not self._stop_event.is_set():
            try:
                text_to_speak = self.text_queue.get(timeout=1)  # Waits for text data
                logging.info("Speaking: %s", text_to_speak)

                # Use a new thread to handle speech output, so the loop isn't blocked
                speech_thread = threading.Thread(target=self._speaker.say, args=(text_to_speak,))
                speech_thread.start()

                self.text_queue.task_done()
            except queue.Empty:
                continue  # Continue if text queue is empty
            except Exception as e:
                logging.error("Error in speaking: %s", e)

    def stop(self):
        """Stops all threads by setting the stop event."""
        self._stop_event.set()

        # Ensure all tasks in queues are processed before stopping
        self.audio_queue.join()  # Wait for all audio tasks to be processed
        self.text_queue.join()  # Wait for all text tasks to be processed

    def cleanup(self):
        """Clean up resources when stopping the assistant."""
        self._SR.cleanup()  # If the Recognizer has a cleanup method
        self._speaker.cleanup()  # If the Speak class has cleanup (like closing audio streams)


def start():
    assistant = Assistant()

    # Create threads for each task
    listen_thread = threading.Thread(target=assistant.listen, name="ListenThread")
    recognize_thread = threading.Thread(target=assistant.recognize, name="RecognizeThread")
    # speak_thread = threading.Thread(target=assistant.speak, name="SpeakThread")

    # Set threads as daemon so they will stop when the main thread ends
    listen_thread.daemon = True
    recognize_thread.daemon = True
    # speak_thread.daemon = True

    # Start threads
    listen_thread.start()
    recognize_thread.start()
    # speak_thread.start()

    try:
        # Wait for threads to complete (won't happen since threads are daemonized)
        listen_thread.join()
        recognize_thread.join()
        # speak_thread.join()
    except KeyboardInterrupt:
        # Stop all threads on interrupt
        logging.info("Stopping Assistant...")
        assistant.stop()
        # Wait for threads to complete gracefully
        listen_thread.join()
        recognize_thread.join()
        # speak_thread.join()