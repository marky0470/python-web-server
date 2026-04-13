#issues: sub1: cb1, no args -> event_type <- cb2, args

class Event:

    def __init__(self):
        self.events = {}

    def register_event(self, event_type):
        try:
            self.events[event_type]
        except KeyError:
            self.events[event_type] = []

    def register_callback(self, event_type, callback, args=None):
        try:
            self.events[event_type].append(callback)
        except KeyError:
            print("Attempt to register callback to non-existent event type")

    def trigger(self, event_type, args):
        try:
            events = self.events[event_type]
        except KeyError:
            print("Attempt to trigger callbacks for event type that does not exist")
            return
        
        print(self.events[event_type])
        for event in events:
            print(f"Triggering callback {event} with arguments {args}")
            event(args)
