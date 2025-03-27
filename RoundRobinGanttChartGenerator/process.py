#Note to self: This was the original version, changed approach to a pandas dataframe
class Process:
    p_count = 0
    time = 0

    #each index will represent the info of a process across these 3 lists,
    #  aftter the scheduler allows for a process to be serviced by a quantum
    # check if it's service time < quantum, if so remove from the ready queue,
    #  and only increse time by the proceses' service-time 
    # else move to the back of queue and increase time by a quantum,
    # after the whole ready queue has been serviced add newly arrived prpocesses 
    # to the [processing queue] from the ready-to-process queue
        #MUST MOVE FROM FORNT TO BACK IN CONJUNCTION:
        #or maybe use a dataframe???

    arrival_times = []
    inter_arrival_times = []
    service_times = []

    def __init__(self, num_processes, inter_arrival_time):
        while p_count < num_processes:

            Process.p_count #implements the class level attribute
            p_count += 1 
            self.ID=Process.p_count #automatic variable
