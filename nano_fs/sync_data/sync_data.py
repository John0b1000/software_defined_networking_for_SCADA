# @file: sync_data.py
#
# @brief: Pulls data from file server periodically.
#
# @references
#    https://stackoverflow.com/questions/5284147/validating-ipv4-addresses-with-regexp
#    https://www.geeksforgeeks.org/how-to-add-colour-to-text-python/
#

# imports
import os
import sys
from re import match
from time import sleep

def fetch_data(file_addr):
  """ Pull data from server using wget command.
  @param fnum (numeric)    number of current file
  @param data    (list)    data strings
  
  @return None
  """
  
  # download the file
  os.system(f"wget -P data/ {file_addr} >> sync_history.log 2>&1")

  
def process_new_data(filename):
    """ Process new data and save values for reference.
    @param filename (string)    name of new file
    
    @return (list)    new data
    """
    # read the new file
    with open(filename, "r") as f:
    
      # read all lines
      lines = [line.rstrip() for line in f]
      
      # process each line
      data = []
      for line in lines[2:len(lines)-1]:
        pair = line.split(":")
        data.append(pair)
        
      # return the new data
      return data
        
def display_new_data(old, new):
    """ Display new data to the terminal.
    @param old (list)    old data vector
    @param new (list)    new data vector
    
    @ return None
    """
    
    # compare new data with old data to see
    # what values have changed
    for i, pair in enumerate(new):
      if pair[1] != old[i][1]:
        data_str = "\33[{code}m".format(code=35) + pair[1]
        change_str = "\33[{code}m".format(code=36) + f"({str(int(pair[1]) - int(old[i][1]))})"
        iden_str = "\33[{code}m".format(code=39) + pair[0] 
        print(f"{iden_str.ljust(50)} ={data_str.rjust(15)} {change_str.rjust(25)}")
      else:
        data_str = "\33[{code}m".format(code=32) + pair[1]
        iden_str = "\33[{code}m".format(code=39) + pair[0] 
        print(f"{iden_str.ljust(50)} ={data_str.rjust(15)}")
    print("\33[{code}m".format(code=39) + "\n" + ("=" * 80))

def main(argv):
  """ Main Program """
  
  # create a file list
  files = [f"data/file{i}.txt" for i in range(0, 10)]

  # error/usage message
  err_no_server = "[ERROR] Not enough server params specified."
  err_inv_ip = "[ERROR] Invalid IP address field:"
  err_inv_port = "[ERROR] Invalid port field:"
  usage = "usage: python3 sync_data.py IP_ADDR PORT"

  # parse the command line argument
  if len(argv) != 3:
    print(err_no_server)
    print(usage)
    return 1
  else:
    ip_addr = argv[1]
    if not match(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", argv[1]):
      print(err_inv_ip, ip_addr)
      print(usage)
      return 1
    try:
      port = int(argv[2])
    except ValueError:
      print(err_inv_port, argv[2])
      print(usage)
      return 1
      
  # wait before grabbing first file
  sleep(5)
    
  try:
  
    while (True):
      
      for file in files:
      
        # init data vectors
        old = []
        new = []
        
        # read and remove current copy of the file
        if os.path.isfile(file):
          with open(file, "r") as f:
            lines = [line.rstrip() for line in f]
            for line in lines[2:len(lines)-1]:
              pair = line.split(":")
              old.append(pair)
          os.system(f"rm {file}")
          
        # sync data from the server
        fetch_data(f"{ip_addr}:{port}/{file}")
        
        # process new data
        new = process_new_data(file)
        
        # display the new data
        if len(old) != 0 and len(new) != 0:
          print("=" * 80)
          print(f"[UPDATE]: {file}\n")
          display_new_data(old, new)
          old = new
        
        # fetch every 20 seconds
        sleep(20)
      
  except KeyboardInterrupt:
  
    # exit gracefully
    return 0


if __name__ == "__main__":
  main(sys.argv)
  