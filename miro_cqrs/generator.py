from dataclasses import dataclass
import os
import time

import requests

BOARD_ID = os.environ["BOARD_ID"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

URL = f"https://api.miro.com/v2/boards/{BOARD_ID}/sticky_notes"
CONNECTOR_URL = f"https://api.miro.com/v2-experimental/boards/{BOARD_ID}/connectors"


def generate_aggregate(content):
    return {
        "data": {
            "content": f"{content}",
            "shape": "square",
        },
        "style": {"fillColor": "yellow"},
        "position": {"origin": "center", "x": 0, "y": 0},
        "geometry": {"width": 199.0},
    }


def generate_command(content):
    return {
        "data": {
            "content": f"{content}",
            "shape": "square",
        },
        "style": {"fillColor": "light_blue"},
        "position": {"origin": "center", "x": 0, "y": 0},
        "geometry": {"width": 199.0},
    }


def generate_event(content):
    return {
        "data": {
            "content": f"{content}",
            "shape": "square",
        },
        "style": {"fillColor": "orange"},
        "position": {"origin": "center", "x": 0, "y": 0},
        "geometry": {"width": 199.0},
    }


def generate_line(start_id, end_id):
    return {"startItem": {"id": f"{start_id}"}, "endItem": {"id": f"{end_id}"}}


@dataclass
class Content:
    title: str
    fields: list = None

    def to_string(self) -> str:
        fields = [f"- {i}" for i in self.fields or []]
        content_list = [self.title] + fields
        content_list = [f"<p>{i}</p>" for i in content_list]
        return "".join(content_list)


if __name__ == "__main__":
    aggregate_content = Content(title="An Aggregate", fields=["id", "name"]).to_string()
    event_content = Content(title="Something Happended", fields=["name"]).to_string()
    command_content = Content(title="Do Something", fields=["name"]).to_string()

    aggregate_payload = generate_aggregate(aggregate_content)
    event_payload = generate_event(event_content)
    command_payload = generate_command(command_content)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BEARER_TOKEN}",
    }

    print("create command")
    c = requests.post(URL, json=command_payload, headers=headers)
    command_id = c.json()["id"]

    print("create event")
    e = requests.post(URL, json=event_payload, headers=headers)
    event_id = e.json()["id"]

    print("create aggregate")
    a = requests.post(URL, json=aggregate_payload, headers=headers)
    aggregate_id = a.json()["id"]

    line_payload1 = generate_line(event_id, aggregate_id)
    line_payload2 = generate_line(command_id, aggregate_id)

    print("create line from event to aggregate")
    requests.post(CONNECTOR_URL, json=line_payload1, headers=headers)

    print("create line from command to aggregate")
    requests.post(CONNECTOR_URL, json=line_payload2, headers=headers)
