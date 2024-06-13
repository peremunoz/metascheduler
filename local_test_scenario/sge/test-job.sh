#!/bin/bash
# Example SGE job script to stay in the queue

# Specify the name of the job
#$ -N SleepJob

# Specify the amount of time to sleep
SLEEP_DURATION=3600  # Sleep for 1 hour

# Run the sleep command
sleep $SLEEP_DURATION
