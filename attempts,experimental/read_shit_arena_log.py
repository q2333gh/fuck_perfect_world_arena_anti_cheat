import win32evtlog


def read_event_logs(service_name):
    server = "localhost"
    log_type = "System"
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    hand = win32evtlog.OpenEventLog(server, log_type)

    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    print(f"Total events in {log_type} log: {total}")

    events = []
    while True:
        events_list = win32evtlog.ReadEventLog(hand, flags, 0)
        if not events_list:
            break
        for event in events_list:
            if service_name in str(event.StringInserts):
                events.append(event)

    win32evtlog.CloseEventLog(hand)
    return events


def print_event_logs(events):
    for event in events:
        print(f"Event Category: {event.EventCategory}")
        print(f"Time Generated: {event.TimeGenerated}")
        print(f"Source Name: {event.SourceName}")
        print(f"Event ID: {event.EventID}")
        print(f"Event Type: {event.EventType}")
        print(f"Event Data: {event.StringInserts}")
        print("-" * 50)


service_name = "MessageTransfer"
events = read_event_logs(service_name)
print_event_logs(events)
