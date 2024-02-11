# Weighted Fair Queuing Algorithm

## Overview
Weighted Fair Queuing (WFQ) is a packet scheduling algorithm used in computer networking to achieve fairness and improve Quality of Service (QoS) in the transmission of data packets. WFQ ensures that each flow gets a fair share of the network resources while allowing for differentiated services based on assigned weights.

## Key Concepts
- **Fairness**: WFQ ensures that every flow, regardless of its weight or packet size, receives an equitable share of network resources over time.
- **Weighted Scheduling**: The algorithm prioritizes packets based on predefined weights assigned to different flows or packet streams.
- **Virtual Time**: WFQ uses the concept of virtual time to schedule packets, granting priority to flows with a higher ratio of data to weight.

## How It Works
1. **Packet Arrival**: As packets arrive, WFQ establishes a virtual finish time based on the current time and the weight of the flow.
2. **Queueing**: Packets are placed into separate queues for each flow and are scheduled for transmission based on their virtual finish times.
3. **Scheduling**: The scheduler selects the packet with the earliest virtual finish time for transmission, ensuring fairness and prioritization based on the assigned weights.

## How to run code 
### **Configurations**

- **router_port** : its a port router use to listen the sources
- **destination_port** : its a port destination use to listen the routers
- **source_amount** : amount of sources
- **destination_port** : its a port destination to used to listen the routers
- **csv_address** : the csv files contain data want to send to the destination
- **result_address** : the address of result.csv to see the order of packets them received to the destination

#### below you can see the example of config.ini file in root directory of project :
```ini
[CONFIGS]
router_port=9006
destination_port=9004
source_amount=3
router_amount=1
csv_address=/home/y/Desktop/iust/AdvanceNetwork/WeightedFairQueueing/client/
result_address=/home/y/Desktop/iust/AdvanceNetwork/WeightedFairQueueing/destination/
```
### **Starter Data**
You have to provide data to client in a structure like below csv file in the csv_address directory that you provide later

- **csv files :**  this is the structure of named csv file ```data_<name>_<weight>.csv``` the name can be any thing but weight must be an integer number that is the sign of weight of data send to destination from a client each csv file is a represent of a client that want to send contained data to destination

- **data in csv files :**  below example of data in a csv files contian **packet** which is name of the packet and **data** is the data a packet contained and **start_time** is the time that a packet send to router
    ```csv
    packet, data, send_time
    B, sdjglr, 5
    D, kdjgniegl, 8
    H, gjlrogdi, 20
    ```

### **Run code**
#### Manual
  - **step one :** after set your config.ini file first you have to run destiantion.py file in the destiantion module
  - **step two :** in this step you have to run router.py file in the router module
  - **step two :** in final step you have to run client.py file in the client module to start the flow
#### Automate
  - **in windows :** after make sure you have install python on your windows os just run runner.bat in cmd like ```.\runner.bat``` or open gitbash and make sure python3 is install on it then run ```bash runner.sh```
  - **in ubuntu :** after make sure python3 is install on your local ubuntu just run ```bash runner.sh```

### **Result**
- You can see the result in a csv file that you set the directory address of it in the **config.ini** file later in a file named ```result.csv``` and you can see the example of output down below .
  ```csv
  data receive in destination => packet : A data length : 8 , data : adhvngld weight : 1 at 1707651170.1469297
  data receive in destination => packet : C data length : 10 , data : djflotbbhg weight : 2 at 1707651172.1142294
  data receive in destination => packet : B data length : 6 , data : sdjglr weight : 1 at 1707651173.1036284
  data receive in destination => packet : E data length : 8 , data : kfogjelg weight : 2 at 1707651176.1178179
  data receive in destination => packet : F data length : 6 , data : kdjbit weight : 1 at 1707651178.1129177
  data receive in destination => packet : G data length : 10 , data : kfldhgirfr weight : 2 at 1707651181.13731
  data receive in destination => packet : D data length : 9 , data : kdjgniegl weight : 1 at 1707651182.1453245
  data receive in destination => packet : H data length : 8 , data : gjlrogdi weight : 1 at 1707651190.191596
  
  ```
## Advantages
- **Fairness**: All flows receive an equitable share of network capacity, preventing certain flows from monopolizing resources.
- **Quality of Service**: WFQ can provide improved QoS for delay-sensitive or high-priority traffic by using weighted scheduling.
- **Differentiated Services**: The algorithm allows for varying levels of service based on assigned weights, making it suitable for diverse traffic types.

## Example
Consider a network with three flows having weights 1, 2, and 3, respectively. In a WFQ system, the flow with weight 3 will receive twice the bandwidth as the flow with weight 1 and thrice the bandwidth of the flow with weight 2.

## Implementation
- WFQ is commonly implemented in network devices such as routers and switches as part of their Quality of Service (QoS) mechanisms.
- Various networking libraries and protocols, such as DiffServ and MPLS, may incorporate WFQ to achieve differentiated service levels.

## Further Reading
- [Cisco - Understanding and Configuring WFQ](https://www.cisco.com/c/en/us/support/docs/ip/quality-of-service-qos/5277-wfq.html)
- [IETF RFC 3664 - The Weighted Fair Queueing Management Information Base](https://tools.ietf.org/html/rfc3664)

## Contributing
Contributions and feedback on the WFQ algorithm and its applications in computer networking are welcome. 

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).