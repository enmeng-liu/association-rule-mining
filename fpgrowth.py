import logging
# https://blog.csdn.net/songbinxu/article/details/80411388  

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

  def display(self, indent=1):
    print(' '*indent, self.name, ' ', self.cnt)
    if self.children:
      for child in self.children:
        child.display(indent+1)
  
  def add_cnt(self, cnt=1):
    self.cnt += cnt
    # logging.debug('node: %s cnt+1=%d' % (self.name, self.cnt))

# ---------------------------------------------------------------
class fpTree:
  def __init__(self, min_sup, data_set):
    self.min_sup = min_sup
    self.data_set = data_set
    self.header_table = {}
    self.root = fpTreeNode('root', 1, None)
  
  def display(self):
    self.root.display()

  def find_in_nodelist(self, name, node_list):
    for node in node_list:
      if node.name == name:
        return node
    return None

  def update_fptree(self, trans, cnt):
    # logging.debug('update tree with {}:{}'.format(trans, cnt))
    cur_node = self.root
    for item in trans:
      child_node = self.find_in_nodelist(item, cur_node.children)
      if child_node != None:
        # 已经存在于子节点中，直接更新计数
        child_node.add_cnt(cnt)
      else:
        # 否则新建节点，并加入子节点中
        child_node = fpTreeNode(item, cnt, cur_node)
        cur_node.children.append(child_node)
        # 记入header_table的链表中
        self.header_table[item].append(child_node)
      cur_node = child_node

  def create(self):
    self.header_table = {}
    self.freq_dict = {}
    if self.data_set == None:
      return None
    # 第一遍扫描DB，计算每个item出现的次数
    for trans in self.data_set:
      for item in trans:
        self.freq_dict[item] = self.freq_dict.get(item, 0) + self.data_set[trans]
    # 只为所有频繁的item创建header table表项
    for item in self.freq_dict:
      if self.freq_dict[item] >= self.min_sup:
        self.header_table[item] = []
    # 无频繁项集就立刻返回None
    if len(self.header_table.keys()) == 0:
      return None
    # 第二遍扫描DB，删除所有非频繁item，排序，建树
    for trans in self.data_set:
      filtered_trans = []
      # 保留频繁的item
      for item in trans:
        if self.freq_dict[item] >= self.min_sup:
          filtered_trans.append(item)
      ordered_trans = sorted(filtered_trans, key=lambda p: (self.freq_dict[p],p), reverse=True)
      self.update_fptree(ordered_trans, self.data_set[trans])
    return self.header_table
  
  def prefix_paths(self, item):
    """找到某一个item开始的所有前缀路径
    """
    ret_dict= {}
    for head_node in self.header_table[item]:
      node = head_node.parent
      path_list, cnt = [], head_node.cnt
      while node != self.root:
        path_list.insert(0, node.name)
        node = node.parent
      key = frozenset(path_list)
      if key in ret_dict:
        ret_dict[key] += cnt
      else:
        ret_dict[key] = cnt
    return ret_dict


  def mine(self, freq_set, freq_set_list):
    freq_1_itemsets = sorted(v[0] for v in sorted(self.header_table.items(), key=lambda p : (self.freq_dict[p[0]], p[0])))
    for item in freq_1_itemsets:
      new_freq_set = freq_set.copy()
      new_freq_set.add(item)
      if len(new_freq_set) > 1:
        freq_set_list.append(new_freq_set)
      paths = self.prefix_paths(item)
      new_fptree = fpTree(self.min_sup, paths)
      new_header_table = new_fptree.create()
      if new_header_table != None:
        new_fptree.mine(new_freq_set, freq_set_list)


# -----------------------------------------
def do_fp_growth(min_sup, records):
  data_set = {}
  for record in records:
    key = frozenset(record)
    if key in data_set:
      data_set[key] += 1
    else:
      data_set[key] = 1
  fptree = fpTree(min_sup, data_set)
  fptree.create()
  # fptree.display()
  freq_set_list = []
  fptree.mine(set(), freq_set_list)
  freq_set_list = sorted(freq_set_list, key=lambda p: len(p))
  return freq_set_list
  

