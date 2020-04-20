import csv, logging, time, os, psutil
import apriori
import fpgrowth
import grocery_store

time_and_mem = False
# method = 'apriori'
method = 'fpgrowth'

def check_sup(freq_itemsets, records, min_sup):
  for itemset in freq_itemsets:
    cnt = 0
    for record in records:
      if apriori.is_subset(itemset, record):
        cnt += 1
    assert(cnt >= min_sup)


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  records, items = grocery_store.get_records_and_items()
  min_sup, min_conf = 100,0.5
  t1 = time.time()
  if method == 'apriori':
    freq_itemsets = apriori.apriori(min_sup=min_sup, items=items, records=records)
  else:
    freq_itemsets = fpgrowth.do_fp_growth(min_sup=min_sup, records=records)
  if time_and_mem:
    t2 = time.time()
    print('time consume: %f s' % (t2 - t1))
    print ('memory used: %.2f MB' % (psutil.Process(os.getpid()).memory_info().rss/(1024 ** 2)))
  else:
    print(len(freq_itemsets))
    freq_itemsets.sort()
    # for itemset in freq_itemsets:
    #   print(list(itemset))
    # check_sup(freq_itemsets, records, min_sup)
  
  # ass_rules = []
  # for itemset in freq_itemsets:
  #   ass_rules += apriori.filter_conf(min_conf, list(itemset), records)
  
  # print('%d rules in total:' % len(ass_rules))
  # for rule in ass_rules:
    # print(rule)


