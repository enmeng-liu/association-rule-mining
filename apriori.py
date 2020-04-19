import logging

def is_subset(itemset, record):
  count = 0
  for item in itemset:
    if item in record:
      count = count + 1
  return (count == len(itemset))

def get_frequence(itemset, records):
  """查找itemset在records中出现的次数
  """
  freq = 0
  for record in records:
    if is_subset(itemset, record):
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
  if k != len(l2):
    raise ValueError('The lengths of two lists are different!')
  for i in range(0, k-1):
    if l1[i] != l2[i]:
      return False
  return (l1[k-1] < l2[k-1])

def has_infreq_subset(new_itemsets, freq_itemsets):
  k = len(freq_itemsets[0])
  assert(len(new_itemsets) == k + 1)
  for item in new_itemsets:
    tmp = new_itemsets.copy()
    tmp.remove(item)
    if not tmp in freq_itemsets:
      return True
  return False

def apriori_gen(k, min_sup, freq_itemsets):
  if not freq_itemsets:
    return []
  new_freq_itemsets = []
  for itemset1 in freq_itemsets:
    for itemset2 in freq_itemsets:
      if list_match(itemset1, itemset2):
        # 因为是排好序的list，所以join操作其实就是加上最后一个元素
        c = itemset1.copy()
        c.append(itemset2[-1])
        # print(itemset1)
        c.sort()
        # 当c所有k-subset都为频繁项集时加入结果中
        if not has_infreq_subset(c, freq_itemsets):
          new_freq_itemsets.append(c)
  if new_freq_itemsets:
    logging.info('k={}, freq[0]={}, times={}'.format(k, new_freq_itemsets[0], get_frequence(new_freq_itemsets[0], freq_itemsets)))
  return new_freq_itemsets


def filter_conf(min_conf, itemset, records, output):
  """计算A=>B的置信度
  """
  size = len(itemset)
  status = 1 << size
  for i in range(1, status-1):
    lhs, rhs = [], []
    for j in range(0,size):
      if (1<<j) & i:
        lhs.append(itemset[j])
      else:
        rhs.append(itemset[j])
    lhs_times, rhs_times = 0, 0
    for record in records:
      if is_subset(lhs, record):
        lhs_times = lhs_times + 1
        if is_subset(rhs, record):
          rhs_times = rhs_times + 1
    logging.debug('lhs={}, lhs_times={}, rhs={}, rhs_times={}'.format(lhs, lhs_times, rhs, rhs_times))
    if (rhs_times/lhs_times) >= min_conf:
      if output: 
        sup = get_frequence(itemset, records)
        print('{} => {}: [{}, {}]'.format(lhs, rhs, sup, rhs_times/lhs_times))


def apriori(min_sup, min_conf, items, records, output):
  nr_items = len(items)
  freq_itemsets = find_freq_1_itemsets(min_sup, items, records)
  logging.debug('freq 1-itemsets: {}'.format(len(freq_itemsets)))
  # res = freq_itemsets
  res = []
  for k in range(1, nr_items + 1):
    freq_itemsets = apriori_gen(k, min_sup, freq_itemsets)
    if not freq_itemsets:
      break
    # 删除所有不够频繁的itemset
    new_freq_itemsets = []
    for itemset in freq_itemsets:
      if get_frequence(itemset, records) >= min_sup:
        new_freq_itemsets.append(itemset)
    res = res + new_freq_itemsets
    freq_itemsets = new_freq_itemsets.copy()
  logging.debug('number of results: {}'.format(len(res)))
  nr_res = 0
  for itemset in res:
    if filter_conf(min_conf, itemset, records, output):
      nr_res = nr_res + 1
  # if output:
  #   print('Mining finished. Get %d rules in total' % nr_res)