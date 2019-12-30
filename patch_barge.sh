#!/bin/bash

OSM_INTERFACE_WITH_WSS_REPO=git@github.com:marcojrfurtado/osmosis-driver-interface.git
OSM_INTERFACE_WITH_WSS_TGT=../osmosis-driver-interface-wss

if [[ ! -d ${OSM_INTERFACE_WITH_WSS_TGT} ]]
then
	mkdir -p ${OSM_INTERFACE_WITH_WSS_TGT}
	cd ${OSM_INTERFACE_WITH_WSS_TGT} && git clone ${OSM_INTERFACE_WITH_WSS_REPO} . && cd -
fi

# Build dependencies
make dist
cd ${OSM_INTERFACE_WITH_WSS_TGT} && make dist && cd -
cp ${OSM_INTERFACE_WITH_WSS_TGT}/dist/*.whl ./dist/


# Build container for patched Brizo and copy patched compose file
docker build . -t brizo-with-wss-support && cp compose-files/patched_brizo.yml ../barge/compose-files/brizo.yml
