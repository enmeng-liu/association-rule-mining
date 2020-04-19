import fpgrowth
import logging

logging.basicConfig(level=logging.DEBUG)
records = [['f','a','c','d','g','i','m','p'], ['a','b','c','f','l','m','o'], ['b','f','h','j','o','w'], ['b','c','k','s','p'], ['a','f','c','e','l','p','m','n'] ]
items = {'f','c','a','b','m','p','o','i','w','d','g','l','k','s','h','e','n', 'j'}
fpgrowth.do_fp_growth(min_sup=3, min_conf=0, items=items, records=records)