import csv
rows = []
with open('../modeloutput/detectnewgatesensation.csv') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        if 'sensation' in row['genretags']:
            row['realclass'] = 'sensation'
        elif 'newgate' in row['genretags']:
            row['realclass'] = 'Newgate'
        elif row['realclass'] == '1':
            row['realclass'] = 'detective'
        else:
            row['realclass'] = 'random'
        rows.append(row)

with open('../plotdata/mungednewgatesensation.csv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fieldnames = fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)


