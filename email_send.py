import smtplib, ssl


port = 465

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context,) as server:
    server.login("captaintn3612@gmail.com", "thomas2002")



