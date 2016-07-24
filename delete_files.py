import logging
import os

import psutil

logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S',
                    filename='deleted_files.log', level=logging.DEBUG)

search_dir = "G:\\test\\record"
percent_threshold = 60

os.chdir(search_dir)
files = filter(os.path.isfile, os.listdir(search_dir))
files = [os.path.join(search_dir, f) for f in files]  # add path to each file
files.sort(key=lambda f: os.path.getmtime(f))

diskstats = psutil.disk_usage(search_dir)

if diskstats.percent > percent_threshold:
    logging.info("Disk is almost full (% > %s)", percent_threshold)
    for file in files:
        if file.find('schedule') and file.endswith('.mkv'):
            try:
                os.remove(file)
                logging.info("Deleted: %s", file)
            except OSError:
                logging.error("Failed to delete %s", file)
            if diskstats.percent < percent_threshold:
                logging.info("Deleted enough files, (% < %s)", diskstats.percent)
                break
