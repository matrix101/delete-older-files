import smtplib
import email


def send_email(deleted_files, diskpercent):
    user = "xxxxxx@hotmail.it"
    passwd = "xxxxxxxxx"

    from_addr = "xxxxxxx@hotmail.it"
    to_addr = "xxxxxx@gmail.com"
    smtp_srv = "smtp.live.com"
    smtp_port = 587

    title = "Disk is almost full"
    print(deleted_files)
    if len(deleted_files) > 1:
        message = "Deleted files:\n" + "\n".join(deleted_files) + "\nCurrent disk usage: {0}%".format(diskpercent)
        print(message)
    else:
        message = "Disk is almost full but nothing to delete in the folder :(\n{0}% of the disk is used.".format(diskpercent)
    msg = email.message_from_string(message)
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = title

    smtp = smtplib.SMTP(smtp_srv, smtp_port)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(user, passwd)
    smtp.sendmail(from_addr, to_addr, msg.as_string())
    smtp.quit()
