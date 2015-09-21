from pyleus.storm import SimpleBolt

class ProcessLogBolt(SimpleBolt):

    OUTPUT_FIELDS = ['sentence']

    def process_tuple(self, tup):
        sentence = tup.values
        print sentence
        new_sentence = "\"{0}\"".format(sentence)
        self.emit((new_sentence,), anchors=[tup])

if __name__ == '__main__':
    ProcessLogBolt().run()
