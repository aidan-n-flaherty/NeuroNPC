from engine.enums.degree import Degree
import random as Rand

class AutoJobs():
    #dictJobs-- Key: index and value: tuple(Jobtitle, Desc, listOfpossbile locations)
    def __init__(self, dictJobs: dict):
        self._dictOfAllJobs = dictJobs
        self._numberOfJobs = len(dictJobs)

    def addJob(self, jobTitle: str, jobDesc: str, listOfLocations: list[int]):
        newValue = (jobTitle, jobDesc, listOfLocations)
        self._dictOfAllJobs[self._numberOfJobs] = newValue
        self._numberOfJobs = self._numberOfJobs + 1

    # return 1 if succesfully removed. return 0 if no job in dict
    def removeJob(self, jobTitle:str):
        if jobTitle in self._dictOfAllJobs:
            self._dictOfAllJobs.pop(jobTitle)
            self._numberOfJobs = self._numberOfJobs - 1
            return 1
        else:
            return 0
    
    #change the information of a job already in the dict
    def changeJobInfo(self, jobTitle: str, jobDesc: str, listOfLocations: list[int]):
        self.removeJob(jobTitle)
        self.addJob(jobTitle,jobDesc,listOfLocations)

    def getJobDict(self) -> dict:
        return self._dictOfAllJobs
    
    def getNumJobs(self) -> int:
        return self._numberOfJobs

class Jobs():
    def __init__(self, jobTitle: str, jobDesc: str, jobLocation: list[int], jobSatisfaction: Degree, jobReward: Degree, jobRisk: Degree):
        self._jobTitle = jobTitle               #title of job
        self._jobDesc = jobDesc                 #short description of what the job is
        self._jobLocation = jobLocation         #List of Location ID of where the job happens
        self._jobSatisfaction = jobSatisfaction #rating from 1-7 of how happy the NPC is with the job
        self._jobReward = jobReward             #rating from 1-7 of how much the NPC is rewarded for completing the job
        self._jobRisk = jobRisk                 #rating from 1-7 of how dangerous the job is
        self._hasJob = True
        self._autoGiveJob = False

        #use degree enums for rating
    
    def __init__(self):
        self._hasJob = False
        self._autoGiveJob = False
        
    #auto assign a random job from the autojob object
    def __init__(self, autoJob: AutoJobs=None):

        if(autoJob):
            #give random job data
            dictOfJobs = autoJob.getJobDict()
            numberOfJobs = autoJob.getNumJobs()
            jobNumber = Rand.randint(0,numberOfJobs-1)
            jobtuple = dictOfJobs[jobNumber] # tuple formatted (jobtitle, jobdesc, possiblejoblocations)
            self._jobTitle = jobtuple[0]
            self._jobDesc = jobtuple[1]
            self._jobLocation = jobtuple[2]
            self._jobSatisfaction = Rand.randint(1,7)
            self._jobReward = Rand.randint(1,7)
            self._jobRisk = Rand.randint(1,7)
            self._hasJob = True
            self._autoGiveJob = True

        else:
           #pretend its jobless constuctor
           self._hasJob = False
           self._autoGiveJob = False
            

    
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
        if self._hasJob:
            return 'This NPC has a job called: "{jobtitle}", this job does: {jobdesc} at these location IDS {jobloc}. On a scale from VERY_LOW to VERY_HIGH, this job is "{satisfying}" satisfying, "{reward}" rewarding, and "{risk}" dangerous'.format(jobtitle=self._jobTitle, jobdesc=self._jobDesc, jobloc=self._jobLocation, satisfying=self._jobSatisfaction, reward=self._jobReward,risk=self._jobRisk)
        else:
            return 'this NPC is unemployed'