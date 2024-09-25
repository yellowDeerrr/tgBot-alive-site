import requests
import time
import threading

mutex = threading.Lock()  # Use a lock to safely modify the global flag across threads
treading_stop = False

def send_get_request(message, bot):
    request = requests.get("https://render-app-jtov.onrender.com")
    bot.send_message(message.chat.id, "Response: " + str(request.status_code))

def stop_sending():
    global treading_stop
    with mutex:
        treading_stop = True
    print("Stop signal sent.")

def start_sending(times_to_do_send, message, bot):
    global treading_stop
    treading_stop = False  # Reset the stop flag when starting

    for i in range(times_to_do_send):
        with mutex:
            if treading_stop:  # Check if the stop signal has been sent
                bot.send_message(message.chat.id, "Sending process stopped.")
                print("Sending process stopped.")
                break
        send_get_request(message, bot)
        time.sleep(5)  # Adjust this to a reasonable value; 5 seconds for testing

    bot.send_message(message.chat.id, "Sending process completed.")
    print("Sending process completed.")
