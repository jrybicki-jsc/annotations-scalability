# annotations-scalability
Testing scalability of neo and mongo by storing annotations

This repository is for documenting experiments assessing suitability (in terms of scalability and performance) of different backends (mongo and neo4j) for storing semantic annotations. We emulate EUDAT B2NOTE service and store annotations in a format close to W3C semantic annotations format. Each annotation is a pair of of target and body. Target can be a data object stored and body can be a concept (or a metadata keyword). 

All experiments and data evaluations are conducted with docker and docker-compose. By that we strive to achieve   
transparency, repeatability, and reproducibility of the results. 

## Run an experiment
```docker-compose build```

```
docker-compose run --name experiment1 tester sh -c ' sleep 20 && /app/test.py mongo 10 1000 && /app/test.py neo 10 1000'
```

The testing application takes three parameters:
* backend (mongo, neo, dummy)
* number of runs
* number of repetitions in each run (e.g. retrieval requests)

The output of the experiments is displayed and stored in volume */results/* (in csv format)

### Evaluating results
Also the processing and evaluation of the results can be done with docker. Start with preparing the image:

```
cd processor
docker build . -t processor
```

Data processing is started with:

```
docker run --rm --volumes-from experiment1 processor
```

### Visualizing results
Similarly the visualization of the results can be done with docker. Prepare the image:

```
cd visualizer
docker build . -t visualizer
```

Start the visualization process:

```
docker run --rm --volumes-from experiment1 visualiser
```

This container takes input in csv format from */results/* and store png plots (generated with gnuplot) in */results/*. 

If you want to extract the data from docker volumes and store it on your disk (in */tmp/output/* directory), use following command:

```
docker run --rm --volumes-from experiment1 -v /tmp/output/:/output/ busybox sh -c 'cp /results/* /output/'
