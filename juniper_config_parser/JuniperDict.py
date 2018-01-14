class JuniperConfig(dict):

    def __init__(self, iterable):
        super().__init__(self.__parse__(iterable))

    def __parse__(self, iterable):
        result = {}
        for i in iterable:
            line = i.lstrip().rstrip("\n").rstrip(";")
            if any(x in line for x in ["#","version"]):
                continue
            if '{' in line:
                result[line.split("{")[0].rstrip()] = self.__parse__(iterable)
                continue
            elif "}" in line:
                return result
            elif " " not in line:
                result[line] = ""
                continue
            elif " " in line:
                try:
                    first = result[line.split(" ", maxsplit=1)[0]]
                    if type(first) is list:
                        result[line.split(" ", maxsplit=1)[0]].append(line.split(" ", maxsplit=1)[-1])
                    else:
                        result[line.split(" ", maxsplit=1)[0]] = [first, line.split(" ", maxsplit=1)[-1]]
                except KeyError:
                    result[line.split(" ", maxsplit=1)[0]] = line.split(" ", maxsplit=1)[-1]
        return result

    def as_file(self, data=None, intend=0):
        if data is None:
            data = self
        for key in data.keys():
            line = data[key]
            if type(line) is str:
                if len(line) > 0:
                    yield intend*" "+"{} {};".format(key, line)
                else:
                    yield intend*" "+"{};".format(key)
            elif type(line) is dict:
                yield intend*" "+'{}'.format(key) + " {"
                for l in self.as_file(data=line, intend=intend+4):
                    yield l
                yield intend*" "+"}"
            elif type(line) is list:
                for l in line:
                    yield intend*" "+"{} {};".format(key, l)

    def set_commands(self, data=None, prefix=None):
        if data is None:
            data = self
        # print(data)
        if prefix is None:
            prefix = ""
        for key in data.keys():
            line = data[key]
            if type(line) is str:
                if len(line) > 0:
                    yield "set" + prefix + " {} {}".format(key, line)
                else:
                    yield "set" + prefix + " {}".format(key)
            elif type(line) is dict:
                for l in self.set_commands(data=line, prefix=str("{} {}").format(prefix, key)):
                    yield l
            elif type(line) is list:
                for l in line:
                    yield "set" + prefix + " {} {}".format(key, l)
