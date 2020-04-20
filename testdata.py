import fpgrowth
import logging

logging.basicConfig(level=logging.DEBUG)
# records = [['f','a','c','d','g','i','m','p'], ['a','b','c','f','l','m','o'], ['b','f','h','j','o','w'], ['b','c','k','s','p'], ['a','f','c','e','l','p','m','n'] ]
# records = [['r','z','h','j','p'],
#             ['z','y','x','w','v','u','t','s'],
#             ['z'],
#             ['r','x','n','o','s'],
#             ['y','r','x','z','q','t','p'],
#             ['y','z','x','e','q','s','t','m']]
records = [[1,2,5], [2,4], [2,3], [1,2,4], [1,3], [2,3], [1,3], [1,2,3,5], [1,2,3]]
freq_itemsets =  fpgrowth.do_fp_growth(min_sup=2, records=records)
print(len(freq_itemsets))
for itemset in freq_itemsets:
  print(itemset)