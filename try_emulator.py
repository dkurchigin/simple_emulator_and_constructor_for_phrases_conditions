import json
import re
import os
import sqlite3

test_phrase = "да конечно нет"


class NewScript:
    def __init__(self, json_file):
        self.json_file = json_file
        self.database_file = json_file + ".db"
        self.load_phrases_from_json()

    def load_phrases_from_json(self):
        with open(self.json_file, "r", encoding='utf-8') as read_file:
            loaded_json = json.load(read_file)
            self._check_db_exist(loaded_json)

    def get_dict_content(self, dict_name, phrase):
        con = sqlite3.connect(self.database_file)
        cur = con.cursor()
        cur.execute('SELECT dict_content FROM rule_dicts WHERE dict_name like \"{}\"'.format(dict_name))

        for rule_in_dict in list(cur.fetchone()):
            rule_in_dict = re.sub(r'\"', '', rule_in_dict)
            if re.match(rule_in_dict, phrase):
                print('{} matched in {}'.format(phrase, rule_in_dict))

        con.commit()
        con.close()

    def _check_db_exist(self, loaded_json):
        while True:
            if os.path.isfile(self.database_file):
                print("База данных {} уже существует. Переписать?".format(self.database_file))
                print("(Y)es | (N)o?")

                answer = input()
                pattern_for_yes = '(^[yY]$|^[yY][eE][sS]$|^[дД]$|^[дД][аА]$)'

                if re.match(pattern_for_yes, answer):
                    os.remove(self.database_file)
                    print("Удаляю старую версию базы данных {}".format(self.database_file))
                else:
                    break
            else:
                self._create_db(self.database_file)
                print("Создана база: {}".format(self.database_file))
                self._parse_phrases(loaded_json["phrases"], self.database_file)
                break

    def _create_db(self, database_file):
        con = sqlite3.connect(database_file)
        cur = con.cursor()
        cur.execute('CREATE TABLE rule_dicts (id INTEGER PRIMARY KEY, dict_name VARCHAR(128), dict_content TEXT)')
        con.commit()
        con.close()

    def _write_data(self, database_file, dict_sql):
        con = sqlite3.connect(database_file)
        cur = con.cursor()
        for key, value in dict_sql.items():
            cur.execute(
                'INSERT INTO rule_dicts (id, dict_name, dict_content) VALUES(NULL, \'{}\', \'{}\')'.format(key, value))
        con.commit()
        con.close()

    def _format_list_to_str(self, input_list):
        out_str = ""
        for rule in input_list:
            out_str = out_str + "\"{}\"".format(rule)
            if not input_list.index(rule) == (len(input_list) - 1):
                out_str = out_str + ",\n"
        return out_str

    def _parse_phrases(self, rule_dicts, db_extension):
        for key, value in rule_dicts.items():
            pure_value = self._format_list_to_str(value)
            rule_dicts[key] = pure_value
            #print("{}\n{}\n\n".format(key, pure_value))
        self._write_data(db_extension, rule_dicts)


class PhrasesConditions:
    def __init__(self, name="defaul_name", description="", *phrases_classes):
        self.name = name
        self.description = description
        self.phrases_classes = phrases_classes
        #self.load_phrases_classes()
        
    def __str__(self):
        return self.phrases_classes
        
    def load_phrases_classes(self):
        for element in self.phrases_classes:
            print('this \"{}\"'.format(element.basic_phrase))

    def match_phrase(self, phrase):
        for phrase_class in self.phrases_classes:
            phrase_class.try_match_phrase(phrase)


class PhraseClass:
    def __init__(self, basic_phrase, *phrases_parts, next_state="test"):
        self.basic_phrase = basic_phrase
        self.phrases_parts = phrases_parts
        self.next_state = next_state
        self.try_match_phrase(self.basic_phrase)
    
    def __str__(self):
        return '\"{}\"'.format(self.basic_phrase)

    def try_match_phrase(self, phrase):
        for part in list(self.phrases_parts[0]):
            #print(robotization.database_file)
            robotization.get_dict_content(part, phrase)
            #print("dict {}".format(part))


robotization = NewScript('RobotizationCalls.json')
yes = PhraseClass("да конечно", ["Yes", "Need"])
print(yes)
no = PhraseClass("нет конечно", ["SayNo"])
print(no)

yes_no_conditions = PhrasesConditions("yes_no_conditions", "", yes, no)

#yes_no_conditions.load_phrases_classes(yes, no)
