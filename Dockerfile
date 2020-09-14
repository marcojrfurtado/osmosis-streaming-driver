FROM marcojrfurtado/provider-py

# Proxy Server Configuration
ENV PROXY_SERVER_WORKERS='4'
ENV PROXY_SERVER_TIMEOUT='9000'
ENV PROXY_SERVER_HOST='0.0.0.0'
ENV PROXY_SERVER_PORT='3580'

#ENV PROXY_SERVER_HOSTNAME='myproxyhost.com'
#ENV PROXY_SERVER_TOKEN_EXPIRATION_MIN=2

# Install custom packages
COPY dist/osmosis_streaming_driver-0.0.1-py2.py3-none-any.whl /ocean-provider
COPY dist/ocean_provider-0.1.0-py2.py3-none-any.whl /ocean-provider
RUN pip uninstall -y osmosis-streaming-driver ocean-provider
RUN pip install wheel /ocean-provider/osmosis_streaming_driver-0.0.1-py2.py3-none-any.whl
RUN pip install wheel /ocean-provider/ocean_provider-0.1.0-py2.py3-none-any.whl
COPY docker-assets/docker-entrypoint.sh /ocean-provider

EXPOSE 8030
EXPOSE 3580

