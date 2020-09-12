#!/bin/sh

# Bash script to turn Cycles multi-mode file into seperate control files to run
# batch simulations

# Name of multi-simulation file
MULTI_FILE=input/$1

# Spin-up control (1 = spin-up, 2 = normal simulation)
SPIN_UP=$2

{
    # Skip header line
    read

    while IFS= read -r line
    do
        # Read control parameters from one line
        SIM_CODE=$(echo ${line} | awk '{print $1}')
        ROT_YEARS=$(echo ${line} | awk '{print $2}')
        START_YEAR=$(echo ${line} | awk '{print $3}')
        END_YEAR=$(echo ${line} | awk '{print $4}')
        USE_REINIT=$(echo ${line} | awk '{print $5}')
        CROP_FILE=$(echo ${line} | awk '{print $6}')
        OPER_FILE=$(echo ${line} | awk '{print $7}')
        SOIL_FILE=$(echo ${line} | awk '{print $8}')
        WX_FILE=$(echo ${line} | awk '{print $9}')
        REINIT_FILE=$(echo ${line} | awk '{print $10}')
        HOURLY_INFIL=$(echo ${line} | awk '{print $11}')
        AUTO_N=$(echo ${line} | awk '{print $12}')

        # Write to a control file
        cat << EOF > "input/${SIM_CODE}.ctrl"
SIMULATION_START_YEAR   ${START_YEAR}
SIMULATION_END_YEAR     ${END_YEAR}
ROTATION_SIZE           ${ROT_YEARS}

## SIMULATION OPTIONS ##
USE_REINITIALIZATION    ${USE_REINIT}
ADJUSTED_YIELDS         0
HOURLY_INFILTRATION     ${HOURLY_INFIL}
AUTOMATIC_NITROGEN      ${AUTO_N}
AUTOMATIC_PHOSPHORUS    0
AUTOMATIC_SULFUR        0
DAILY_WEATHER_OUT       0
DAILY_CROP_OUT          0
DAILY_RESIDUE_OUT       0
DAILY_WATER_OUT         0
DAILY_NITROGEN_OUT      0
DAILY_SOIL_CARBON_OUT   0
DAILY_SOIL_LYR_CN_OUT   0
ANNUAL_SOIL_OUT         0
ANNUAL_PROFILE_OUT      0
ANNUAL_NFLUX_OUT        1

## OTHER INPUT FILES ##
CROP_FILE               ${CROP_FILE}
OPERATION_FILE          ${OPER_FILE}
SOIL_FILE               ${SOIL_FILE}
WEATHER_FILE            ${WX_FILE}
REINIT_FILE             ${REINIT_FILE}

EOF

        # Run Cycles simulation in brief mode
        if [ $SPIN_UP == 1 ]; then
            ./Cycles -s -b ${SIM_CODE}
        else
            # Unzip soil file from archive
            SOIL_ARCHIVE=${1%%.*}
            SOIL_ARCHIVE="${SOIL_ARCHIVE/NT/CT}_soil.zip"
            unzip -oj ${SOIL_ARCHIVE} input/${SOIL_FILE} -d ./input
            ./Cycles -b ${SIM_CODE}
        fi

        if [ "$?" == 0 ]; then
            SUCCESS=1
        else
            SUCCESS=0
        fi

        # Delete generated control file
        rm input/${SIM_CODE}.ctrl

        # Use multi-mode name as archive file name
        ZIP=${MULTI_FILE#"input/"}
        ZIP=${ZIP%%.*}

        # Add output to archive and then delete
        if [ $SUCCESS == 1 ]; then
            zip -ur ${ZIP}.zip output/${SIM_CODE} &> /dev/null
        else
            echo "Simulation ${SIM_CODE} failed"
        fi
        rm -r output/${SIM_CODE} &> /dev/null

        # Add steady-state soil file to archive and then delete
        if [ $SPIN_UP == 1 ]; then
            SOIL_ARCHIVE=
            zip -u ${1%.txt}_soil.zip input/${SIM_CODE}_ss.soil &> /dev/null
            rm input/${SIM_CODE}_ss.soil &> /dev/null
        else
            rm input/${SOIL_FILE}
        fi

    done
}<"$MULTI_FILE"

