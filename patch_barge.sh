#!/bin/bash

BARGE_DIR=../barge
if [ "$#" -eq 1 ]
then
	BARGE_DIR=$1
fi

if [ ! -d ${BARGE_DIR} ]
then
	echo "Barge root directory not found. Usage: ./patch_barge.sh <BARGE DIR>"
	exit -1
fi

OSM_INTERFACE_WITH_WSS_REPO=https://github.com/marcojrfurtado/osmosis-driver-interface.git
OSM_INTERFACE_WITH_WSS_TGT=../osmosis-driver-interface-wss

echo "Cloning custom osm-driver-interface ..."
if [[ ! -d ${OSM_INTERFACE_WITH_WSS_TGT} ]]
then
	mkdir -p ${OSM_INTERFACE_WITH_WSS_TGT}
	cd ${OSM_INTERFACE_WITH_WSS_TGT} && git clone ${OSM_INTERFACE_WITH_WSS_REPO} . && cd -
fi

# Build dependencies
echo "Building module..."
make dist
cd ${OSM_INTERFACE_WITH_WSS_TGT} && make dist && cd -
cp ${OSM_INTERFACE_WITH_WSS_TGT}/dist/*.whl ./dist/


# Build container for patched Brizo and copy patched compose file
echo "Building container..."
docker build . -t brizo-with-wss-support && cp docker-assets/compose-files/patched_brizo.yml ${BARGE_DIR}/compose-files/brizo.yml


echo "Done."
