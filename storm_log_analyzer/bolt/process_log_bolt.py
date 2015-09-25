from pyleus.storm import SimpleBolt
import logging
import logging.config

log = logging.getLogger("storm_log_analyzer.bolt.process_log_bolt")

class ProcessLogBolt(SimpleBolt):

    OUTPUT_FIELDS = ['timestamp']

    def process_tuple(self, tup):
        log_line = tup.values[0]
        line = log_line.split(' ')
        log.info(log_line)
        log.info(line)
        if 'ERROR' in log_line:
            line = log_line.split(' ')
            timestamp = line[0] + ' ' + line[1]
            log.info("Process Bolt Emitted timestamp: %r", timestamp)
            #emit timestamp of error
            self.emit((timestamp,), anchors=[tup])

if __name__ == '__main__':
    ProcessLogBolt().run()
