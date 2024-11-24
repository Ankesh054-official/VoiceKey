import threading
import queue
import logging


logging.basicConfig(level=logging.INFO)


class Assistant:
    def __init__(self):
        super().__init__()
        self._SR = Recognizer()
        self._speaker = Speak()

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
                    # if ("launch" in text):
                    #     print("test hellop")
                    #     for i in list_apps():
                    #         if i in text.lower():
                    #             Application(i).launch()
                    self.text_queue.put(text)
                    logging.info("Text recognized and added to text queue: %s", text)
                self.audio_queue.task_done()
            except queue.Empty:
                continue  # Continue if audio queue is empty
            except Exception as e:
                logging.error("Error in recognition: %s", e)

    def speak(self):
        """Takes recognized text from text queue and speaks it."""
        while not self._stop_event.is_set():
            try:
                text_to_speak = self.text_queue.get(timeout=1)  # Waits for text data
                logging.info("Speaking: %s", text_to_speak)
                self._speaker.say(text_to_speak)  # Simulate speaking
                self.text_queue.task_done()
            except queue.Empty:
                continue  # Continue if text queue is empty
            except Exception as e:
                logging.error("Error in speaking: %s", e)

    def stop(self):
        """Stops all threads by setting the stop event."""
        self._stop_event.set()


def start():
    assistant = Assistant()

    # Create threads for each task
    listen_thread = threading.Thread(target=assistant.listen)
    recognize_thread = threading.Thread(target=assistant.recognize)
    speak_thread = threading.Thread(target=assistant.speak)

    # Start threads
    listen_thread.start()
    recognize_thread.start()
    speak_thread.start()

    try:
        # Wait for threads to complete
        listen_thread.join()
        recognize_thread.join()
        speak_thread.join()
    except KeyboardInterrupt:
        # Stop all threads on interrupt
        logging.info("Stopping Assistant...")
        assistant.stop()
        listen_thread.join()
        recognize_thread.join()
        speak_thread.join()