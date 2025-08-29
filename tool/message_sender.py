import datetime
import time
import os
import message as send

# Get delay between rounds
set_timer = int("60")
countrycode = "880"

# Resolve absolute paths
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "requests", "request.txt")
log_file_path = os.path.join(base_dir, "requests", "sent_log.txt")  # log history
console_file_path = os.path.join(base_dir, "requests", "console.txt")  # log history

def log_sent_number(number, message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"{now} - Sent '{message}' to {number}\n")
    with open(console_file_path, "a", encoding="utf-8") as console_file:
        console_file.write(f"[console] {now} - Sent '{message}' to {number}\n")
        
def log_console(msg):
    with open(console_file_path, "a", encoding="utf-8") as console_file:
        console_file.write("[console:] " + msg + "\n")

def send_messages():
    with open(file_path, "r") as f:
        lines = f.readlines()

    if not lines:
        print("✅ No more numbers left in file.")
        log_console("✅ No more numbers left in file.")

    now = datetime.datetime.now()
    h, m = now.hour, now.minute

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        try:
            # Split by first comma
            number, message = line.split(",", 1)
            number = countrycode + number.strip()
            message = message.strip()
        except Exception as e:
            print(f"❌ Skipping invalid line: {line} ({e})")
            log_console(f"❌ Skipping invalid line: {line} ({e})")
            continue

        # Schedule at least 1 minute ahead
        scheduled_minute = m 
        scheduled_hour = h
        if scheduled_minute >= 60:
            scheduled_hour += scheduled_minute // 60
            scheduled_minute = scheduled_minute % 60

        print(f"📩 Sending message '{message}' to {number} at {scheduled_hour}:{scheduled_minute}")
        log_console(f"📩 Sending message '{message}' to {number} at {scheduled_hour}:{scheduled_minute}")

        try:
            # kit.sendwhatmsg(number, message, scheduled_hour, scheduled_minute, 10, True, 2)
            # time.sleep(15)  # avoid overlap
            send.whatsapp(number,message)

            log_sent_number(number, message)

            # Remove the line after sending
            with open(file_path, "r") as f:
                remaining = f.readlines()
            with open(file_path, "w") as f:
                f.writelines(remaining[1:])

        except Exception as e:
            print(f"❌ Failed to send to {number}: {e}")
            log_console(f"❌ Failed to send to {number}: {e}")
            break

    return True

# Main loop
while True:
    if not send_messages():
        break
    print(f"⏳ Waiting {set_timer / 60} minutes before next round...")
    log_console(f"⏳ Waiting {set_timer / 60} minutes before next round...")
    time.sleep(set_timer)
    print("🔄 Starting next round...")
    log_console("🔄 Starting next round... ")
