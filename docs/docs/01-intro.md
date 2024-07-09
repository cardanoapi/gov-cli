---
sidebar_position: 1
---
# Gov Cli

## Overview

This command-line utility, `gov-cli`, provides a set of functionalities to work with cardano keys and perform governance related actions.

## Prerequisites

- Python 3 or higher
- Cardano CLI in path
- A running Cardano node

## Environment Variables

- `CARDANO_NODE_SOCKET_PATH` : Node socket path to be used by cardano-cli
- `NETWORK` : `mainnet|preview|preprod|sancho|1|2|4|42` : Network magic or some common names
- `LOG_CLI` : `true|false|yes|no` Toggle logging of cli commands used for command
- `KEYS_DIR` : Directory where keys are stored. Keys are used when creating transactions

## Quick Start (As a drep)

### 1. Create wallets
```
export CARDANO_NODE_SOCKET_PATH=$HOME/sancho/node.socket
export NETWORK=sancho

gov-cli gen
# or,
gov-cli wallet 

# Now make sure you have balance.
gov-cli balance
```
Now you need to fund your wallet

### 2. Register yourself as sole voter
```
gov-cli register stake
## wait for transaction to be confirmed


gov-cli register drep
## wait for transaction to be confirmed


gov-cli delegate self
```

### 3. Propose and vote on the gov-action
```
gov-cli propose update-committee \
  --anchor-url https://raw.githubusercontent.com/Ryun1/metadata/main/cip108/treasury-withdrawal.jsonld \
  --anchor-data-hash 931f1d8cdfdc82050bd2baadfe384df8bf99b00e36cb12bfb8795beab3ac7fe5 \
  --threshold 60/100 

```


### 4. Vote on your own proposal with your drep credentials
```
gov-cli vote drep 51e638ad93ba98fe1efefe9e3230e8a4ddf4d8b18f2aa85f9cb341a84176b0f4#0 yes
```


