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
from JobRunningTimeMetric import JobRunningTimeMetric
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


def get_cluster_history(cluster):
    requirements = 'Machine =?= %s && ClusterId == %d' % (cluster.submitter, cluster.cluster_id)
    projection = ["Owner", "ExitStatus", "ProcId", "JobStatus", "RemoteSlotID", "RemoteHost", "RemoteWallClockTime"]
    jobs = schedd.history(requirements, projection)
    for job in jobs:
        job_id = job.get("ProcId", -1)
        status = job.get("JobStatus", "")
        time = job.get("RemoteWallClockTime", 0)
        if job not in cluster.jobs:
            cluster.jobs[job_id] = CondorJob(job_id)
        current_job = cluster.jobs[job_id]
        current_job.state = parse_job_status(status)
        current_job.running_time = time


def parse_job_status(status_code):
    if status_code == 1:
        return "Idle"
    elif status_code == 2:
        return "Running"
    elif status_code == 5:
        return "Held"
    elif status_code == 4:
        return "Completed"
    return ""


class CondorCollector(object):

    def __init__(self):
        self.machines = {}
        self.clusters = {}

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

    def get_jobs_from_submitter(self, submitter):
        projection = ["Owner", "User", "ExitStatus", "Cmd", "ClusterId", "ProcId",
                      "GlobalJobId", "JobStatus", "RemoteSlotID", "RemoteHost"]
        # requirements = 'Machine =?= %s' % submitter.name
        jobs_from_submitter = schedd.xquery(projection=projection)
        for job in jobs_from_submitter:
            cluster_id = job.get("ClusterId", None)
            job_id = job.get("ProcId", None)
            status = job.get("JobStatus", None)
            submitter = job.get("User", "")
            if cluster_id not in self.clusters:
                self.clusters[cluster_id] = CondorJobCluster(cluster_id, parse_submitter(submitter))
            self.clusters[cluster_id].active = True
            if job_id not in self.clusters[cluster_id].jobs:
                self.clusters[cluster_id].jobs[job_id] = CondorJob(job_id)
                self.clusters[cluster_id].jobs[job_id].state = parse_job_status(status)
            if self.clusters[cluster_id].jobs[job_id].state == "Running":
                self.clusters[cluster_id].jobs[job_id].execute_machine = job.get("RemoteHost", 0)
        for cluster in self.clusters.itervalues():
            get_cluster_history(cluster)
            if not cluster.active:
                del self.clusters[cluster.cluster_id]
        return [cluster for cluster in self.clusters.itervalues()]

    def collect_job_metrics(self, job_state_metrics, job_time_metrics):
        for cluster in self.clusters.itervalues():
            cluster.active = False
        submitters = get_all_submitters()
        for submitter in submitters:
            for job in self.get_jobs_from_submitter(submitter):
                job.update_job_state(job_state_metrics)
                job.update_job_running_time(job_time_metrics)

    def collect(self):
        activity_metrics = SlotActivityMetric()
        state_metrics = SlotStateMetric()
        job_state_metrics = JobStateMetric()
        job_time_metrics = JobRunningTimeMetric()
        metrics = [activity_metrics, state_metrics, job_state_metrics, job_time_metrics]

        self.collect_machine_metrics(activity_metrics, state_metrics)
        self.collect_job_metrics(job_state_metrics, job_time_metrics)
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
