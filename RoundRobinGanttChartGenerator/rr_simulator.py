# Initialize variables
processes_to_generate = 100
quantum = 5
context_switch = 0

p_count = 0
q_count = 0

#random value generator functions
def generate_service_times(num_service_times=100, min_time=2, max_time=5):
    import random
    import numpy as np

    service_times = []
    random.seed(5)
    for i in range(num_service_times):
        rand_int= random.randint(min_time, max_time)
        service_times.append(rand_int)
    service_times = np.array(service_times)
    #print("Service Times:",service_times)
    #print("Service Times size:",len(service_times))
    return service_times

def generate_rand_arrival_times(num_arrivals=99, min_time=4, max_time=9):# modified to return 2 arrays inter_arrival_times[] and arrival_times[]
    import random
    import numpy as np
    arrivals = []
    arrivals.append(0)
    random.seed(5)
    for i in range(num_arrivals):
        rand_int= random.randint(min_time-1, max_time)
        arrivals.append(rand_int)
    inter_arrival_times = np.array(arrivals)
    #print("Inter Arrival Times:",np.array(inter_arrival_times),"\nInter Arrival Times:",len(inter_arrival_times))
    #arrival_times = np.cumsum(inter_arrival_times) #cumulative sum is a simple alternative
    arrival_times = []
    sum=0
    for i in inter_arrival_times:
        sum+=i
        arrival_times.append(sum)
    arrival_times = np.array(arrival_times)
    #print("\nArrival Times:",arrival_times,"\nArrival Times size:",len(arrival_times))
    return inter_arrival_times ,arrival_times

# Generate random arrival and service times
result = generate_rand_arrival_times(99, 4, 9)
inter_arrival_times = result[0]
arrival_times = result[1]
original_service_times = generate_service_times(100, 2, 10)

# Create the DataFrame
import pandas as pd
process_df = pd.DataFrame(columns=["Process ID", "Inter Arrival T", "Arrival T", "Service T", "Service T Left", "End T", "Turn Around T", "Total Wait T", "Initial Wait T", "Start T", "Status"])

process_df["Process ID"] = list(range(1, 1 + processes_to_generate))
process_df["Inter Arrival T"] = inter_arrival_times
process_df["Arrival T"] = arrival_times
process_df["Service T"] = original_service_times
process_df["Service T Left"] = original_service_times
process_df["Status"] = "Has not arrived"

# Initialize queues
ready_queue = []
service_queue = []

time = 0  # Start time

# Function to update the ready queue
def update_ready_queue():
    global ready_queue
    for index, row in process_df.iterrows():
        if row["Arrival T"] <= time and row["Status"] == "Has not arrived":
            ready_queue.append(row["Process ID"])
            process_df.loc[index, "Status"] = "Has Arrived, moving to service queue"

# Function to service the service queue
def service_service_queue():
    global time, service_queue
    for index, row in process_df[process_df["Process ID"].isin(service_queue)].iterrows():
        if pd.isnull(row["Start T"]): #If this is the firt time a processes is serviced, set "Start T" = time (current time)
            process_df.loc[index,"Start T"] = time # Set start time
            process_df.loc[index, "Initial wait time"] = time - row["Arrival T"] # Calculate initial wait time
            print("Time:", time,"Starting Process:", row["Process ID"],"Time Left:", row["Service T Left"])
        #updating the status to "In service"
        process_df.loc[index, "Status"] = "In Service"

        if row["Service T Left"] > quantum:  # Case 1: Service time > quantum
            time += quantum
            process_df.loc[index, "Service T Left"] -= quantum
            # Move process to the back of the queue
            service_queue.append(service_queue.pop(0))
            #print("Time:", time, "Servicing Process ID number:", row["Process ID"],"Time Left:", row["Service T Left", "Status:", row["Status"]])
            print("Time:", time, "Servicing Process ID number:", row["Process ID"], "Time Left:",process_df.loc[index, "Service T Left"], "Status:", process_df.loc[index, "Status"])
        
        else:  # Case 2: Service time < quantum, meaning it will be completed
            time += row["Service T Left"]
            process_df.loc[index, "Service T Left"] = 0
            process_df.loc[index, "Status"] = "Completed"
            process_df.loc[index, "End T"] = time
            process_df.loc[index, "Turn Around T"] = row["End T"]- row["Arrival T"]
            process_df.loc[index, "Total Wait"] = row["Turn Around T"] - row["Service T"]
            service_queue.pop(0)  # Remove process from the queue
            print("Time:", time,"Servicing Proces ID number:", row["Process ID"],"Time Left:", process_df.loc[index, "Service T Left"], "Status:", process_df.loc[index, "Status"])
            


# Main simulation loop
while not process_df["Status"].eq("Completed").all():
    update_ready_queue()
    if ready_queue:
        service_queue.append(ready_queue.pop(0))  # Move process from ready to service queue
    if service_queue:
        service_service_queue()
    else:
        # If no processes are in the service queue, increment time to the next arrival
        next_arrival_time = process_df.loc[process_df["Status"] == "Has not arrived", "Arrival T"].min()
        if not pd.isnull(next_arrival_time) and next_arrival_time > time:
            time = next_arrival_time
process_df