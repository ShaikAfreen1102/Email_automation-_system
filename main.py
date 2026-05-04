import time
from config import DAILY_LIMIT, DELAY_BETWEEN_EMAILS
from db import get_connection, fetch_pending, update_status
from email_sender import send_email

def run():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    users = fetch_pending(cursor)

    print(f"Found {len(users)} emails to process\n")

    sent_count = 0

    for user in users:
        if sent_count >= DAILY_LIMIT:
            print("Daily limit reached")
            break

        print(f"Sending to {user['name']} ({user['email']})")

        status, error = send_email(user)

        update_status(cursor, user["id"], status, error)
        connection.commit()

        if status == "Sent":
            sent_count += 1

        time.sleep(DELAY_BETWEEN_EMAILS)

    cursor.close()
    connection.close()

    print("\nAll emails processed.")

if __name__ == "__main__":
    run()