import csv, os
sourcedir = '/Users/tunder/Dropbox/book/chapter2/modeloutput/'
files = os.listdir(sourcedir)

files = [x for x in files if x.endswith('.csv') and not x.endswith('.coefs.csv')]

for fil in files:
    path = sourcedir + fil
    zapped = False
    lines = []
    with open(path, encoding = 'utf-8') as f:
        for line in f:
            if not zapped and ',trainsize' in line:
                line = line.replace(',trainsize', '')
                zapped = True
            lines.append(line)

        if not zapped:
            print('error')

    with open(path, mode = 'w', encoding = 'utf-8') as f:
        for l in lines:
            f.write(l)

