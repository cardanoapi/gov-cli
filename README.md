GOV CLI
================
Cli wrapper on top of cardano-cli for governance actions on cardano blockchain


### Features
- Key generation auto loading of required keys when making transactions
- Automatic transaction balancing
- Automatic query of deposits and collateral
- Automatic query of prev-gov-action and gov-action deposit
- Automatic query of constitution guardrail-script and use in proposals.

Tutorial : [Quick Start with Gov-Cli](https://cardanoapi.github.io/gov-cli/docs/intro)


### Installation
```
$ pip install gov-cli
$ gov-cli help
  Usage:
  
     gov-cli <command> [*options]

  Available commands:
  
    ls         -> list proposed gov-actions
    tip        -> show blockchain tip 
    wallet     -> show wallet info
    balance    -> print wallet balance
    
    gen [wallet|drep|cc]
    guardrail load  <gurdrail-script-file-path>
    
    register  <stake|drep|cc>
    delegate  <abstain|no-confidence|self|<drep_id>>
    propose  <proposal_type>  [*proposal-related_cli_args]
    vote  <drep|cc>  <gov-action-tx#index>  [yes|no]
    
    tx [script] [*cli-args]   
```
