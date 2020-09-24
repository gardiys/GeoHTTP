class Storage:
    """Custom storage for parse and store data"""
    def __init__(self):
        self.data = self._parse_data()
        self.data_list = list(self.data.keys())

    def _parse_data(self):
        data = {}
        with open("RU.txt") as f:
            line = f.readline().split("\t")

            while len(line) == 19:
                data[int(line[0])] = self._parse_line(line)
                line = f.readline().split("\t")

        return data

    def _parse_line(self,line):
        temp = {}
        temp["name"] = line[1]
        temp["asciiname"] = line[2]
        temp["alternatenames"] = line[3].split(",")
        temp["latitude"] = float(line[4])
        temp["longitude"] = float(line[5])
        temp["feature_class"] = line[6]
        temp["feature_code"] = line[7]
        temp["country_code"] = line[8]
        temp["cc2"] = line[9]
        temp["admin1_code"] = line[10]
        temp["admin2_code"] = line[11]
        temp["admin3_code"] = line[12]
        temp["admin4_code"] = line[13]
        temp["population"] = int(line[14])
        temp["elevation"] = line[15] and int(line[15])
        temp["dem"] = int(line[16])
        temp["timezone"] = line[17]
        temp["modification_date"] = line[18]

        return temp

    def get(self, id):
        return self.data.get(id)


if __name__ == "__main__":
    ex = Storage()
    print(len(ex.data_list))