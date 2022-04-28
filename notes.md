# Cloud BFG dev notes

![brainstorm session Apr 28, 2022](img/brainstorm.png)

## Client

- The ESP will have a buffer of entries to keep track of, so that socket connections are not so common.
- Each recorded reading will also be buffered, so as to remove spikes and noise from readings
- The ESP only needs to keep track of SOC characterization coefficients; these can be loaded from EEPROM and used for SOC instantaneously, independent from the server
- The ESP will connect to the 'Broker', 

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

- Are we doing cell-based, or for a whole pack? It might be smart to do both?
- We will need to discuss which BMS we are going to use for testing, since BMS's with serial might be expensive
  - ie are we designing our own BMS or using a third party BMS?
  - We could use MaxKGO for sensing, since this algorithm will be working with different companies' BMS's
  - Alternatively, we can make our own BMS
- If we use something like MaxKGO, since it is open source, we can (fairly easily) add our API to it, so that its SoC estimation can connect to our SoC estimation. 
  - Lovelesh recommends this, since from his experience, providing a demo where we can show that our algorithm can be implemented into an existing platform is a product we can 'sell' to the community.
  - Take existing hardware, and show that we can improve it.
  - When we showcase this technology, if we use proprietary hardware, the initial reaction might be that we need special or extra hardware to implement our algorithm, which is not true
  - If we can show a useable product, and **open-source** the product, then the product will grow very quickly, and we can become a sales platform, rather than a platform for the service
