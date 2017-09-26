from prometheus_client.core import GaugeMetricFamily


class JobStateMetric:
    def __init__(self):
        self.idle = GaugeMetricFamily('condor_job_state_idle',
                                      'Number of jobs on the idle state for a given cluster and submitter',
                                      labels=['submitter', 'cluster'])
        self.running = GaugeMetricFamily('condor_job_state_running',
                                         'Number of jobs on the running state for a given cluster and submitter',
                                         labels=['submitter', 'cluster'])
        self.held = GaugeMetricFamily('condor_job_state_held',
                                      'Number of jobs on the held state for a given cluster and submitter',
                                      labels=['submitter', 'cluster'])

    def as_list(self):
        return [self.idle, self.running, self.held]
