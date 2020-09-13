FROM oceanprotocol/brizo:v0.7.2

# Proxy Server Configuration
ENV PROXY_SERVER_WORKERS='8'
ENV PROXY_SERVER_TIMEOUT='9000'
ENV PROXY_SERVER_HOST='0.0.0.0'
ENV PROXY_SERVER_PORT='3580'

#ENV PROXY_SERVER_HOSTNAME='myproxyhost.com'
#ENV PROXY_SERVER_TOKEN_EXPIRATION_MIN=2

# Install custom packages
COPY dist/osmosis_streaming_driver-0.0.1-py2.py3-none-any.whl /brizo
COPY dist/osmosis_driver_interface-0.0.7-py2.py3-none-any.whl /brizo
RUN pip install /brizo/osmosis_streaming_driver-0.0.1-py2.py3-none-any.whl
RUN pip install --force /brizo/osmosis_driver_interface-0.0.7-py2.py3-none-any.whl

COPY docker-assets/docker-entrypoint.sh /brizo 

EXPOSE 3580

