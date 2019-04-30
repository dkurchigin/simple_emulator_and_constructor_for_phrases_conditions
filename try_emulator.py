test_phrase = "да конечно нет"

class PhrasesConditions:
    def __init__(self, name="defaul_name", description="", *phrases_classes):
        self.name = name
        self.description = description
        self.phrases_classes = phrases_classes
        self.load_phrases_classes()
        
    def __str__(self):
        return self.phrases_classes
        
    def load_phrases_classes(self):
        for element in self.phrases_classes:
            print('this \"{}\"'.format(element.basic_phrase))
        
class PhraseClass:
    def __init__(self, basic_phrase, phrases_parts="test", next_state="test"):
        self.basic_phrase = basic_phrase
        self.phrases_parts = phrases_parts
        self.next_state = next_state
    
    def __str__(self):
        return '\"{}\"'.format(self.basic_phrase)
        
        
yes = PhraseClass("да конечно")
print(yes)
no = PhraseClass("нет конечно")
print(no)

yes_no_conditions = PhrasesConditions("yes_no_conditions", "", yes, no)
#yes_no_conditions.load_phrases_classes(yes, no)