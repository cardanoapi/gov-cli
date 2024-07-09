---
sidebar_position: 7
---

# Voting

In order to vote, you will require the list of active proposals, You can list them with:

```
gov-cli ls

```

**Governance action id format**: `proposedTxHash#index`.

### Cast vote with drep keys


```
gov-cli drep vote <gov_action> [yes|no|abstain]
gov-cli vote drep <gov_action> [yes|no|abstain]
```


### examples:
```bash
gov-cli vote drep ea478d10558aa77247440cfbf053bfd5d219003fcde26bd1e3204d738711d076#0         # vote yes
gov-cli vote drep ea478d10558aa77247440cfbf053bfd5d219003fcde26bd1e3204d738711d076#0 yes     # vote yes
gov-cli vote drep ea478d10558aa77247440cfbf053bfd5d219003fcde26bd1e3204d738711d076#0 no      # vote no
gov-cli vote drep ea478d10558aa77247440cfbf053bfd5d219003fcde26bd1e3204d738711d076#0 abstain # vote abstain
```

### Cast vote with cc keys


```
gov-cli cc vote <gov_action> [yes|no|abstain]
gov-cli vote cc <gov_action> [yes|no|abstain]
```


