import xmltodict
from collections import OrderedDict
import os


class DataHandler(object):
    """
    This class interacts with the .xml file which records the data of previous players with the highest scores
    obtained.
    """

    # We shall use the first file listed in data/
    dirname = os.path.dirname(__file__)
    data_dir = os.path.join(dirname, r'data/')
    data_file = data_dir + os.listdir(data_dir)[0]

    # We shall only store up to this amount of player data
    max_data = 5

    def __init__(self):
        if not (os.path.isfile(self.data_file) or self.data_file.endswith('.xml')):
            raise IOError("File not suitable. Is it an XML file? Make sure the root element is 'leaderboard'.")

    @classmethod
    def change_data_file_path(cls, new_path: str):
        """
        change which file is used for this static class. Must be in .xml format
        :param new_path:
        :return:
        """
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
    def get_leaderboard_data(cls):
        """
        Get leaderboard data in a dictionary format. The result is slightly different compared to using xmltodict.parse
        :return:
        """
        leaderboard_data = {}
        raw_data = cls.parse_xml_data()
        if raw_data['leaderboard'] is not None:
            p_data = raw_data['leaderboard']['player']
            if isinstance(p_data, OrderedDict):
                leaderboard_data[p_data['@rank']] = {
                    'name': p_data['name'],
                    'date': f"{p_data['date']['year']}-{p_data['date']['month']}-{p_data['date']['day']}",
                    'dimensions': f"{p_data['dimensions']['row']}x{p_data['dimensions']['column']}",
                    'time': f"{p_data['time']['minutes']}:{p_data['time']['seconds']}",
                    'score': p_data['score'],
                }
            else:
                for i in range(len(p_data)):
                    leaderboard_data[p_data[i]['@rank']] = {
                        'name': p_data[i]['name'],
                        'date': f"{p_data[i]['date']['year']}-{p_data[i]['date']['month']}-{p_data[i]['date']['day']}",
                        'dimensions': f"{p_data[i]['dimensions']['row']}x{p_data[i]['dimensions']['column']}",
                        'time': f"{p_data[i]['time']['minutes']}:{p_data[i]['time']['seconds']}",
                        'score': p_data[i]['score'],
                    }
        return leaderboard_data

    @classmethod
    def new_high_score(cls, score: str):
        """
        Check if the player is qualified to add their name to the leaderboard based on their score.
        :param score: player score
        :return:
        """
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
        """
        Add player data to the XML file by parsing data in dictionary form, modifying it and writing the final
        result. We include the following parameters below to the XML file and automatically calculate the rank
        based on score which is also included with the rest of the data. Recommended to pass the arguments via
        a dictionary (using the ** notation).
        :param name:
        :param date_year:
        :param date_month:
        :param date_day:
        :param row:
        :param column:
        :param time_minutes:
        :param time_seconds:
        :param score:
        :return:
        """
        data = cls.parse_xml_data()
        new_data = OrderedDict({
            'name': name,
            'date': OrderedDict({'year': date_year, 'month': date_month, 'day': date_day}),
            'dimensions': OrderedDict({'row': row, 'column': column}),
            'time': OrderedDict({'minutes': time_minutes, 'seconds': time_seconds}),
            'score': score,
        })

        # If there is no data, manually add 'player' environment
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
            new_data['@rank'] = str(len(data_list) + 1)
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

        # Write new xml format to file
        xml_format = xmltodict.unparse(data, pretty=True)
        with open(cls.data_file, 'w') as f:
            f.write(xml_format)


if __name__ == "__main__":
    from pprint import pprint
    test = DataHandler.get_leaderboard_data()
    pprint(test)
