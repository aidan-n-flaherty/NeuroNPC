from engine.enums.degree import Degree

class job():
    def __init__(self, jobTitle: str, jobDesc: str, jobLocation: list[int], jobSatisfaction: Degree, jobReward: Degree, jobRisk: Degree):
        self._jobTitle = jobTitle               #title of job
        self._jobDesc = jobDesc                 #short description of what the job is
        self._jobLocation = jobLocation         #List of Location ID of where the job happens
        self._jobSatisfaction = jobSatisfaction #rating from 1-7 of how happy the NPC is with the job
        self._jobReward = jobReward             #rating from 1-7 of how much the NPC is rewarded for completing the job
        self._jobRisk = jobRisk                 #rating from 1-7 of how dangerous the job is

        #use degree enums for rating
    
    def getJob(self):
        return self._jobTitle
    
    def getJobDesc(self):
        return self._jobDesc
    
    def getJobLocation(self):
        return self._jobLocation
    
    def getJobSatisfaction(self):
        return self._jobSatisfaction
    
    def getJobReward(self):
        return self._jobReward
    
    def getJobRisk(self):
        return self._jobRisk
    
    def updateJobReward(self, newReward: Degree):
        self._jobReward = newReward
    
    def updateJobTitles(self, newJobTitle: str, newJobDesc: str):
        self._jobTitle = newJobTitle
        self._jobDesc = newJobDesc
    
    def updateJobLocation(self, newJobLocation: list[int]):
        self._jobLocation = newJobLocation
    
    def updateJobSatisfaction(self, newJobSatisfaction: Degree):
        self._jobSatisfaction = newJobSatisfaction
    
    def updateJobRisk(self, newJobRisk: Degree):
        self._jobRisk = newJobRisk

    def newJob(self, newJob: str, newJobDesc: str, newJobLocation: list[int], newJobsatisfaction: Degree, newJobReward: Degree, newJobRisk: Degree):
        self.updateJobTitles(newJob, newJobDesc)
        self.updateJobReward(newJobReward)
        self.updateJobLocation(newJobLocation)
        self.updateJobRisk(newJobRisk)
        self.updateJobSatisfaction(newJobsatisfaction)

    def getIdentifier(self) -> str:
        return 'This NPC has a job called: "{jobtitle}", this job does: {jobdesc} at these location IDS {jobloc}. On a scale from VERY_LOW to VERY_HIGH, this job is "{satisfying}" satisfying, "{reward}" rewarding, and "{risk}" dangerous'.format(jobtitle=self._jobTitle, jobdesc=self._jobDesc, jobloc=self._jobLocation, satisfying=self._jobSatisfaction, reward=self._jobReward,risk=self._jobRisk)