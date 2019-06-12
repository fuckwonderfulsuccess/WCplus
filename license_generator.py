#!/usr/bin/env python3

"""
generate WCplus3 license
usage:
    python3 license_generator.py 标识码
example:
    python3 license_generator.py 3标识码@186527425142744
"""
from datetime import datetime
import sys
import re


def generate_license(mac):
    """

    :param mac: int 类型的mac地址
    :return:
    """
    end_time = datetime.strptime("2020-12-31 23:59:59", "%Y-%m-%d %H:%M:%S")
    end_time_int = int(end_time.timestamp())
    passport = end_time_int + 12874767561234 + mac
    with open("license.ca", "w", encoding="utf-8") as f:
        f.write("licensed by F***wonderfulsuccess\n" * 70)
        f.write("{}\n".format(mac))
        f.write("licensed by F***wonderfulsuccess\n" * 20)
        f.write("{}\n".format(passport))


if __name__ == "__main__":
    try:
        code = sys.argv[1]
    except IndexError:
        print(__doc__)
        exit(0)
    m = re.search(r"3标识码@(\d{2,})", code)
    if m:
        mac = m.group(1)
    else:
        m = re.search(r"\d{2,}", code)
        if not m:
            print(__doc__)
            exit(0)
        mac = m.group(0)
    mac = int(mac)
    generate_license(mac)
    print("License generated at license.ca")

