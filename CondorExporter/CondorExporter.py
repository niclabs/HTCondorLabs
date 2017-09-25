#!/usr/bin/python


import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

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


def parse_address(address):
#   regex_match = re.compile(r'.*p="primary"; a="([\d.]*)"; port.*}').match(address)
    regex_match = re.compile(r'<(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):.*').match(address)
    if regex_match is not None:
        return regex_match.group(1)
    return ""


def get_all_submitters():
    pass


def get_jobs_from_submitter(submitter):
    pass


def parse_job_status(status_code):
    if status_code == 0:
        return ""
    elif status_code == 1:
        return ""
    elif status_code == 2:
        return ""
    return ""


class CondorCollector(object):

    def __init__(self):
        self.activity_metrics = SlotActivityMetric()
        self.state_metrics = SlotStateMetric()
        self.metrics = [self.activity_metrics, self.state_metrics]
        self.machines = {}

    def get_machine_list(self):
        return [machine for machine in self.machines.itervalues()]

    def query_all_machines(self):
        projection = ["Machine", "State", "Name", "SlotID", "Activity", "MyAddress"]
        slots_info = query_all_slots(projection=projection)
        for machine in self.machines.itervalues():
            machine.reset_slots_metrics()
        for slot in slots_info:
            name = slot.get("Machine", None)
            slot_id = slot.get("SlotID", None)
            activity = slot.get("Activity", None)
            state = slot.get("State", None)
            address = slot.get("MyAddress", "")
            if name not in self.machines:
                self.machines[name] = Machine(name, parse_address(address))
            current_machine = self.machines[name]
            if slot_id not in current_machine.slots:
                current_machine.slots[slot_id] = Slot(slot_id)
            current_slot = current_machine.slots[slot_id]
            current_slot.activity = activity
            current_slot.state = state
        return self.get_machine_list()

    def collect_machine_metrics(self):
        machines = self.query_all_machines()
        for machines in machines:
            machines.update_activity(self.activity_metrics)
            machines.update_state(self.state_metrics)

    def collect_job_metrics(self):
        pass

    def collect(self):
        self.collect_machine_metrics()
        self.collect_job_metrics()
        metrics_list = []
        for m in self.metrics:
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
