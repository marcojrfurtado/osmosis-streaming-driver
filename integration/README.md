# Running Brizo Integration test

Integration test for osmosis-streaming-driver.

## Requirements

* Node.JS v11.15

Simply select it with NVM:

```
nvm use 11.15
```

Note: Other version might work, but newer versions are known to have issues with dependency '@truffle/hdwallet-provider'. 

## Setting up / Running test

### Ocean

Start it with Barge, wait for keeper node to start

```
<BARGE DIR>/start_ocean.sh
```

### Build

```
npm install
```

### Keeper contracts

Copy Keeper contracts before running

```
./scripts/keeper.sh
```

This command will hang until contracts have been copied.

### Running

```
npm run integration
```
