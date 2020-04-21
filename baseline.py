import apriori, logging

def records_to_items(records):
  items = set()
  for record in records:
    items.update(record)
  return items

def baseline_gen(k, min_sup, freq_itemsets, items):
  if not freq_itemsets:
    return []
  new_freq_itemsets = []
  for itemset in freq_itemsets:
    for item in items:
      if item not in itemset:
        new_itemset = itemset.copy() + [item,]
        new_itemset.sort()
        if new_itemset not in new_freq_itemsets:
          if not apriori.has_infreq_subset(new_itemset, freq_itemsets):
            new_freq_itemsets.append(new_itemset)
  return new_freq_itemsets

def do_baseline(min_sup, records):
  freq_itemsets = apriori.find_freq_1_itemsets(min_sup, records)
  res, k = [], 1
  items = records_to_items(records)
  while True:
    freq_itemsets = baseline_gen(k, min_sup, freq_itemsets, items)
    if not freq_itemsets:
      break
    new_freq_itemsets = []
    for itemset in freq_itemsets:
      if apriori.get_frequence(itemset, records) >= min_sup:
        new_freq_itemsets.append(itemset)
    res += new_freq_itemsets.copy()
    freq_itemsets = new_freq_itemsets
    logging.debug('finish search k=%d' % k)
    k += 1
  return res