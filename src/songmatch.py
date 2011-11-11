import csv, sys

def read_csv(filename):
  with open(filename, 'rb') as f:
    reader = csv.reader(f)
    try:
      for row in reader
        print row
    except csv.Error, e:
      sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
  
print 'Dump csv\n'
read_csv('dump.csv')

print 'DONE\n'

