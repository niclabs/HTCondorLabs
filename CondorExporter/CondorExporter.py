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
from JobStateMetric import JobStateMetric
from CondorJobCluster import CondorJobCluster
from CondorJob import CondorJob

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


def parse_submitter(user):
    # User is a string in the form "username@machine" we want only the 'machine' part
    regex_match = re.compile(r'.*@(.*)$').match(user)
    if regex_match is not None:
        return regex_match.group(1)
    return ""

def get_all_submitters():
    return [1]


def get_jobs_from_submitter(submitter):
    projection = ["Owner", "User", "ExitStatus", "Cmd", "ClusterId", "ProcId",
                  "GlobalJobId", "JobStatus", "RemoteSlotID", "RemoteHost"]
    #requirements = 'Machine =?= %s' % submitter.name
    jobs_from_submitter = schedd.xquery(projection=projection)
    clusters = {}
    for job in jobs_from_submitter:
        cluster_id = job.get("ClusterId", None)
        job_id = job.get("ProcId", None)
        status = job.get("JobStatus", None)
        submitter = job.get("User", "")
        job = CondorJob(job_id)
        job.state = parse_job_status(status)
        if cluster_id not in clusters:
            new_cluster = CondorJobCluster(cluster_id, parse_submitter(submitter))
            clusters[cluster_id] = new_cluster
        clusters[cluster_id].jobs.append(job)
    return [cluster for cluster in clusters.itervalues()]


def parse_job_status(status_code):
    if status_code == 1:
        return "Idle"
    elif status_code == 2:
        return "Running"
    elif status_code == 5:
        return "Held"
    return ""


class CondorCollector(object):

    def __init__(self):
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

    def collect_machine_metrics(self, activity_metrics, state_metrics):
        machines = self.query_all_machines()
        for machines in machines:
            machines.update_activity(activity_metrics)
            machines.update_state(state_metrics)

    def collect_job_metrics(self, job_metrics):
        submitters = get_all_submitters()
        for submitter in submitters:
            for job in get_jobs_from_submitter(submitter):
                job.update_job_state(job_metrics)

    def collect(self):
        activity_metrics = SlotActivityMetric()
        state_metrics = SlotStateMetric()
        job_state_metrics = JobStateMetric()
        metrics = [activity_metrics, state_metrics, job_state_metrics]

        self.collect_machine_metrics(activity_metrics, state_metrics)
        self.collect_job_metrics(job_state_metrics)
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
