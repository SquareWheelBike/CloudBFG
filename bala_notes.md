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

- we need to better explain why we need a NN, becase current techniques take a long time. the way we explain it now indicates we are just improving on what we currently can do, but we need to be doing something that is not possible with current techniques
- specifically justify that NN can estimate on noisy data
- we can throw temperature modelling into the mix, because R0 and the related values are temperature dependent
- trying to estimate values using a NN is a losing game, he thinks we should just directly pass it values and get a prediction
- the cloud based approach has some advantages, we can develop it anyways, but bala's
- instead of estimating k-parameters, we can assume we have them already and use the measured voltage to estimate SOC
- we need to be more clear about what our approach will be, since we are just talking about the initial starting point in the slides right now
- collaborate with the other students to get data and ideas, since throwing data at a neural network is not what they have been doing
- we will also be stacking temperature data onto the NN, so we need to be clear about that
- we need a more clearly defined use case
- bala has a pitch that we can buy 10 different batteries with different characteristics, we will characterize all of them with bala's approach, and then 
