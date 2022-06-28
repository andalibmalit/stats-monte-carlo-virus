import time
start_time = time.time()
from monte_12 import Init_Computer_Dict, Single_Day

# DESCRIPTION:
#   This program runs the single day simulation from textbook problem 5.10 N times.
#   Each iteration starts with a fresh list of computers with a random one infected as patient zero.
#   A running count of the number of days it takes to clean all computers, the number of times
#       every computer was infected at least once, and the total infected before the single day
#       simulation ends is kept in 'days', 'maximum_infected' and 'total_infected' respectively.
#   Each of these variables is averaged based on N iterations for our final estimations.
#   Functions for initializing the computer list and for the single day simulation are in "monte_12.py".

# NOTE: To simulate a probability of 0.1 +/- 0.001, our 90%, 95% and 99% confidence intervals require
#   676507, 955507 and 1657657 simulations respectively.
N = 1657657
days = 0
max_days = 0
maximum_infected = 0
total_infected = 0

i = 0
while i < N:
  Computer_Dict = Init_Computer_Dict()
  infected_count = 1
  net_infected = 0
  
  # Run single day simulation
  print("Running simulation " + str(i) + "...")
  temp_days = 0 
  while (infected_count > 0):
    Computer_Dict, infected_count = Single_Day(Computer_Dict, infected_count)
    temp_days += 1
    days += 1
  print("Simulation completed in " + str(temp_days) + " days.")
  if temp_days > max_days:
    max_days = days
  
  # Get total computers infected in this simulation  
  for status in Computer_Dict.values():
      if status[1] == 1:
          net_infected += 1
  
  # Increment maximum_infected if all 20 computers were infected at some point        
  if net_infected == 20:
    maximum_infected += 1
  
  # Add number of computers that were infected to total_infected  
  total_infected += net_infected
  
  # Increment i, move to next simulation
  i += 1

# Print averages
avg_days = days/N
avg_max_infected = maximum_infected/N
avg_infected = total_infected/N

print("\n" + str(N) + " simulations completed in " + str(time.time() - start_time) + " seconds, averages below:")
print("1) Expected time to remove virus, in days (longest single simulation took " + str(max_days) + " days): " + str(avg_days))
print("2) Probability of each computer getting infected at least once: " + str(avg_max_infected))
print("3) Expected number of computers to get infected: " + str((avg_infected)))

# RESULTS 4/23/22
#   1657657 simulations completed in 49010.8559615612 seconds, averages below:
#   1) Expected time to remove virus, in days (longest single simulation took 1602915 days): 131.1413657952158
#   2) Probability of each computer getting infected at least once: 0.0011039678292915844
#   3) Expected number of computers to get infected: 2.9772009529112475