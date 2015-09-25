from pyleus.storm import SimpleBolt
from kafka import SimpleProducer, KafkaClient
from datetime import datetime
import logging
import logging.config

log = logging.getLogger("storm_log_analyzer.bolt.alarm_bolt")

class AlarmBolt(SimpleBolt):

    OUTPUT_FIELDS = ['error']


    def initialize(self):
        self.base_error_timestamp = ''
        self.current_error_timestamp = ''
        self.counter = 0
        self.kafka = KafkaClient('localhost:9092')
        self.producer = SimpleProducer(self.kafka)

    def _check_time(self, timestamp_new, timestamp_current):
        return (timestamp_new - timestamp_current).total_seconds() <= 180


    def process_tuple(self, tup):
        timestamp = tup.values[0]
        new_timestamp = datetime.strptime(timestamp,
                                          "%Y-%m-%d %H:%M:%S.%f")
        log.info("Alarm Bolt Received timestamp: %r", timestamp)
        if self.base_error_timestamp:
            if self._check_time(new_timestamp, self.base_error_timestamp):
                self.current_error_timestamp = new_timestamp
                self.counter += 1
            else:
                if self.current_error_timestamp:
                    if self._check_time(new_timestamp,
                                        self.current_error_timestamp):
                        self.base_error_timestamp = self.current_error_timestamp
                        self.current_error_timestamp = new_timestamp
                        self.counter = 2
                    else:
                        self.base_error_timestamp = new_timestamp
                        self.counter = 1
                else:
                    self.base_error_timestamp = new_timestamp
                    self.counter = 1
        else:
            self.base_error_timestamp = new_timestamp
            self.counter = 1

        if self.counter >= 3:
            #emit to kafka an alarm
            self.producer.send_messages(b'alarm',
                                        b'Warning: There were 3 errors in the '
                                        'last 3 minutes')

if __name__ == '__main__':
    AlarmBolt().run()
