
class CondorJob:

    def __init__(self, job_id):
        self.job_id = job_id
        self.state = None
        self.execute_machine = None
