from universal import config
import json
from views import dialogs


def save_events(app):
    try:
        events = app.textbox.get("0.0", "end")
        events = json.loads(events)
        events = add_id(events)
        app.exception_display(None)
        config.actions = events
        clean_data(app)

    except Exception as ex:

        app.exception_display(ex)


def clean_data(app):

    config.actions = add_id(config.actions)

    app.textbox.delete("0.0", "end")
    app.textbox.insert("0.0", json.dumps(config.actions, indent=2))


def insert_event(event, app):
    if event:
        config.actions.append(event)

    clean_data(app)


def add_id(events):

    for i, event in enumerate(events):
        new_event = dict(event)
        new_event["id"] = i
        events[i] = new_event

    return events


