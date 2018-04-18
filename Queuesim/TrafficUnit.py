class TrafficUnit:
    def __init__(self, queue):
        self.action = queue.add_process()

    def response_time(self):
        try:
            return self.action.value
        except AttributeError:
            # Traffic still in the queue
            pass
