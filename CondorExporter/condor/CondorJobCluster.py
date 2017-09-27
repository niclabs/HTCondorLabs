
class CondorJobCluster:
    def __init__(self, cluster_id, submitter):
        self.cluster_id = cluster_id
        self.submitter = submitter
        self.jobs = {}
        self.active = False

    def update_job_state(self, state_metric):
        count_held = 0
        count_idle = 0
        count_running = 0
        count_completed = 0
        for job in self.jobs.itervalues():
            if job.state == "Running":
                count_running += 1
            elif job.state == "Idle":
                count_idle += 1
            elif job.state == "Held":
                count_held += 1
            elif job.state == "Completed":
                count_completed += 1

        state_metric.idle.add_metric([self.submitter, str(self.cluster_id)], count_idle)
        state_metric.held.add_metric([self.submitter, str(self.cluster_id)], count_held)
        state_metric.running.add_metric([self.submitter, str(self.cluster_id)], count_running)
        state_metric.completed.add_metric([self.submitter, str(self.cluster_id)], count_completed)

    def update_job_running_time(self, runtime_metric):
        runtime_sum = 0.0
        runtime_count = 0.0
        for job in self.jobs.itervalues():
            if job.state == "Completed":
                runtime_sum += job.running_time
                runtime_count += 1
        runtime_metric.time.add_metric([self.submitter, str(self.cluster_id)], runtime_sum / runtime_count)

