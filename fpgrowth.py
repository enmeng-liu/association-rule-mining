import logging

class fpTreeNode:
  """
  name: 节点对应的item name
  cnt: 节点上item出现的次数
  nxt: 下一个item相同的节点
  parent: 上一个节点
  children: dict, 下一个节点：节点对象
  """
  def __init__(self, name, cnt, parent):
    self.name = name
    self.cnt = cnt
    self.parent = parent
    self.children = []
    # logging.debug('create node: %s' % name)
  def __repr__(self):
    print('(%s: %d)' % (self.name, self.cnt))

  def output(self, indent=1):
    print(' '*indent, self.name, ' ', self.cnt)
    if self.children:
      for child in self.children:
        child.output(indent+1)
  
  def add_cnt(self):
    self.cnt += 1
    # logging.debug('node: %s cnt+1=%d' % (self.name, self.cnt))

# ---------------------------------------------------------
def find_in_nodes_list(name, node_list):
  """在一系列节点中查找名字为name的节点，返回第一个
  """
  for node in node_list:
    if name == node.name:
      return node
  return None

class fpTree:
  """
  root_children: list of nodes, 直接与根节点相连的节点
  """
  def __init__(self, min_sup, min_conf, records, items):
    self.min_sup = min_sup
    self.min_conf = min_conf
    self.records = records
    self.items = items
    self.root_children = []

  def __repr__(self):
    for child in self.root_children:
      child.output()

  def update_fptree(self, record):
    """给定record，更新fp-tree
    """
    logging.debug('add record:{} to fp-tree'.format(record))
    cur_node = None
    for item in record:
      if cur_node is None:
        children = self.root_children
      else:
        children = cur_node.children
      new_node = find_in_nodes_list(item, children)
      if new_node is None:
        # 在孩子里找不到这个item，新建一个节点，并加入header table和children中
        new_node = fpTreeNode(name=item, cnt=1, parent=cur_node)
        self.header_table[item].append(new_node)
        children.append(new_node)
      else:
        # 在孩子里找到了这个item，计数+1
        new_node.add_cnt()
      cur_node = new_node

  def construct(self):
    # Scan DB, find frequent 1-itemset and their frequencies
    self.freq_dict = {}
    for item in self.items:
      self.freq_dict[item] = 0
    for record in self.records:
      for item in record:
        self.freq_dict[item] += 1
    # create header table
    self.header_table = {}
    for item in self.items:
      if self.freq_dict[item] >= self.min_sup:
        self.header_table[item] = []
    # logging.debug(sorted(self.header_table.keys(), key=lambda x: self.freq_dict[x]), reverse=True)
    # Scan DB 2nd time
    for record in self.records:
      # delete infrequent items 
      new_record = []
      for item in record:
        if self.freq_dict[item] >= self.min_sup:
          new_record.append(item)
      # sort frequent items
      new_record = sorted(new_record, key=lambda x: (self.freq_dict[x], x),reverse=True)
      # new_record.sort(key=self.freq_key, reverse=True)
      # logging.debug('------------------------')
      # for i in new_record:
      #   logging.debug('%s: %d'% (i, self.freq_dict[i] ))
      self.update_fptree(new_record)

  def find_all_paths(self, item):
    """在fp-tree中为某个倒序item找到所有路径，返回一个字典记录每个item出现的次数
    """
    paths = []
    for bottom in self.header_table[item]:
      node_list, freq = [], bottom.cnt
      while bottom is not None:
        node_list.insert(0, bottom.name)
        bottom = bottom.parent
      for i in range(0, freq):
        paths.append(node_list)
    return paths

  def mine(self):
    # 最开始的频繁项集是header table中的各元素
    freq_1_itemsets = sorted(self.header_table.keys(), key=lambda x: self.freq_dict[x])
    for item in freq_1_itemsets:
      new_records = []
      for bottom in self.header_table[item]:
        prefix_list, freq = [], bottom.cnt
        while bottom is not None:
          prefix_list.insert(0, bottom.name)
          bottom = bottom.parent
      for i in range(0, freq):
        new_records.append(prefix_list)
      new_tree = fpTree(self.min_sup, self.min_conf, new_records, set(freq_1_itemsets))
      new_tree.construct()
      if new_tree.header_table != None:
        new_tree.mine()
      else:
        self.records = new_tree.records

  def mining(self, prefix, freq_itemsets):
    freq_1_itemsets = sorted(self.header_table.keys(), key=lambda x: self.freq_dict[x])
    for itemset in freq_1_itemsets:
      new_freq_set = prefix.copy()
      new_freq_set.add(itemset)
      freq_itemsets.append(new_freq_set)
      cond_pattern_bases = self.find_all_paths(itemset)
      cond_tree = fpTree(self.min_sup, self.min_conf, cond_pattern_bases, freq_itemsets)
      cond_tree.construct()
      if cond_tree.header_table != None:
        cond_tree.mining(new_freq_set,  freq_itemsets)

  
  def output_result(self):
    for record in self.records:
      print(record)

# ----------------------------------------------------------
def do_fp_growth(min_sup, min_conf, items, records):
  fptree = fpTree(min_sup, min_conf, records, items)
  fptree.construct()
  # logging.debug(fptree)
  # fptree.mine()
  res = []
  fptree.mining(set(), res)
  print(res)
  # fptree.output_result()
  
