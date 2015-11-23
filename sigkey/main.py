__author__ = 'vwvolodya'

from pprint import pprint


class IndexedString(object):
    def __init__(self):
        self.tree = dict()
        self.searched = list()

    def add_key(self, string):
        pointer = self.tree
        for i, c in enumerate(string):
            val = dict()
            if i == len(string) - 1:
                val = {'value': string}
            self._recursive_add(pointer, c, val)
            pointer = pointer[c]

    def _recursive_add(self, pointer, key, value):
        if not pointer:     # points to empty dict
            pointer[key] = value
        else:
            if key in pointer.keys():
                pass
            else:
                pointer[key] = value

    def _recursive_search(self, pointer):
        key_list = pointer.keys()
        for el in key_list:
            if el == 'value':
                self.searched.append(pointer['value'])
                return
            self._recursive_search(pointer[el])

    def search_key(self, string):
        pointer = self.tree
        for i, c in enumerate(string):
            val = pointer.get(c)
            if not val:
                return -1
            if i == len(string) - 1:
                result = val.get('value')
                if not result:
                    self._recursive_search(val)
                    result = self.searched
                    self.searched = list()
                    return result
                else:
                    if len(result) == len(string):
                        return [result]
                    return -1
            pointer = pointer[c]

    def search_key_strict(self, string):
        pointer = self.tree
        for i, c in enumerate(string):
            val = pointer.get(c)
            if not val:
                return -1
            if i == len(string) - 1:
                result = val.get('value')
                if not result:
                    return -1
                else:
                    return [result]
            pointer = pointer[c]

    def printed(self):
        pprint(self.tree)


if __name__ == '__main__':
    tmp = IndexedString()
    tmp.add_key('bdfhko')
    tmp.add_key('bdgjl')
    print tmp.search_key('bdgjl')
    print tmp.search_key('bdfhko')
    print tmp.search_key('fhfjh')
    print tmp.search_key('bd')
    tmp.printed()
