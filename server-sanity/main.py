import datetime
import os
import random
import sys
import threading
import time

import pika
import requests


class Consumer(threading.Thread):
    CLOCKS_PATH = "https://ticktok-io-dev.herokuapp.com/api/v1/clocks?access_token=%s" % os.environ["TICKTOK_TOKEN"]


    channel = None

    def __init__(self, name, schedule, on_tick_callback):
        threading.Thread.__init__(self)
        self.name = name
        self.schedule = schedule
        self.on_tick_callback = on_tick_callback

    def run(self):
        clock = self.create_clock()
        self.listen_on_ticks(clock["channel"])

    def create_clock(self):
        response = requests.post(self.CLOCKS_PATH, json={'name': self.name, 'schedule': self.schedule})
        assert response.status_code == 201, response.text
        print("Created a clock [name: %s, schedule: %s]" % (self.name, self.schedule))
        return response.json()

    def listen_on_ticks(self, clock_channel):
        connection = pika.BlockingConnection(pika.connection.URLParameters(clock_channel["uri"]))
        self.channel = connection.channel()
        self.channel.basic_consume(self.tick, queue=clock_channel['queue'])
        self.channel.start_consuming()

    def tick(self, ch, method, properties, body):
        self.on_tick_callback(self.name, self.schedule)

    def stop(self):
        if self.channel is not None:
            self.channel.stop_consuming()


class TicktokTester(object):
    FILE_NAME = "ticktok-results-%s.csv" % str(round(time.time()))
    NUM_OF_TICKS = 10

    consumers = {}
    counters = {}

    def test(self, num_of_clocks, consumers_per_clock):
        for clockIdx in range(0, num_of_clocks):
            schedule = self.draw_schedule()
            for consumerIdx in range(0, consumers_per_clock):
                self.invoke_consumer_for("test-consumer-%s" % clockIdx, schedule)
        self.wait_for_consumer_to_finish()

    def draw_schedule(self):
        secs = random.randint(1, 5)
        return "every.%s.seconds" % secs

    def invoke_consumer_for(self, name, schedule):
        consumer = Consumer(name, schedule, self.on_tick_callback)
        consumer.start()
        if not (name in self.consumers):
            self.consumers[name] = []
        self.consumers[name].append(consumer)
        self.counters[name] = 0

    def on_tick_callback(self, name, schedule):
        self.counters[name] += 1
        with open(self.FILE_NAME, "a") as file:
            file.write("%s, %s, %s, %s\n" % (str(datetime.datetime.now()), name, schedule, self.counters[name]))
        sys.stdout.flush()
        self.stop_all_consumers_for(name)

    def stop_all_consumers_for(self, name):
        if self.counters[name] >= self.NUM_OF_TICKS:
            print("Stopping consumers for: %s" % name)
            for c in self.consumers[name]:
                c.stop()

    def wait_for_consumer_to_finish(self):
        for key, value in self.consumers.items():
            for consumer in value:
                consumer.join()


if __name__ == '__main__':
    TicktokTester().test(1, 1)
    print("done")
