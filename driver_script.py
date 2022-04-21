import matplotlib.pyplot as plt
import numpy as np

# 1) načíst csv
# 2) vytvořit pole, kde bude počet paketů za 5 minut
# 3) 3 sigma rule na tomhle poli packets_in_epoch
# 4) načtení testovacího setu to_m a from_m stejnym způsobem a zjištění False positives atd.
# 5) vykreslení výsledků (i těch dropnutých)
# *6) DDOS simulace


def load_array(data):
    time = 0 # time accumulator
    count = 0 # # of packets accumulator
    packets_in_epoch = []  # how many packets are in 5 minute window
    epochs = []  # holds how many 5 minute windows there are in the dataset
    epoch = 0  # epoch = 5 minute window
    for pkt_t in data:
        time += pkt_t[0]  # time accumulation
        count += 1  # akumulace počtu paketů za 5 minut
        if(time >= 300):
            time = 0
            epoch += 1
            packets_in_epoch.append(count)
            # TODO je tohle potřeba? můžu to brát jako index...
            epochs.append(epoch)
            count = 0
            # přiřazení do pole
    # TODO udělat to pro poslední epochu
    return packets_in_epoch, epochs




# 1) Loading the CSV file

file = open('csv/packets_to_m_train.csv', 'rb')
data = np.loadtxt(file, delimiter=",", skiprows=1)
file.close()
print(data)

# 2) Vytvoření pole, kde bude počet paketů za 5 minut, epochs[i]*5 určuje čas v minutách
packets_in_epoch, epochs = load_array(data)
print(packets_in_epoch)
print(len(packets_in_epoch) == len(epochs))


time_windows_secs = [epoch*300 for epoch in epochs]  # epochy v sekundách
time_windows_min = [epoch*300/60 for epoch in epochs]  # epochy v minutách

#print(time_windows_secs)
#print(len(time_windows_secs) == len(packets_in_epoch))
#print(sum(packets_in_epoch))

# 3) 3 sigma rule on packets_in_epoch

mean = np.mean(packets_in_epoch) # mean and standard deviation of the dataset (# of packets in 5 minute windows)
sigma = np.std(packets_in_epoch) 

lower_bound = mean - 3*sigma
upper_bound = mean + 3*sigma

# some lambda magic
f = lambda x: x < lower_bound or x > upper_bound
anomalies = np.array([f(xi) for xi in packets_in_epoch]) # getting the anomalous packets
num_of_anomalies = len(anomalies)

# 5) Plotting the results
plt.style.use('_mpl-gallery')
fig, ax = plt.subplots(figsize=(12, 8), dpi=150, layout='constrained')
ax.plot(time_windows_min,packets_in_epoch)  # Plot some data on the axes.
ax.set_ylim((0,200))
ax.set_xlabel('Čas [min]') 
ax.set_ylabel('Počet paketů')
ax.set_title("Počet paketů v čase (trénovací množina[TO_MASTER]")  
ax.legend();  # Add a legend.

plt.savefig("FIG2.png")
