import xmltodict
from collections import OrderedDict


class DataHandler(object):

    data_file = 'scores.xml'
    max_data = 5

    def __init__(self):
        file = None
        try:
            file = open(self.data_file, 'r')
        except IOError:
            print('.xml file not found')
        finally:
            file.close()

    def parse_xml_data(self):
        with open(self.data_file, 'r') as f:
            data = xmltodict.parse(f.read())
        return data

    def add_new_data(self, name: str, date_year: str, date_month: str, date_day: str, row: str, column: str,
                     time_minutes: str, time_seconds: str, score: str):
        data = self.parse_xml_data()
        new_data = OrderedDict()
        new_data['name'] = name
        new_data['date'] = OrderedDict({'year': date_year, 'month': date_month, 'day': date_day})
        new_data['dimensions'] = OrderedDict({'row': row, 'column': column})
        new_data['time'] = OrderedDict({'minutes': time_minutes, 'seconds': time_seconds})
        new_data['score'] = score
        if data['leaderboard'] is None:
            new_data['@rank'] = '1'
            data['leaderboard'] = {'player': []}
            data['leaderboard']['player'].append(new_data)
        elif isinstance(data['leaderboard']['player'], OrderedDict):
            print('ping')
            data_list = [data['leaderboard']['player']]
            print(data_list)
            if int(score) > int(data_list[0]['score']):
                new_data['@rank'] = '1'
                data_list[0]['@rank'] = '2'
            else:
                new_data['@rank'] = '2'
            data_list.append(new_data)
            data['leaderboard']['player'] = data_list
            print(data['leaderboard']['player'])
        else:
            data_list = data['leaderboard']['player']
            data_list.sort(reverse=True, key=lambda x: int(x['@rank']))
            new_data['@rank'] = str(len(data_list)+1)
            for i in range(len(data_list)):
                if int(score) > int(data_list[i]['score']):
                    new_data['@rank'] = data_list[i]['@rank']
                    print(new_data['@rank'])
                    data_list[i]['@rank'] = str(int(data_list[i]['@rank']) + 1)
                    continue
                else:
                    break
            if len(data_list) >= self.max_data >= int(new_data['@rank']):
                data_list.pop(0)
                data_list.append(new_data)
            elif len(data_list) < self.max_data and int(new_data['@rank']) <= self.max_data:
                data_list.append(new_data)
            data_list.sort(key=lambda x: int(x['@rank']))
            data['leaderboard']['player'] = data_list
        xml_format = xmltodict.unparse(data, pretty=True)
        with open(self.data_file, 'w') as f:
            f.write(xml_format)


if __name__ == "__main__":
    dh = DataHandler()
    dh.add_new_data('blimey3', '2008', '06', '5', '3', '3', '5', '45', '22050')
