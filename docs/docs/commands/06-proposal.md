---
sidebar_position: 6
---
# Proposals

Let's first understand the items required for a proposal

## Proposal Components

### 1. Anchor

When proposing a governance action, the proposer may employ an *anchor*, which comprises a *URL* hosting a document that outlines the rationale
for the proposed changes, along with the document's *hash*.

The document at the URL can be of a free form. It's important that it should communicate to ada holders the *what* and the *why* of the proposal. This tutorial mostly uses 'https://raw.githubusercontent.com/Ryun1/metadata/main/cip108/treasury-withdrawal.jsonld' as an example, see [here](https://github.com/Ryun1/CIPs/blob/governance-metadata-actions/CIP-0108/test-vector.md) for more details.

See [CIP-100 | Governance Metadata](https://github.com/cardano-foundation/CIPs/tree/master/CIP-0100) and [CIP-0108? | Governance Metadata - Governance Actions](https://github.com/cardano-foundation/CIPs/pull/632) for standard.
Following CIP-100, we canonize the metadata anchor first, via [JSON-LD playground](https://json-ld.org/playground/), which we then hash.

You can use `cardano-cli` to get the hash:

```bash
cardano-cli conway governance hash anchor-data --file-text treasury-withdrawal.canonical
931f1d8cdfdc82050bd2baadfe384df8bf99b00e36cb12bfb8795beab3ac7fe5
```
Alternatively, utilize b2sum to hash the document:

```bash
b2sum -l 256 treasury-withdrawal.canonical
931f1d8cdfdc82050bd2baadfe384df8bf99b00e36cb12bfb8795beab3ac7fe5  treasury-withdrawal.canonical
```
You will need to supply the hash of the document when creating a governance action.


### 2. Guardrail script


Guardrail script validates certain parameters on proposals to make sure that it complies with the constitution. The script is injected wherever required.

Link: https://github.com/IntersectMBO/constitution-priv 

Follow the instructions in the README.md file to compile the PlutusV3 script. A successful compilation creates the 'compiled' directory containing the script in a text envelope.

```
cat compiled/guardrails-script.plutus 
```
```
{
    "type": "PlutusScriptV3",
    "description": "",
    "cborHex": "59082f59082c0101003232323232323232323232323232323232323232323232323232323232323232323232323232323232323225932325333573466e1d2000001180098121bab357426ae88d55cf001054ccd5cd19b874801000460042c6aae74004dd51aba1357446ae88d55cf1baa325333573466e1d200a35573a00226ae84d5d11aab9e0011637546ae84d5d11aba235573c6ea800642b26006003149a2c8a4c3021801c0052000c00e0070018016006901e40608058c00e00290016007003800c00b0034830268320306007001800600690406d6204e00060001801c0052004c00e007001801600690404001e0006007001800600690404007e00060001801c0052006c00e006023801c006001801a4101000980018000600700148023003801808e0070018006006904827600060001801c005200ac00e0070018016006904044bd4060c00e003000c00d2080ade204c000c0003003800a4019801c00e003002c00d2080cab5ee0180c100d1801c005200ec00e0060238000c00e00290086007003800c00b003483d00e0306007001800600690500fe00040243003800a4025803c00c01a0103003800a4029803c00e003002c00cc07520d00f8079801c006001801980ea4120078001800060070014805b00780180360070018006006603e900a4038c0003003800a4041801c00c04601a3003800a4045801c00e003002c00d20f02e80c1801c006001801a4190cb80010090c00e00290126000c00e0029013600b003803c00e003002c00cc0752032c000c00e003000c00cc075200ac000c0006007007801c006005801980ea418170058001801c006001801980ea41209d80018000c0003003800a4051802c00e007003011c00e003000c00d2080e89226c000c0006007003801808e007001800600690406c4770b7e000600030000c00e0029015600b003801c00c047003800c00300348202e2e1cb00030001801c00e006023801c006001801a410181f905540580018000c0003003800a4059801c00c047003800c00300348203000700030000c00e00290176007003800c00b003483200603060070018006006904801e00040243003800a4061801c00c0430001801c0052032c016006003801801e00600780180140100c00e002901a600b003001c00c00f003003c00c00f003002c00c007003001c00c007003803c00e003002c00c0560184014802000c00e002901b6007003800c00b003480030034801b0001801c006001801a4029800180006007001480e3003801c006005801a4001801a40498000c00e003000c00d20ca04c00080486007001480eb00380180860070018006006900f600060001801c005203cc00e006015801c006001801a4101012bcf138c09800180006007001480fb003801805600700180060069040505bc3f482e00060001801c0052040c00e0070018016006900d4060c00e003000c00d204ac000c0003003800a4085801c00c04601630000000000200f003006c00e003000c00c05a0166000200f003005c00e003000c00c057003010c0006000200f003800c00b003012c00cc05d2028c0004008801c01e007001801600602380010043000400e003000c00c04b003011c0006000800c00b00300d8049001801600601d801980924190038000801c0060010066000801c00600900f6000800c00b003480030034820225eb0001003800c003003483403f0003000400c023000400e003000c00d208094ebdc03c000c001003009c001003300f4800b0004006005801a40058001001801401c6014900518052402860169004180424008600a900a180324005003480030001806240cc6016900d18052402460129004180424004600e900018032400c6014446666aae7c004a0005003328009aab9d0019aab9e0011aba100298019aba200224c6012444a6520071300149a4432005225900689802a4d2219002912c998099bad0020068ac99807002800c4cc03001c00e300244cc03001c02a3002012c801460012218010c00888004c004880094cc8c0040048848c8cc0088c00888c00800c8c00888c00400c8d4cc01001000cd400c0044888cc00c896400a300090999804c00488ccd5cd19b87002001800400a01522333573466e2000800600100291199ab9a33712004003000801488ccd5cd19b89002001801400244666ae68cdc4001000c00a001225333573466e240080044004400a44a666ae68cdc4801000880108008004dd6801484cc010004dd6001484c8ccc02a002452005229003912999ab9a3370e0080042666ae68cdc3801800c00200430022452005229003911980899b820040013370400400648a400a45200722333573466e20cdc100200099b82002003800400880648a400a45200722333573466e24cdc100200099b82002003801400091480148a400e44666ae68cdc419b8200400133704004007002800122593300e0020018800c400922593300e00200188014400400233323357346ae8cd5d10009198051bad357420066eb4d5d08011aba2001268001bac00214800c8ccd5cd1aba3001800400a444b26600c0066ae8400626600a0046ae8800630020c0148894ccd5cd19b87480000045854ccd5cd19b88001480004cc00ccdc0a400000466e05200000113280099b8400300199b840020011980200100098021112999ab9a3370e9000000880109980180099b860020012223300622590018c002443200522323300d225900189804803488564cc0140080322600800318010004b20051900991111111001a3201322222222005448964ce402e444444440100020018c00a30000002225333573466e1c00800460002a666ae68cdc48010008c010600445200522900391199ab9a3371266e08010004cdc1001001c0020041191800800918011198010010009"
}
```

Now, get the script hash with:

```shell
cardano-cli conway governance hash script --script-file guardrails-script.plutus 
edcd84c10e36ae810dc50847477083069db796219b39ccde790484e0
```


#### Setting guardrail-script on gov-cli

```
gov-cli guardrail load ./guardrails-script.plutus 
```

**Note** this will use the guardrail script whenever it is required.


## Submitting Proposals

### Update committee

#### Update committee to *add* a new CC member:

Assume you want to add three CC members, who have generated cold keys and have provided their key hashes:
- `89181f26b47c3d3b6b127df163b15b74b45bba7c3b7a1d185c05c2de`
- `ea8738081fca0726f4e781f5e55fda05f8745432a5f8a8d09eb0b34b`
- `7f6721067362d4ae9ca73469fe983ce5572dad9028386100104b0da0`

You can submit a proposal to add them as new CC members with an expiration epoch (`--epoch`) for each of them. This is a good time to review the quorum. Let’s assume that 2/3 of the committee needs to accept the proposal:

Create the governance action proposal:
```bash
cardano-cli propose update-committee \
  --anchor-url https://raw.githubusercontent.com/Ryun1/metadata/main/cip108/treasury-withdrawal.jsonld \
  --anchor-data-hash 931f1d8cdfdc82050bd2baadfe384df8bf99b00e36cb12bfb8795beab3ac7fe5 \
  --add-cc-cold-verification-key-hash 89181f26b47c3d3b6b127df163b15b74b45bba7c3b7a1d185c05c2de \
  --epoch 100 \
  --add-cc-cold-verification-key-hash ea8738081fca0726f4e781f5e55fda05f8745432a5f8a8d09eb0b34b \
  --epoch 95 \
  --add-cc-cold-verification-key-hash 7f6721067362d4ae9ca73469fe983ce5572dad9028386100104b0da0 \
  --epoch 90 \
  --threshold 2/3
```

#### Update committee to *remove* an existing CC member:

Assume that you want to remove the CC member with the key hash `89181f26b47c3d3b6b127df163b15b74b45bba7c3b7a1d185c05c2de`. You can do this with:

```bash
gov-cli propose update-committee \
  --anchor-url https://raw.githubusercontent.com/Ryun1/metadata/main/cip108/treasury-withdrawal.jsonld \
  --anchor-data-hash 931f1d8cdfdc82050bd2baadfe384df8bf99b00e36cb12bfb8795beab3ac7fe5 \
  --remove-cc-cold-verification-key-hash 89181f26b47c3d3b6b127df163b15b74b45bba7c3b7a1d185c05c2de \
  --threshold 1/2 
```

#### Update committee to only change the *threshold*:

```bash
gov-cli propose update-committee \
  --anchor-url https://raw.githubusercontent.com/Ryun1/metadata/main/cip108/treasury-withdrawal.jsonld \
  --anchor-data-hash 931f1d8cdfdc82050bd2baadfe384df8bf99b00e36cb12bfb8795beab3ac7fe5 \
  --threshold 60/100 
```

### Updating the constitution

This section describes how to propose a new constitution. Lets's use as an axample the interim constitution that is to be used 
on Mainnet. It is available in https://ipfs.io/ipfs/Qmdo2J5vkGKVu2ur43PuTrM7FdaeyfeFav8fhovT6C2tto


#### Prepare the constiuttion anchor.

When proposing a new constitution, you are required to put it on a URL that is publicly accessible and, idealy, in some sort of persistent form. For example 
put it on IPFS, like the [interim constitution](https://ipfs.io/ipfs/Qmdo2J5vkGKVu2ur43PuTrM7FdaeyfeFav8fhovT6C2tto)

Now, download the file from the url:

```bash
wget https://ipfs.io/ipfs/Qmdo2J5vkGKVu2ur43PuTrM7FdaeyfeFav8fhovT6C2tto -O constitution.txt
```

Get its hash, you can do it with blake2 or with cardano-cli:

```bash
b2sum -l 256 constitution.txt
a77245f63bc7504c6ce34383633729692388dc1823723b0ee9825743a87a6a6d  constitution.txt
```
or

```bash
cardano-cli conway governance hash anchor-data --file-text constitution.txt
a77245f63bc7504c6ce34383633729692388dc1823723b0ee9825743a87a6a6d
```


#### Create the proposal to update the constitution:

When there is no previously enacted constiutition: 

```bash
gov-cli propose create-constitution \
  --anchor-url https://raw.githubusercontent.com/cardano-foundation/CIPs/master/CIP-0100/cip-0100.common.schema.json \
  --anchor-data-hash "9d99fbca260b2d77e6d3012204e1a8658f872637ae94cdb1d8a53f4369400aa9" \
  --constitution-url https://ipfs.io/ipfs/Qmdo2J5vkGKVu2ur43PuTrM7FdaeyfeFav8fhovT6C2tto \
  --constitution-hash "a77245f63bc7504c6ce34383633729692388dc1823723b0ee9825743a87a6a6d" \
  --constitution-script-hash "edcd84c10e36ae810dc50847477083069db796219b39ccde790484e0"
```


### Motion of no confidence

Signal that you have no confidence on current constitutional committee.

#### Create a no-confidence governance action:

```bash
gov-cli propose create-no-confidence \
  --anchor-url https://raw.githubusercontent.com/Ryun1/metadata/main/cip108/treasury-withdrawal.jsonld \
  --anchor-data-hash 931f1d8cdfdc82050bd2baadfe384df8bf99b00e36cb12bfb8795beab3ac7fe5
```

### Treasury withdrawal

In addition to the stake credential required to obtain a deposit refund, the proposer must also furnish stake credentials for receiving funds from the treasury in the
event that the governance action is approved.

Also, treasury withdrawals must reference the Guardrails script. 

#### Create the treasury withdrawal proposal:


```bash
gov-cli propose create-treasury-withdrawal \
  --anchor-url https://raw.githubusercontent.com/Ryun1/metadata/main/cip108/treasury-withdrawal.jsonld \
  --anchor-data-hash 931f1d8cdfdc82050bd2baadfe384df8bf99b00e36cb12bfb8795beab3ac7fe5 \
  --funds-receiving-stake-verification-key-file "$HOME/.cardano/keys/stake.vkey"\
  --transfer 50000000000
```


### Info Proposal

Used for offline discussions on different topics

#### Create the 'info' governance action:

```bash
gov-cli propose create-info \
  --anchor-url  https://tinyurl.com/yc74fxx4 \
  --anchor-data-hash 931f1d8cdfdc82050bd2baadfe384df8bf99b00e36cb12bfb8795beab3ac7fe5 \
```

### Update protocol parameters



```bash
gov-cli propose create-protocol-parameters-update \
  --anchor-url https://raw.githubusercontent.com/Ryun1/metadata/main/cip108/treasury-withdrawal.jsonld \
  --anchor-data-hash 931f1d8cdfdc82050bd2baadfe384df8bf99b00e36cb12bfb8795beab3ac7fe5 \
  --key-reg-deposit-amt 1000000
```

#### List of updatable parameters

- `--min-fee-linear LOVELACE`
- `--min-fee-constant LOVELACE`
- `--max-block-body-size WORD32`
- `--max-tx-size WORD32`
- `--max-block-header-size WORD16`
- `--key-reg-deposit-amt NATURAL`
- `--pool-reg-deposit NATURAL`
- `--pool-retirement-epoch-interval WORD32`
- `--number-of-pools NATURAL`
- `--pool-influence RATIONAL`
- `--treasury-expansion RATIONAL`
- `--monetary-expansion RATIONAL`
- `--min-pool-cost NATURAL`
- `--price-execution-steps RATIONAL`
- `--price-execution-memory RATIONAL`
- `--max-tx-execution-units (INT, INT)`
- `--max-block-execution-units (INT, INT)`
- `--max-value-size INT`
- `--collateral-percent INT`
- `--max-collateral-inputs INT`
- `--utxo-cost-per-byte LOVELACE`
- `--pool-voting-threshold-motion-no-confidence RATIONAL`
- `--pool-voting-threshold-committee-normal RATIONAL`
- `--pool-voting-threshold-committee-no-confidence RATIONAL`
- `--pool-voting-threshold-hard-fork-initiation RATIONAL`
- `--pool-voting-threshold-pp-security-group RATIONAL`
- `--drep-voting-threshold-motion-no-confidence RATIONAL`
- `--drep-voting-threshold-committee-normal RATIONAL`
- `--drep-voting-threshold-committee-no-confidence RATIONAL`
- `--drep-voting-threshold-update-to-constitution RATIONAL`
- `--drep-voting-threshold-hard-fork-initiation RATIONAL`
- `--drep-voting-threshold-pp-network-group RATIONAL`
- `--drep-voting-threshold-pp-economic-group RATIONAL`
- `--drep-voting-threshold-pp-technical-group RATIONAL`
- `--drep-voting-threshold-pp-governance-group RATIONAL`
- `--drep-voting-threshold-treasury-withdrawal RATIONAL`
- `--min-committee-size INT`
- `--committee-term-length WORD32`
- `--governance-action-lifetime WORD32`
- `--new-governance-action-deposit NATURAL`
- `--drep-deposit LOVELACE`
- `--drep-activity WORD32`
- `--ref-script-cost-per-byte RATIONAL`
- `--cost-model-file FILE`
