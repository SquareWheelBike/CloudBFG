# AWS setup notes

## IoT core

- You will need to make sure that packages come in on python2.7 and not python3
  - The startup script calls `python` and `pip`, which may not refer to the same version of python
  - AWS also only works with python releases 2.7 - 3.5

## AWS Lambda IOT Comms

- Lambda will handle small, scaleable functions. This way, we can write queries and response functions that add to the database or do lookups, and respond to the IoT devices.
  - This way, we will not need to worry about making a virtual machine scaleable, amazon will do it for us

## Machine Learning

We have two major routes we could follow when approaching the machine learning model:

### EC2 instance

- An EC2 instance will allow us to write all our own custom code and scheduling, and have a static VM instance that can periodically download database information, perform the analysis, and upload the results.
- The benefit of this model is that we will have much more control and freedom with how we design the model.

### Lambda Function (**we are using this one**)

- We also have the option to create a lambda function that will be called periodically, and will download the database, perform the analysis, and upload the results.
- The benefit to this model is that it is simpler to set up, but it will not have its own static ecosystem in which to run, which could potentially pose problems

**note** we are starting with this one, but if it does not work out, then we will swap to an EC2 instance, since that is what we are both more familiar with
