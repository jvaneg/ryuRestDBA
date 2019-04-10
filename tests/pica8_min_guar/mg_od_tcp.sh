
#!/bin/sh

# Minimum Guarantee, TCP, One Dominates

# TEST SETUP
# H1 min: 100 Mbps
# H1 demand: 200 Mbps
# H2 min: 200 Mbps
# H2 demand: 600 Mbps
# Link capacity: 600Mbps
# Host1, Host2 -> Host3
# TCP

# requires sshpass to be installed on the machine running the script
# assumes ryurest is currently running on the switch

# Demands (Mbps)
H1_DEMAND=600
H2_DEMAND=200

# output file's name
FILE_NAME=mg_od_tcp
RYURESTDBA_INSTALL=/home/host4/dbaController/ryuRestDBA/
CTRL_SETUP_FILE=./pica8_min_guar/pica8_min_guar_setup.toml
LOCAL_RESULTS_FOLDER=./results/pica8_min_guar/od/tcp/
UDP_TOGGLE=""

# Internal network host IPs
H1_IP=192.168.2.1
H2_IP=192.168.2.2
H3_IP=192.168.2.3

H1_PORT=6001
H2_PORT=6002
H3_PORT=6003

H1_PASS=host1
H2_PASS=host2
H3_PASS=host3
CTRL_PASS=host4

# starts and shuts down the controller (assumes ryurest is already running)
CTRL_SETUP="source /etc/profile;\
cd ${RYURESTDBA_INSTALL};\
pipenv run python ./controller.py ${CTRL_SETUP_FILE} -l ./${FILE_NAME}.csv >/dev/null 2>&1 &"
CTRL_TEARDOWN="killall -2 python; sleep 3; killall python;"
CTRL_CLEANUP="rm ${RYURESTDBA_INSTALL}${FILE_NAME}.csv"

# starts the iperf listen server on host3
# does some weird dev/null stuff to redirect stdin/out so that ssh doesn't hang
H3_SETUP="nohup iperf -s ${UDP_TOGGLE} -p 5503 >nohup.out 2>&1 &"

# terminates the iperf listen server, renames the log file
H3_TEARDOWN="killall -2 iperf; mv ./nohup.out ./${FILE_NAME}_results.log"
H3_CLEANUP="rm ${FILE_NAME}_results.log"

# starts the iperf clients on Host 1 and Host 2, TCP, lasts for 30 seconds
H1_START="nohup iperf -c ${H3_IP} ${UDP_TOGGLE} -b ${H1_DEMAND}M -t 30 -p 5503 >/dev/null 2>&1 &"
H2_START="nohup iperf -c ${H3_IP} ${UDP_TOGGLE} -b ${H2_DEMAND}M -t 30 -p 5503 >/dev/null 2>&1 &"

# main script
sshpass -p "${CTRL_PASS}" ssh -n host4@host4 "${CTRL_SETUP}"
echo "ryuRestDBA started on controller"
sleep 10s

sshpass -p "${H3_PASS}" ssh -n -p $H3_PORT host3@host3 "${H3_SETUP}"
echo "Iperf server started on Host 3 - Port 5503"

sshpass -p "${H1_PASS}" ssh -n -p $H1_PORT host1@host1 "${H1_START}" &
echo "Iperf client started on Host 1"

sshpass -p "${H2_PASS}" ssh -n -p $H2_PORT host2@host2 "${H2_START}" &
echo "Iperf client started on Host 2"

sleep 33s

sshpass -p "${H3_PASS}" ssh -p $H3_PORT host3@host3 "${H3_TEARDOWN}"
echo "Iperf server shut down on Host 3"

sshpass -p "${CTRL_PASS}" ssh -n host4@host4 "${CTRL_TEARDOWN}"
echo "ryuRestDBA stopped on controller"

sshpass -p "${H3_PASS}" scp -P ${H3_PORT} host3@host3:${FILE_NAME}_results.log ${LOCAL_RESULTS_FOLDER}
sshpass -p "${H3_PASS}" ssh -p ${H3_PORT} host3@host3 "${H3_CLEANUP}"

sshpass -p "${CTRL_PASS}" scp host4@host4:${RYURESTDBA_INSTALL}${FILE_NAME}.csv ${LOCAL_RESULTS_FOLDER}
sshpass -p "${CTRL_PASS}" ssh host4@host4 "${CTRL_CLEANUP}"

echo "------ New Trial ------" >> ${LOCAL_RESULTS_FOLDER}${FILE_NAME}_all_trials.log
cat ${LOCAL_RESULTS_FOLDER}${FILE_NAME}_results.log >> ${LOCAL_RESULTS_FOLDER}${FILE_NAME}_all_trials.log
echo "Results downloaded - ${LOCAL_RESULTS_FOLDER}${FILE_NAME}_results.log"
echo "Cumulative results at ${LOCAL_RESULTS_FOLDER}${FILE_NAME}_all_trials.log"
echo "and at ${LOCAL_RESULTS_FOLDER}${FILE_NAME}.csv"

cat ${LOCAL_RESULTS_FOLDER}${FILE_NAME}_results.log

pipenv run python ./tools/plotTool.py ${LOCAL_RESULTS_FOLDER}${FILE_NAME}.csv -s -ng >> ${LOCAL_RESULTS_FOLDER}${FILE_NAME}_all_csv_details.log
cat ${LOCAL_RESULTS_FOLDER}${FILE_NAME}_all_csv_details.log