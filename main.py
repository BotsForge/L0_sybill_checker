# pyinstaller -n "L0_sybill_checker" -F -i "../BF.ico" --add-data "../BF.ico;." --add-data "provisionalSybilList.csv;." main.py

import csv
import sys
import ctypes
from time import sleep
import traceback

from loguru import logger

from utils import LOGO, resource_path


logger.remove(0)
logger.add(sys.stderr, level='DEBUG', colorize=True, format="{time:HH:mm:ss}<level> | {level: <7} | {message}</level>",)


def get_cbill_wallets():
    with open(resource_path('provisionalSybilList.csv')) as file:
        reader = csv.reader(file, delimiter=',')
        rows = [row for row in reader]
        wallets = []
        for row in rows[1:]:
            try:
                wallets.append(row[2].lower().strip())
            except Exception:
                pass

        return wallets


def get_my_wallets():
    with open('wallets.txt') as file:
        wallets = [i.strip().lower() for i in file.readlines() if i.strip()]
    return wallets


def main():
    s = get_cbill_wallets()
    logger.info(f"total sybill = {len(s)}")
    w = get_my_wallets()
    logger.info(f"total wallets to check = {len(w)}")

    sleep(2)
    for wallet in w:
        if wallet in s:
            logger.error(wallet)
        else:
            logger.success(wallet)


if __name__ == '__main__':
    ctypes.windll.kernel32.SetConsoleTitleW('L0_sybill_checker')
    print(LOGO)
    try:
        main()
    except Exception as er:
        logger.warning(er)
        logger.debug(traceback.format_exc())
    finally:
        input('Press <Enter> to close...')
