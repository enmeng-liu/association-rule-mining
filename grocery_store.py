import csv

def get_records():
  """读取csv，将购买记录整理为list of lists
  """
  with open('dataset/GroceryStore/Groceries.csv') as f:
    f_csv = csv.reader(f)
    _ = next(f_csv)
    records = []
    for row in f_csv:
      row[1] = row[1][1:-1]
      item_line = row[1].split(',')
      records.append(item_line)
  return records