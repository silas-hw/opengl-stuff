#
# a subclass of dict that allows for keys to have a range of numbers as their key
#
# if a dict 'myDict' had a key 'range(0, 45)', then both 'myDict[20]' and 'myDict[26]' would return
# its value
#
# taken from https://stackoverflow.com/questions/39358092/range-as-dictionary-key-in-python/39358140

class RangeDict(dict):
    def __getitem__(self, item):
        if not isinstance(item, range):
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item)