---
sidebar_position: 4
---

#  Key Registration

Once keys are generated, they have to be registered on-chain


## Stake Registration
```
gov-cli register [stake]
```
This will register the `stake.vkey` into the chain. User's staking is not enabled only after the stake key is registreed.

Registers keys on the blockchain.

- `register`: Registers the stake key.
- `register drep`: Registers the DRep key.
- `register stake`: Registers the stake key.
- `register cc`: Authorizes hot keys with the cold keys for the Constitutional Committee (CC).