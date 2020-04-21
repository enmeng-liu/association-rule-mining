def get_records(uid):
  file_path = 'dataset/UNIX_usage/USER%d/sanitized_all.981115184025' % uid
  with open(file_path) as f:
    records = []
    cmd_set = set()
    for row in f:
      row = row[0:-1]
      if row == '**EOF**':
        records.append(list(cmd_set.copy()))
        cmd_set.clear()
      elif row.isalpha():
        cmd_set.add(row)
  return records

# if __name__ == '__main__':
#   print(get_records(0))
