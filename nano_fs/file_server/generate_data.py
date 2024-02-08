# @file: generate_data.py
#
# @brief: Generates text files with random data every few seconds.
#

# imports
from datetime import datetime
import os
from random import randint
import sys
from time import sleep

def generate_data():
  """ Generate random data strings.
  
  @return    list of data strings
  """
  data = []
  data.append("Energy Consumption (kWh): " + str(randint(10, 100000)) + "\n")
  data.append("Average Power Consumption (W): " + str(randint(10, 100000)) + "\n")
  data.append("Peak Power Consumption (last hour) (W): " + str(randint(10, 10000000)) + "\n")
  data.append("Average Speed (mph): " + str(randint(10, 200)) + "\n")
  data.append("Average Temperature (deg F): " + str(randint(10, 120)) + "\n")
  
  # return the list
  return data
  
def write_data_to_files(fnum, data):
    """ Write data strings to files.
    
    @param fnum (numeric)    number of current file
    @param data    (list)    data strings
  
    @return    None
    """
    
    # place files in a data directory located in the current working directory
    filename = "data/file" + str(fnum) + ".txt"
    if os.path.isfile(filename):
      os.system(f"rm {filename}") # remove any previous data files
      
    # write to the file
    with open(filename, "w") as f:
      time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      f.write(f"========== SENSOR READINGS ({time}) ==========\n\n") # file title
      for data_string in data:
        f.write(data_string) # write data
      f.write("\n") # new line to end file
    

def main(argv):
  """ Main Program """

  # define the maximum number of files to be generated
  max_files = 10
  
  try:
  
    while (True):
    
      for i in range(0, max_files):
      
        # generate and write random data
        write_data_to_files(i, generate_data());
        
        # wait for next write
        sleep(randint(1, 10))
      
  except KeyboardInterrupt:
  
    # exit gracefully
    return 0


if __name__ == "__main__":
  main(sys.argv)
  