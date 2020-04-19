import csv, logging, time, os, psutil
import apriori
import fpgrowth

def get_records_and_items():
  """读取csv，将购买记录整理为list of lists
  """
  with open('Groceries.csv') as f:
    f_csv = csv.reader(f)
    _ = next(f_csv)
    records = []
    items = set()
    for row in f_csv:
      row[1] = row[1][1:-1]
      item_line = row[1].split(',')
      items.update(item_line)
      records.append(item_line)
    return records, items

if __name__ == '__main__':
  t1 = time.time()
  logging.basicConfig(level = logging.DEBUG)
  records, items = get_records_and_items()
  min_sup, min_conf = 100, 0.5
  # apriori.apriori(min_sup=100, min_conf=0.5, items=items, records=records, output=False)
  fpgrowth.do_fp_growth(min_sup, min_conf, items, records)
  t2 = time.time()
  print('time consume: %f s' % (t2 - t1))
  print ('memory used: %.2f MB' % (psutil.Process(os.getpid()).memory_info().rss/(1024 ** 2)))
