import smtplib
import sys
import mail_creds

# mail_creds.smtp_user
# mail_creds.smtp_pass


  

try:
    # Prepare test emails
    print("Sending test e-mail to: " + mail_creds.smtp_user)
    
    # Build email
    sent_from = mail_creds.smtp_user
    to = [mail_creds.smtp_user]
    subject = 'E-mail sent successfully from Raspberry Pi'
    body = 'This is a successful test.\n\nHave a nice day!'
    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)
        
    # Server & network stuff
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.ehlo()
    server.login(mail_creds.smtp_user, mail_creds.smtp_pass)
    server.sendmail(sent_from, to, email_text)
    server.close()
    print("Email successfully sent!")
    
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
    