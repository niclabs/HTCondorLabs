
class CondorJobCluster:
    def __init__(self, cluster_id, submitter):
        self.cluster_id = cluster_id
        self.submitter = submitter
        self.jobs = []

    def update_job_state(self, state_metric):
        count_held = 0
        count_idle = 0
        count_running = 0
        for job in self.jobs:
            if job.state == "Running":
                count_running += 1
            elif job.state == "Idle":
                count_idle += 1
            elif job.state == "Held":
                count_held += 1

        state_metric.idle.add_metric([self.submitter, str(self.cluster_id)], count_idle)
        state_metric.held.add_metric([self.submitter, str(self.cluster_id)], count_held)
        state_metric.running.add_metric([self.submitter, str(self.cluster_id)], count_running)


