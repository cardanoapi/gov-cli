---
sidebar_position: 3
---

# Utility Commands

### Print wallet info
```
gov-cli wallet
```

### Query blockchain tip

```
gov-cli tip
```

### List proposed gov-actions


```
gov-cli ls
```

### Get wallet balance


```
gov-cli balance [address]
```

- `address`: The address to query. If not specified, reads the address from `payment.addr` in the keys directory.


### `transfer`

Transfers funds to a specified address.

```
Usage: gov-cli transfer <address> <amount>
```

- `address`: The recipient's address.
- `amount`: The amount to transfer.

### `tx`

Helper to create transactions and submit without having to fill in evey stuffs

```
gov-cli tx [script] [...cli args]
```

**example1**: Payment to smart contact

```
./gov-cli tx \
    --tx-out addr_test1wz6gk3gq9aatj78d65x8vttxh0wh4gsr78qh3ryleecvrxcugy0p6+3000000 \
    --tx-out-inline-datum-value '{}'
```

**example2**: Reedeming from smart cont

```
./gov-cli tx script \
--tx-in '316930ca32b97f92c680fd487367dc70def458dcd2ae69bbe7ee45be57839fc4#0' \
--tx-in-script-file ./alwaysSpend.plutusV2 \
--tx-in-redeemer-value '{}' \
--tx-in-inline-datum-present  
```
