#!/bin/bash

# This is the test script used to verify the functionality of the system.
# The script will schedule jobs with different sizes and configurations to the system.

# To setup the system for testing, run the following commands:
# 1. Start the hadoop and sge cluster with docker-compose
# 2. Inside the sge container, give access to schedule jobs to the main queue the user "metascheduler", with the command:
#    export SGE_ROOT=/opt/sge/ && /opt/sge/bin/lx-amd64/qconf -au metascheduler arusers
# 3. Inside the sge container, in /home/metascheduler, compile the test jobs with the command:
#    sudo -u metascheduler sh -c 'gcc -o /home/metascheduler/test_job /home/metascheduler/test_job.c'
# 4. Inside the hadoop container, give full access to user "metascheduler" and start the sshd service with the command:
#    hdfs dfs -setfacl -m user:metascheduler:rwx / && /opt/hadoop/bin/hdfs dfs -chown -R metascheduler:metascheduler / && /opt/hadoop/bin/hdfs dfs -chmod -R 755 / && (echo "metascheduler ALL=(ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers.d/metascheduler) && sudo systemctl start sshd
# 5. Inside the hadoop container, copy the test files to the hdfs with the command:
#    sudo -u metascheduler sh -c 'export JAVA_HOME=/usr/lib/jvm/jre/ && /opt/hadoop/bin/hdfs dfs -put /home/metascheduler/1000000.txt /1000000.txt && /opt/hadoop/bin/hdfs dfs -put /home/metascheduler/5000000.txt /5000000.txt && /opt/hadoop/bin/hdfs dfs -put /home/metascheduler/10000000.txt /10000000.txt && /opt/hadoop/bin/hdfs dfs -put /home/metascheduler/15000000.txt /15000000.txt'
# 6. Run the API server and the test script.

cd ../client

pipenv run sh -c 'export PYTHONPATH=.. && python3 main.py send job --name "n100000000" --path "test_job100000000.sh" --queue 2'

sleep 1

pipenv run sh -c 'export PYTHONPATH=.. && python3 main.py send job --name "n1000000000" --path "test_job1000000000.sh" --queue 2'

sleep 1

pipenv run sh -c 'export PYTHONPATH=.. && python3 main.py send job --name "n10000000000" --path "test_job10000000000.sh" --queue 2'

sleep 1

pipenv run sh -c 'export PYTHONPATH=.. && python3 main.py send job --name "n100000000000" --path "test_job100000000000.sh" --queue 2'

sleep 1

pipenv run sh -c 'export PYTHONPATH=.. && python3 main.py send job --name "" --path "/opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar" --queue 1 --options "wordcount /1000000.txt /out1"'

sleep 1

pipenv run sh -c 'export PYTHONPATH=.. && python3 main.py send job --name "" --path "/opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar" --queue 1 --options "wordcount /5000000.txt /out2"'

sleep 1

pipenv run sh -c 'export PYTHONPATH=.. && python3 main.py send job --name "" --path "/opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar" --queue 1 --options "wordcount /10000000.txt /out3"'

sleep 1

pipenv run sh -c 'export PYTHONPATH=.. && python3 main.py send job --name "" --path "/opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar" --queue 1 --options "wordcount /15000000.txt /out4"'
