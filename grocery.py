import csv

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

def get_frequence(itemset, records):
  """查找itemset在records中出现的次数
  """
  freq = 0
  for record in records:
    for item in itemset:
      count = 0
      if item in record:
        count = count + 1
    if count == len(itemset):
      freq = freq + 1
  return freq

def find_freq_1_itemsets(min_sup, items, records):
  freq_itemsets = []
  for item in items:
    if get_frequence({item}, records) > min_sup:
      freq_itemsets.append([item])
  return freq_itemsets

def list_match(l1, l2):
  """判断两个大小为k的list是否前k-1个都一样，第k个元素set1的更小
  """
  k = len(l1)
  if k != len(k2):
    raise ValueError('The lengths of two lists are different!')
  for i in range(0, k-1):
    if l1[i] != l2[i]:
      return False
  return (l1[k-1] < l2[k-1])

def has_infreq_subset(new_itemsets, freq_itemsets):
  k = len(freq_itemsets)
  assert(len(new_itemsets) == k + 1)
  for item in new_itemsets:
    tmp = new_itemsets.remove(item)
    if not tmp in freq_itemsets:
      return True
  return False

def apriori_gen(k, min_sup, freq_itemsets):
  new_freq_itemsets = []
  for itemset1 in freq_itemsets:
    for itemset2 in freq_itemsets:
      if list_match(itemset1, itemset2):
        # 因为是排好序的list，所以join操作其实就是加上最后一个元素
        c = itemset1 + itemset2[-1]
        c.sort()
        # 当c所有k-subset都为频繁项集时加入结果中
        if not has_infreq_subset(c, freq_itemsets):
          new_freq_itemsets = new_freq_itemsets + c
  return new_freq_itemsets



if __name__ == "__main__":
  records, items = get_records_and_items()
  nr_items = len(items)
  min_sup = 500
  freq_itemsets = find_freq_1_itemsets(min_sup, items, records)
  res = freq_itemsets
  for k in range(1, nr_items + 1):
    freq_itemsets = apriori_gen(k, min_sup. freq_itemsets)
    # 删除所有不够频繁的itemset
    for itemset in freq_itemsets:
      if get_frequence(itemset, records) < min_sup:
        freq_itemsets.remove(itemset)
    res = res + freq_itemsets