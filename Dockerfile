FROM oceanprotocol/brizo:v0.7.2

# Install custom packages
COPY dist/osmosis_streaming_driver-0.0.1-py2.py3-none-any.whl /brizo
COPY dist/osmosis_driver_interface-0.0.7-py2.py3-none-any.whl /brizo
RUN pip install /brizo/osmosis_streaming_driver-0.0.1-py2.py3-none-any.whl
RUN pip install --force /brizo/osmosis_driver_interface-0.0.7-py2.py3-none-any.whl

EXPOSE 3580

