import csv, sys

def read_csv(filename):
  with open(filename, 'rb') as f:
    reader = csv.reader(f)
    try:
      for row in reader
        print row
    except csv.Error, e:
      sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
  
################### Main:
if (len(sys.argv) > 1):
  print 'Dump csv\n'
  read_csv(sys.argv[1])
else:
    print "Usage: " + sys.argv[0] + " csv_filename"

print 'DONE\n'

