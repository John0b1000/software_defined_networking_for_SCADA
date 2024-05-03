# @file: entropy.py
#
# @brief: Computes the entropy of incoming network traffic.
#

# imports
import sys
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scapy.all import *
from random import randint

def analyze(pkt): 
    """ Analyze received packet. """

    if IP in pkt:
        ip_src=pkt[IP].src
        ip_dst=pkt[IP].dst
    # if TCP in pkt:
    #     tcp_sport=pkt[TCP].sport
    #     src_prts.append(tcp_sport)
    #     tcp_dport=pkt[TCP].dport

       # print(" IP src " + str(ip_src) + " TCP sport " + str(tcp_sport))
       # print(" IP dst " + str(ip_dst) + " TCP dport " + str(tcp_dport))

    # you can filter with something like that
    # if ( ( pkt[IP].src == "192.168.0.1") or ( pkt[IP].dst == "192.168.0.1") ):
    #     print("!")

# This function is called periodically from FuncAnimation
def animate(i, xs, ys, ax):

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(randint(0,1000))

    # Limit x and y lists to 20 items
    # xs = xs[-20:]
    # ys = ys[-20:]
    xs = xs
    ys = ys

    # Draw x and y lists
    ax.clear()
    plt.cla()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('TMP102 Temperature over Time')
    plt.ylabel('Temperature (deg C)')

def main(argv):
    """ Main Program """ 

    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []

    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, ax), interval=1000)

    while(True):
        pkts = sniff(filter="ip", timeout=5, prn=analyze)
        pkts.nsummary()
        ss = len(pkts)
        print(ss)

        src_ips = {}
        for pkt in pkts:
            if IP in pkt:
                if pkt[IP].dst in src_ips:
                    src_ips[pkt[IP].dst] = src_ips[pkt[IP].dst] + 1
                else:
                    src_ips[pkt[IP].dst] = 1

        print(src_ips)
        plt.draw()
        # Pause for a short duration to allow visualization
        plt.pause(0.5)
        # or it possible to filter with filter parameter...!
        #sniff(filter="ip and host 192.168.0.1",prn=print_summary)
        #print(src_ips)
        #print(src_prts)
        # Set up plot to call animate() function periodically


if __name__ == "__main__":
    # Enable interactive mode for non-blocking plotting
    plt.ion()

    # Display the plot window in non-blocking mode
    plt.show(block=False)

    main(sys.argv)
