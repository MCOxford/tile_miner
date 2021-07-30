import xmltodict
from collections import OrderedDict
import os


class DataHandler(object):

    # We shall use the first file listed in data/
    data_file = 'data/' + os.listdir(r'data/')[0]

    max_data = 5

    def __init__(self):
        if not (os.path.isfile(self.data_file) or self.data_file.endswith('.xml')):
            raise IOError("File not suitable. Is it an XML file? Make sure the root element is 'leaderboard'.")

    @classmethod
    def change_data_file_path(cls, new_path):
        if os.path.isfile(new_path) and new_path.endswith('.xml'):
            cls.data_file = new_path
            print("Assigning new file path: SUCCESSFUL")
        else:
            print("Assigning new file path: UNSUCCESSFUL")

    @classmethod
    def parse_xml_data(cls):
        with open(cls.data_file, 'r') as f:
            data = xmltodict.parse(f.read())
        return data

    @classmethod
    def new_high_score(cls, score: str):
        is_high_score = False
        data = cls.parse_xml_data()
        if data['leaderboard'] is None or isinstance(data['leaderboard']['player'], OrderedDict) or \
                0 < len(data['leaderboard']['player']) < cls.max_data:
            is_high_score = True
        else:
            scores = [int(data['leaderboard']['player'][i]['score']) for i in range(len(data['leaderboard']['player']))]
            lowest_score = min(scores)
            if int(score) > lowest_score:
                is_high_score = True
        return is_high_score

    @classmethod
    def add_new_player_data(cls, name: str, date_year: str, date_month: str, date_day: str, row: str, column: str,
                            time_minutes: str, time_seconds: str, score: str):
        data = cls.parse_xml_data()
        new_data = OrderedDict({
            'name': name,
            'date': OrderedDict({'year': date_year, 'month': date_month, 'day': date_day}),
            'dimensions': OrderedDict({'row': row, 'column': column}),
            'time': OrderedDict({'minutes': time_minutes, 'seconds': time_seconds}),
            'score': score,
        })
        if data['leaderboard'] is None:
            new_data['@rank'] = '1'
            data['leaderboard'] = {'player': [new_data]}
        # If there is only one set of player data recorded, we work with an ordered dictionary
        elif isinstance(data['leaderboard']['player'], OrderedDict):
            data_list = [data['leaderboard']['player']]
            if int(score) > int(data_list[0]['score']):
                new_data['@rank'] = '1'
                data_list[0]['@rank'] = '2'
            else:
                new_data['@rank'] = '2'
            data_list.append(new_data)
            data_list.sort(key=lambda x: int(x['@rank']))
            data['leaderboard']['player'] = data_list
        # In this case, we now work with a list
        else:
            data_list = data['leaderboard']['player']
            data_list.sort(reverse=True, key=lambda x: int(x['@rank']))
            new_data['@rank'] = str(len(data_list)+1)
            for i in range(len(data_list)):
                if int(score) > int(data_list[i]['score']):
                    new_data['@rank'] = data_list[i]['@rank']
                    data_list[i]['@rank'] = str(int(data_list[i]['@rank']) + 1)
                    continue
                else:
                    break
            if len(data_list) >= cls.max_data >= int(new_data['@rank']):
                data_list.pop(0)
                data_list.append(new_data)
            elif len(data_list) < cls.max_data and int(new_data['@rank']) <= cls.max_data:
                data_list.append(new_data)
            data_list.sort(key=lambda x: int(x['@rank']))
            data['leaderboard']['player'] = data_list
        xml_format = xmltodict.unparse(data, pretty=True)
        with open(cls.data_file, 'w') as f:
            f.write(xml_format)


if __name__ == "__main__":
    pass
