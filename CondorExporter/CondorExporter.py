#!/usr/bin/python


import time

from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

import htcondor
import re

from CondorMachine import Machine
from CondorSlot import Slot
from SlotActivityMetric import SlotActivityMetric
from SlotStateMetric import SlotStateMetric

schedd = htcondor.Schedd()


def query_all_slots(projection=[]):
    coll = htcondor.Collector()
    all_submitters_query = coll.query(htcondor.AdTypes.Startd, projection=projection)
    return all_submitters_query


def parse_address(addressV1):
    regex_match = re.compile(r'.*p="primary"; a="([\d.]*)"; port.*}').match(addressV1)
    if regex_match is not None:
        return regex_match.group(1)
    return ""


def get_all_machines():
    projection = ["Machine", "State", "Name", "SlotID", "Activity", "AddressV1"]
    slots_info = query_all_slots(projection=projection)
    machines = {}
    for slot in slots_info:
        name = slot.get("Machine", None)
        slot_id = slot.get("SlotID", None)
        activity = slot.get("Activity", None)
        state = slot.get("State", None)
        address = slot.get("AddressV1", None)
        if name not in machines:
            machines[name] = Machine(name, parse_address(address))
        current_slot = Slot(slot_id)
        current_slot.activity = activity
        current_slot.state = state
        machines[name].slots.append(current_slot)
    return machines.itervalues()


class CondorCollector(object):

    def __init__(self):
        self.metrics = {}

    def setup_empty_prometheus_metrics(self):
        self.metrics = {}

    def collect(self):
        machines = get_all_machines()
        activity_metrics = SlotActivityMetric()
        state_metrics = SlotStateMetric()
        metrics = [activity_metrics, state_metrics]
        for machines in machines:
            machines.update_activity(activity_metrics)
            machines.update_state(state_metrics)

        metrics_list = []
        for m in metrics:
            metrics_list += m.as_list()
        for m in metrics_list:
            yield m


def main():
    try:
        REGISTRY.register(CondorCollector())
        start_http_server(9118)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted, Shutting down")
        exit(0)


if __name__ == "__main__":
    main()
