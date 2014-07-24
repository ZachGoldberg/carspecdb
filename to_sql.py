import csv
import sqlite3



if __name__ == '__main__':
    reader = csv.DictReader(open('data.csv').readlines())
    conn = sqlite3.connect('cars.db')

    fields = ",".join("%s text" % k for k in reader.fieldnames)
    conn.execute('''DROP TABLE cars''')
    conn.execute('''CREATE TABLE cars (%s)''' % fields)

    qs = ",".join("?" * len(reader.fieldnames))

    i = 0
    for row in reader:
        i += 1
        if i % 100 == 0:
            print i
        vals = []
        for field in reader.fieldnames:
            val = row[field]
            val = val.replace('"', 'in')
            vals.append('"%s"' % val)

        query = 'INSERT INTO cars VALUES (%s)' % (','.join(vals))
        conn.execute(query)
    conn.commit()
