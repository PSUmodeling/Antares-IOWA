#!/bin/sh

# Bash script to find unfinished runs
# Usage:
# ./find_unfinished MULTI_MODE_FILE_BACKUP SCENARIO
# Note that the multi-mode file back up should contain all simulations, and
# cannot be the one in the input directory.
# The script will delete the multi-mode file in the input directory to the
# SCENARIO, and replace it with a new one containing only unfinished
# runs.

MULTI_FILE1=$1
SCENARIO=$2

# Check content of the archive to find finished runs
unzip -l ${SCENARIO}.zip > ${SCENARIO}.log

# Delete the existing multi-mode file in input directory
MULTI_FILE2=input/$2.txt
rm ${MULTI_FILE2}

# Write header
echo "SIM_CODE 				 ROTATION_YEARS START_YEAR END_YEAR USE_REINIT CROP_FILE 	 OPERATION_FILE 			 SOIL_FILE             	 WEATHER_FILE 	 REINIT_FILE HOURLY_INFILTRATION AUTOMATIC_NITROGEN" > ${MULTI_FILE2}

# Read complete list of runs from the multi-mode file backup and compare with
# the list of finished runs
{
    # Skip header line
    read

    while IFS= read -r line
    do
        # Read control parameters from one line
        SIM_CODE=$(echo ${line} | awk '{print $1}')

        if ! grep -q "${SIM_CODE}" ${SCENARIO}.log; then
            # If not found in the finished-run list, write it to new multi-mode
            # file
            echo "Add ${SIM_CODE} to the new multi-mode file"
            echo ${line} >> ${MULTI_FILE2}
        fi
    done
}<"$MULTI_FILE1"

# Remove the list of finished runs
rm ${SCENARIO}.log
