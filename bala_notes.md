- good start, but we need  more details
- what  are we doing a NN for,  what are  we training on, what is SOC estimations, what are the OCV-SOC models, what are the features of the cloud page, we  can  use one of our lab  templates for the presentation, 

There were more points, I thought he moved  on to something else so I missed it; it will be in the  lab recording

## round 2???

- battery characterization in title first, also maybe shorten the title? (note: we picked a long one because everyone else's is long)
- Move over to the template online
- include some generated data from online open source content
- we need to think about making this in a way that it indicates what our final product will be
- Need diagrams of our web framework // mqtt connections
- we need to explain why we need a neural network and how we are going to train it
- We need a deliverables slide
- include a bunch of details on what is happening on the cloud side

## round 3

- [X] we need to better explain why we need a NN, becase current techniques take a long time. the way we explain it now indicates we are just improving on what we currently can do, but we need to be doing something that is not possible with current techniques
- [X] specifically justify that NN can estimate on noisy data
- [ ] we can throw temperature modelling into the mix, because R0 and the related values are temperature dependent
- [X] trying to estimate values using a NN is a losing game, he thinks we should just directly pass it values and get a prediction
- [ ] the cloud based approach has some advantages, we can develop it anyways, but bala's
- [ ] instead of estimating k-parameters, we can assume we have them already and use the measured voltage to estimate SOC
- [ ] we need to be more clear about what our approach will be, since we are just talking about the initial starting point in the slides right now
- [ ] collaborate with the other students to get data and ideas, since throwing data at a neural network is not what they have been doing
- [ ] we will also be stacking temperature data onto the NN, so we need to be clear about that
- [ ] we need a more clearly defined use case
- [ ] bala has a pitch that we can buy 10 different batteries with different characteristics, we will characterize all of them with bala's approach, and then


## notes on what to present

### CloudBMS

3 mins exactly

- Explain the idea of the project
  - A Battery Fuel Gauge is a device that estimates the state of charge (SOC) of a battery
  - Batteries have something called a BMS on them that balances cells and estimates SOC, but it is not very accurate in a lot of cases
  - We aim to reduce characterization time (60 hours) and improve SOC estimation accuracy by using a cloud-based approach
  - There are a few methods to better estimate SOC, Bala's Combined +3 characterization is one of them, as he presented earlier. We can also look at coulomb counting, but voltage-based methods require characterized batteries that take a lot of time and expense to characterize
  - Using a Neural Network, we hope to create a cache of characterized batteries with varying levels of wear or even varying chemistries, and then gather live data from the battery in the field and choose which one is closest using the NN
  - There will be intermediary values, and there can be error estimation from collected data, so that the BFG can intelligently and iteratively get more accurate estimations.
  - Modern cell phones and laptops do this, but the idea of the cloud approach is it combines an algorithmic way to store the OCV curve, with small inexpensive hardware that can accurately estimate the SOC. Offloading the characterization to the cloud allows for a more accurate SOC estimation, and also allows for a more accurate SOC estimation for batteries that are not characterized.
- The result of this work is an inexpensive addition to existing BMS systems that can bring intelligent voltage-based (or combined) SOC estimation to the masses
- This will also reduce waste of batteries, and possibly allow for recycling of used batteries  

#### notes
- q can it be used on worn batteries?
  - yes, the more data we have, the better the estimation will be

### BFGEval

- BFGEval is a project that compares the performance of different SOC estimation algorithms that are available in commercial BFG systems. These systems are inexpensive, but they are not very accurate. We want to compare the performance of different algorithms to see which one is the best for our purposes.
- Additionally, we hope to use a common voltage/current sensor to collect data on an inexpensive 'BFG', that provides a data source to compare our own algorithm against the existing systems.
- The implementation was using an arduino and Python, where the arduino would collect data from the sensors, and the Python code would collect the data over the serial port, and log it to .csv files for comparison later.
- Components included two BFGs, and a combined voltage/current/power sensor.
- Each datapoint was timestamped, and any and all data that could be read from each component was read and stored.

### HIL testing

- HIL stands for Hardware In the Loop
- This is the same as the project bala presented earlier, but alas, here we are
- We had created a test platform for demonstrating the performance of the predictive temperature algorithm
- This consisted of two major components: the embedded component and the computer component
- The embedded component was an Arduino Pro Micro connected to two temperature sensors (one for the battery and one for the environment), a BFG, a humidity sensor, and a voltage/current sensor.
- We would simulate a high discharge, 6A on a discharger, and the Arduino would collect data from the sensors and send it to the computer component for estimation
- The computer would receive the data over serial from the Arduino using Python, which would write the data to a file. MATLAB would then read the data from the file and perform the estimation, updating a graph live on the screen.
