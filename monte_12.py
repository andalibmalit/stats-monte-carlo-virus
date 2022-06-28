import random
random.seed(None)
from numpy.random import default_rng
rng = default_rng(None)
rng.random()

def Init_Computer_Dict():
    # For each computer, the first element of the value (status array) is 1 if the computer is currently infected.
    #   The second value element is 1 if the computer has ever been infected.
    Computer_Dict = {computer:[0, 0] for computer in range(20)}
    # Infect patient zero
    patient_zero = random.sample(list(Computer_Dict.keys()), 1)
    Computer_Dict[patient_zero[0]] = [1, 1]
    return Computer_Dict

def Single_Day(Computer_Dict, infected_count):
    oldInfected = infected_count
    print("\tStarting single day loop...")
    print("\t\tPerforming Bernoulli trials with " + str(infected_count) + " infected computers out of 20...")
    spreadVirusBernoulli(Computer_Dict)
    infected_count = updateInfected(Computer_Dict)
    
    print("\t\t" + str(infected_count - oldInfected) + " new computers infected!")  
    
    print("\t\tCleaning computers...")        
    cleanComputers(Computer_Dict, infected_count)
    infected_count = updateInfected(Computer_Dict) 
    
    if infected_count == 0:
        print("\tSimulation complete! All computers clean.")
    else:
        print("\t" + str(infected_count) + " infected computers remain, restarting loop...")
    
    return Computer_Dict, infected_count

# For each infected computer, run Bernoulli trial to infect every uninfected computer
def spreadVirusBernoulli(Computer_Dict):
    infectable = list()
    for status1 in Computer_Dict.values():
        if status1[0] == 1:
            # For each infected computer, add the key of every uninfected computer to `infectable`.
            for computer, status2 in Computer_Dict.items():
                if status2[0] == 0:
                        infectable.append(computer)
    # For each key in `infectable`, run a Bernoulli trial to determine if it gets infected.
    #   Note that the same victim can be infected multiple times by different computers,
    #   but that only counts as one net infection.
    for computer in infectable:
        if rng.binomial(1, 0.1) == 1:
            Computer_Dict[computer] = [1, 1]

# Attempt to minimize time complexity by reducing size of outer loop to only those computers actually
#   spreading the virus.        
def spreadVirusBinomial(Computer_Dict):
    spreaders = 0
    infectable = list()
    for computer, status in Computer_Dict.items():
        if status[0] == 1:
            spreaders += 1
        else:
            infectable.append(computer)
    # For each infected computer, sample a binomial distribution of uninfected computers with probability
    #   of infection 0.1.
    for i in range(spreaders):
        num_to_infect = rng.binomial(len(infectable), 0.1)
        for computer in random.sample(infectable, num_to_infect):
            Computer_Dict[computer] = [1, 1]

def updateInfected(Computer_Dict):
    infected_count = 0
    for status in Computer_Dict.values():
        if status[0] == 1:
            infected_count += 1
    return infected_count
            
def cleanComputers(Computer_Dict, infected_count):
    # Clean all infected computers if infected_count <= 5
    if infected_count <= 5:
        for status in Computer_Dict.values():
            if status[0] == 1:
                status[0] = 0
    # Clean 5 randomly selected infected computers if infected_count > 5
    if infected_count >5:
        infected_list = list()
        for computer, status in Computer_Dict.items():
            if status[0] == 1:
                infected_list.append(computer)
        for computer in random.sample(infected_list, 5):
            Computer_Dict[computer] = [0, 1]