#!/usr/bin/env python3

from zipfile import ZipFile

import requests
import shutil
import json
import sys
import os


def bills(path="."):
    for root, dirs, files in os.walk(path):
        for file_ in files:
            with open(os.path.join(root, file_), 'r') as fd:
                yield json.load(fd)


def digest():
    statuses = set()
    for bill in bills():
        # print("  {bill_id}".format(**bill))
        for action in bill['actions']:
            statuses.add(action.get('status', None))
    print(statuses)



def main(session):
    url = ("http://unitedstates.sunlightfoundation.com/"
           "congress/data/{}.zip".format(session))

    print("Downloading the data")
    zipfile = "{}.zip".format(session)

    if not os.path.exists(zipfile):
        r = requests.get(url)
        with open(zipfile, 'w') as fd:
            fd.write(r.content)

    print("Got it.")

    # if os.path.exists(session):
    #     print("Removing old data")
    #     shutil.rmtree(session)

    # os.mkdir(session)
    os.chdir(session)
    # print("Extracting new data")
    # ZipFile(os.path.join("..", zipfile)).extractall()
    digest()


if __name__ == "__main__":
    main(*sys.argv[1:])
