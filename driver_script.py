import matplotlib.pyplot as plt
import numpy as np

# This script does 6 tasks:
#   1) Loads dataset from csv
#   2) Creates list with number of packets in 5 minute windows
#   3) Trains 3 sigma rule "classificator" on this list
#   4) Load testing set direction: to_master a from_master and checks if it's classified correctly
#   *5) DDOS simulation
#   6) Plotting of the results


def load_array(data):
    time = 0  # time accumulator
    count = 0  # of packets accumulator
    packets_in_epoch = []  # how many packets are in 5 minute window
    epochs = []  # holds how many 5 minute windows there are in the dataset
    epoch = 0  # epoch = 5 minute window
    for pkt_t in data:
        time += pkt_t[0]  # time accumulation
        count += 1  # accumulation of the # of packets in 5 minute window
        if(time >= 300):
            time = 0
            epoch += 1
            packets_in_epoch.append(count)
            epochs.append(epoch)
            count = 0

    # TODO do it for the last epoch
    return packets_in_epoch, epochs


# Detecting anomalies with some lambda magic

def detect_anomaly(array, lower_bound, upper_bound):
    def f(x): return x < lower_bound or x > upper_bound
    anomalies = np.array([xi for xi in array if f(xi) == True])
    return anomalies


# 1) Loading the CSV file
train_file = 'csv/packets_from_m_train.csv'
test_file = 'csv/packets_from_m_test.csv'
anomalous_file = 'csv/packets_from_m_test_DDOS.csv'

file = open(train_file, 'rb')
training_data = np.loadtxt(file, delimiter=",", skiprows=1)
file.close()

# 2) List with # of packets in 5 min window, epochs[i]*5 = time in minutes
packets_in_epoch, epochs = load_array(training_data)
time_windows_min = [epoch*300/60 for epoch in epochs]  # epochs in minutes

# 3) 3 sigma rule on packets_in_epoch

# The mean and standard deviation of the dataset (# of packets in 5 minute windows)
mean = np.mean(packets_in_epoch)
sigma = np.std(packets_in_epoch)

lower_bound = mean - 3*sigma  # 3 sigma rule bounds "The Classificator"
upper_bound = mean + 3*sigma

# 4) Loading testing dataset and counting False Negatives etc.

file = open(test_file, 'rb')
testing_data = np.loadtxt(file, delimiter=",", skiprows=1)
file.close()

test_packets_in_epoch, test_epochs = load_array(testing_data)
test_time_windows_min = [epoch*300/60 for epoch in test_epochs]

# Detect if there are any false negatives in the testing set
anomalies = detect_anomaly(test_packets_in_epoch, lower_bound, upper_bound)
print(anomalies)

# *5) DDOS simulation

file = open(anomalous_file, 'rb')
anomalous_data = np.loadtxt(file, delimiter=",", skiprows=1)
file.close()

anomalous_packets_in_epoch, anomalous_epochs = load_array(anomalous_data)
anomalous_time_windows_min = [epoch*300/60 for epoch in anomalous_epochs]

# Detect anomalies
anomalies = detect_anomaly(
    anomalous_packets_in_epoch, lower_bound, upper_bound)
print(anomalies)

# Drop the anomalous packets / simulate packet filtering
for i, x in enumerate(anomalous_packets_in_epoch):
    if x in anomalies:
        anomalous_packets_in_epoch[i] = 1 # Should be 0, but 1 is more visible on the graphical plot
print(anomalous_packets_in_epoch)

# 6) Plotting the results in Czech

plt.style.use('_mpl-gallery')
fig, ax = plt.subplots(figsize=(12, 8), dpi=150, layout='constrained')
ax.plot(time_windows_min, packets_in_epoch, label="Trénovací množina")
ax.plot(test_time_windows_min, test_packets_in_epoch, label="Testovací množina")
ax.plot(anomalous_time_windows_min, anomalous_packets_in_epoch,
        label="DDOS detekce (množina s nagenerovanými anomáliemi)")
ax.set_ylim((0, 200))
ax.set_xlabel('Čas [min]')
ax.set_ylabel('Počet paketů')
ax.set_title("Počet paketů v čase (směr [FROM_MASTER])")
ax.legend()

plt.savefig("FIG.png")