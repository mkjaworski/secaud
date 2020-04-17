#!/usr/bin/python

import csv
import sys
import re
import os
import glob

def inlookup(inf, inval, outf):
    try:
        config_app_path = os.path.join(os.environ['SPLUNK_HOME'],'etc','apps','secaud')
        csvname = "service_lookup.csv"
        csvpath = os.path.join(config_app_path,'lookups',csvname)
    except Exception as e:
        sys.stderr.write("No %s file found." % csvname)
        sys.exit(0)

    try:
        c = open(csvpath, 'rb')
        f = csv.DictReader(c)

        for row in f:
            if re.search(row[inf], inval):
                return row[outf]

    except Exception as e:
        sys.stderr.write(e)
        sys.exit(1)
        return []

def main():
    if len(sys.argv) != 3:
        print "Usage: %s <in field> <out field>" % (sys.argv[0])
        sys.exit(0)

    inf = sys.argv[1]
    outf = sys.argv[2]
    r = csv.DictReader(sys.stdin)
    w = csv.DictWriter(sys.stdout, r.fieldnames)
    w.writeheader()

    for result in r:
        # If all fields are already present, there's no need
        # to look anything up
        if len(result[inf]) and len(result[outf]):
            w.writerow(result)

        elif len(result[inf]):
            outvalue = inlookup(inf, result[inf], outf)
            result[outf] = outvalue
            w.writerow(result)

main()
