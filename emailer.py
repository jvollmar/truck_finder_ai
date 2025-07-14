import smtplib

EMAIL_SENDER = "your_yahoo_email@yahoo.com"
EMAIL_PASSWORD = "your_yahoo_app_password"
EMAIL_RECEIVER = "rmzgrace@yahoo.com"

GITHUB_PAGES_URL = "https://jvollmar.github.io/truck_finder_ai"

def send_email_with_link():
    subject = "🚙 Truck Search Results Ready"
    body = f"""
    The latest certified truck search results are ready. 🛻

    👉 View them here: {GITHUB_PAGES_URL}

    (This link updates automatically with the newest results.)
    """

    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message)
        print("✅ Email with GitHub Pages link sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)
