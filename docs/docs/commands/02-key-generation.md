---
sidebar_position: 2
---

# Key Generation

`gov-cli` reads keys from the directory set with following key variable:

- `KEYS_DIR` env variable. If this not set, default directory for key generation is `$HOME/.cardano/keys`

Keys are classified into following types
- Wallet keys - payment and stake keys
- Drep keys  - drep stake keys
- CC keys - hot and cold key pairs for Constitutional Committee




### Wallet keys

Generates keys for wallet
```bash
gov-cli gen wallet
```

Following files are created.
 - `$KEYS_DIR`/payment.skey
 - `$KEYS_DIR`/payment.vkey
 - `$KEYS_DIR`/stake.skey
 - `$KEYS_DIR`/stake.vkey
 - `$KEYS_DIR`/payment.addr
 - `$KEYS_DIR`/stake_reg.cert


### Drep keys

```bash
gov-cli gen drep
```

Following files are created.
 - `$KEYS_DIR`/drep.skey
 - `$KEYS_DIR`/drep.vkey
 - `$KEYS_DIR`/drep.id


### Constitutional Committee Keys

Generate cold and hot keys for cc wallet.

```
gov-cli gen cc
```

Following files are created.
 - `$KEYS_DIR`/cc-hot.skey
 - `$KEYS_DIR`/cc-hot.vkey
 - `$KEYS_DIR`/cc-cold.skey
 - `$KEYS_DIR`/cc-cold.vkey
 - `$KEYS_DIR`/cc-hot-key-authorization.cert
