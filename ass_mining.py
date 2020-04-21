import csv, logging, time, os, psutil
import apriori, fpgrowth, baseline
import grocery_store, unix_usage

time_and_mem = False
# method = 'apriori'
method = 'fpgrowth'
# method = 'baseline'

method_dict = {
  'apriori': apriori.apriori,
  'fpgrowth': fpgrowth.do_fp_growth,
  'baseline': baseline.do_baseline
}

def check_sup(freq_itemsets, records, min_sup):
  for itemset in freq_itemsets:
    cnt = 0
    for record in records:
      if apriori.is_subset(itemset, record):
        cnt += 1
    assert(cnt >= min_sup)


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  # records = grocery_store.get_records()
  records = unix_usage.get_records(1)
  min_sup, min_conf = 200, 0.7
  t1 = time.time()
  freq_itemsets = method_dict[method](min_sup, records)
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
  
  ass_rules = []
  for itemset in freq_itemsets:
    ass_rules += apriori.filter_conf(min_conf, list(itemset), records)
  print('%d rules in total:' % len(ass_rules))
  for rule in ass_rules:
    print(rule)


