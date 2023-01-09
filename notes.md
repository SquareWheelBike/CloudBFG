# Cloud BFG dev notes

![brainstorm session Apr 28, 2022](img/brainstorm.png)

## Client

- The ESP will have a buffer of entries to keep track of, so that socket connections are not so common.
- Each recorded reading will also be buffered, so as to remove spikes and noise from readings
- The ESP only needs to keep track of SOC characterization coefficients; these can be loaded from EEPROM and used for SOC instantaneously, independent from the server
- The ESP will connect to the 'Broker'

## Server

- MongoDB can store data points from each device
- Each battery will be given a serial number, serial numbers should correspond to *battery* rather than *device*
- So, in a battery pack undergoing characterization, each individual cell will have a unique serial number within that pack
- This is a **lot** of data, so it should be stored in a database in a way that is easy to query
- The server will need to collect all the data for all of these cells, so we can identify dead batteries inside a pack
  - The problem with this is, we cannot estimate SoC on every single one at runtime on a controller
  - The solution to this is to (probably) have separate 'topics' for cells vs packs, so that the microcontroller only needs to worry about SoC estimation on the *pack*, rather than on every single cell.
- We are also going to need to come up with a naming nomenclature, so that we can easily serialize each data point

## Nomenclature

A minimum set of battery information on an initial device connection could be:

- Make or Model
- Cell size
- Cell chemistry
- Series/parallel (pack only)

We should also have a way to name generic cells, so that BFGs connecting for generic use can also be serialized. This pertains to the units that will be 'predicting' the cell chemistry.

We should also have a way to 'rename' pack names

### Cell Serialization

Each cell or pack should get an integer ID, which will be used to identify the cell or pack. Cell lookups in the database will use *integer keys*. This way, we can store a string along with each integer key, for potential use, but if the end-user needs to update the data from a generic cell, they can just update the integer key.

HOWEVER, we need to limit this so that each 'generic' can only be registered **once**. Else, end users might try to change the cell data for an existing cell when they swap cells, rather than registering a cell.

## Database Schema

- Each microcontroller gets a unique ID, which is a string ID that will allow the broker to make a connection to the microcontroller, with new information. Since each ID from the broker should be unique to the controller inherently, we can use this as a primary key. Each device will contain a set of cells, or packs containing cells.
  - This relationship will allow us to associate each cell and each pack with an endpoint ID for comminicating back to the controller.

### Tables

There will be one master database, stored in MongoDB, which will contain all of the data. The tables will define relationships between the data.

| Table Name | Description | Columns | Primary Key |
| ---------- | ----------- | ------- | ------------ |
| `devices` | Devices that have been registered with the broker | `device_id`:str, `SOC_curve`:tuple(float) | `device_id` |
| `cells` | Cells registered | `cell_id`:int, `SOC_curve`:tuple(float), `manufacturer`:str, `model`:str, `chemistry`:str, `size`:str, `device_id`:str | `cell_id` |
| `history` | History of readings for each cell | `cell_id`:int, `timestamp`:datetime, `soc`:float, `voltage`:float, `current`:float, `temp_int`:float, `temp_amb`:float | `cell_id`, `timestamp` |
| `SoC_char_history` | History of cell healths | `cell_id`:int, `timestamp`:datetime, `soc_char`:tuple(float) | `cell_id`, `timestamp` |

#### Relationships

- each cell is associated with a device
- each hisorical point is associated with a cell
- each SoC characterization point is associated with a cell

- may or may not store AI cache for later
- reevaluation of SoC curve should be cycle-based, rather than time-based (or maybe a combination)

## Microcontroller Hardware

- Each controller can be an embedded ESP32, connected to an INA260 for voltage/current readings, and a MAX31855 for ambient and cell temperature readings

## For next meeting

### Status of Project

- Last meeting, we determined that we are going to start by using our own custom data collection system, rather than using an existing BMS.
- We have set up an email account and registered it with Amazon AWS
  - Set up with Lambda, DynamoDB, and IoT Core
  - IoT core is the broker mechanism; we got it responding to my server, so it is working

### Questions

- We need a credit card of some kind registered to the account, right now Cole's card is registered, but this cannot be permanent.
- There is a Pi Zero 2 W in the lab, we have taken it for now for testing purposes, but we should check with Bala to make sure it is okay to use.
- I need the battery simulation code that he made, so that I can simulate stuff for testing.
- Ask about records off of Arbin that we can use to construct a training database for the neural network.

### Model 3 estimation parameters

Ranges for generating more reali

- R0: 10 - 500 m Ohm
- R1: 100 - 200 m Ohm
- R2: 100 - 200 m Ohm
- C1: 5 - 500 F
- C2: 5 - 500 F

## Machine Learning

### General Approach

One approach you could take is to first represent each curve in your cache as a set of ordered points in the Cartesian plane. You could then represent your input curve in the same way. You could then use a machine learning model, such as a neural network, to predict the ordered set of points that represents the curve in the cache that is most similar to the input curve.

To train the model, you would need to define a loss function that measures the difference between the predicted curve and the input curve. This loss function could be based on the Euclidean distance between the corresponding points on the two curves, possibly with some weights applied to give more or less importance to certain points.

For example, you could define the loss function as the sum of the squared Euclidean distances between each pair of corresponding points, divided by the number of points in the curve. This would give you an average distance between the two curves.

You could also consider using a loss function that takes into account the partial nature of the curves, for example by weighting points that are closer to the start or end of the curve more heavily, since these points may be more indicative of the overall shape of the curve.

Once you have defined your loss function and trained your model, you can use it to predict the curve in the cache that is most similar to the input curve by minimizing the loss function.
