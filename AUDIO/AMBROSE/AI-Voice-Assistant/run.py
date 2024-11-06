from platforms.desktop import main

if __name__ == "__main__":
    try:
        main.start()
    except KeyboardInterrupt:
        print("Quitting process")
