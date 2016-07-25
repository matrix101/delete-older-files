import logging
import os

import psutil
import notify_user

logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S',
                    filename='deleted_files.log', level=logging.DEBUG)

search_dir = "G:\\test\\FI9900P_00626E660790\\record"
warning_threshold = 55
delete_threshold = 60
email_enabled = True

try:
    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir(search_dir))
    files = [os.path.join(search_dir, f) for f in files]  # add path to each file
    files.sort(key=lambda f: os.path.getmtime(f))

    diskstats = psutil.disk_usage(search_dir)

    if diskstats.percent > delete_threshold:
        logging.info("Disk is almost full %s%%", diskstats.percent)
        deleted_files = []
        for filename in files:
            if 'schedule' in filename and filename.endswith('.mkv'):
                try:
                    os.remove(filename)
                    deleted_files.append(filename)
                    logging.info("Deleted: %s", filename)
                except OSError:
                    logging.error("Failed to delete %s", filename)
                if diskstats.percent < warning_threshold:
                    logging.info("Deleted enough files %s%%", diskstats.percent)
                    break
        # if no scheduled record has been deleted but we are running out of space
        #delete alarms
        if len(deleted_files) == 0 and diskstats.percent > delete_threshold:
            for filename in files:
                if 'MDalarm' in filename and filename.endswith('.mkv'):
                    try:
                        os.remove(filename)
                        deleted_files.append(filename)
                        logging.info("Deleted: %s", filename)
                    except OSError:
                        logging.error("Failed to delete %s", filename)
                    if diskstats.percent < warning_threshold:
                        logging.info("Deleted enough files %s%%", diskstats.percent)
                        break
        if email_enabled:
            notify_user.send_email(deleted_files, diskstats.percent)
            logging.info("Email sent")
except FileNotFoundError:
    logging.error("Directory not found: %s", search_dir)
    quit(-1)
