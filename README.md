[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://oceanprotocol.com)

# osmosis-streaming-driver

> 💧 Osmosis IPFS Driver Implementation
> [oceanprotocol.com](https://oceanprotocol.com)

[![Build Status](https://travis-ci.com/marcojrfurtado/osmosis-streaming-driver.svg)](https://travis-ci.com/oceanprotocol/osmosis-streaming-driver)
[![PyPI](https://img.shields.io/pypi/v/osmosis-streaming-driver.svg)](https://pypi.org/project/osmosis-streaming-driver/)

---

## Table of Contents

- [Setup](#setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [New Version](#new-version)
- [License](#license)

---

## Setup

Install the osmosis ipfs driver and set ipfs gateway envvar

```bash
pip install osmosis-ipfs-driver
export IPFS_GATEWAY=https://gateway.ipfs.io
```

Instantiate an Osmosis instance and resolve an ipfs url

```python
from osmosis_driver_interface.osmosis import Osmosis
url = "ipfs://ZnOfotxMMnLTXCCW0GPVYT8gtEugghgD8Hgz"
osm = Osmosis(url)  # the proper osmosis driver is loaded automatically to match the url

# Resolve the url
download_url = osm.data_plugin.generate_url(url)
```

## Code Style

Information about our Python code style is documented in the [python-developer-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-developer-guide.md)
and the [python-style-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-style-guide.md).

## Testing

Automatic tests are setup via Travis, executing `tox`.
Our tests use the pytest framework.

## New Version

The `bumpversion.sh` script helps to bump the project version. You can execute the script using as first argument {major|minor|patch} to bump accordingly the version.

## License

```text
Copyright 2019 Ocean Protocol Foundation Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

