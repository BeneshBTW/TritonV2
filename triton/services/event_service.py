class EventService():
    def __init__(self, event_store):
        self.event_store = event_store

    def get_events(self) -> list[dict]:
        return self.event_store.load()
    
    def add_event(self, title: str, date: str, time: str) -> dict:
        events = self.get_events()

        event = {
            "title": title,
            "date": date,
            "time": time
        }

        events.append(event)
        self.event_store.save(events)

        return event
    
    def remove_event(self, event_number: int) -> dict | None:
        events = self.get_events()
        event_index = event_number - 1

        if event_index < 0 or event_index >= len(events):
            return None
        
        removed_event = events.pop(event_index)
        self.event_store.save(events)

        return {
            "index": event_index,
            "events": removed_event
        }

    def restore_event(self,index: int, event: dict) -> None:
        events = self.get_events()
        events.insert(index, event)
        self.event_store.save(events)

    def clear_events(self) -> list[dict]:
        events = self.get_events()
        self.event_store.save([])
        return events 
