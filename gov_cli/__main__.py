#!/usr/bin/env python
import shutil
import subprocess
from subprocess import CompletedProcess
import os
import sys
from typing import List, Optional
import json

HOME=os.environ.get("HOME","/root")
# Define paths
KEYS_DIR = os.environ.get("CARDANO_KEYS_DIR",os.path.join(HOME,".cardano","keys"))
NETWORK = "--testnet-magic=4"
CARDANO_NODE_SOCKET_PATH=os.environ.get("CARDANO_NODE_SOCKET_PATH",os.path.join(HOME,'.cardano','testnet','node.socket')).strip()
if not os.path.exists(KEYS_DIR):
    os.makedirs(KEYS_DIR)
if(os.environ.get("NETWORK")):
    NETWORK = os.environ.get("NETWORK").strip()

    try:
        # Try to parse the string as an integer
        number = int(NETWORK)
        NETWORK="--testnet-magic="+ str(number)

    except ValueError:
        if NETWORK == 'mainnet':
            NETWORK = "--mainnet"
        elif NETWORK == 'snacho' or NETWORK == 'sanchonet':
            NETWORK="--testnet-magic=4"
        elif NETWORK == 'preview':
            NETWORK="--testnet-magic=2"
        elif NETWORK == 'preprod':
            NETWORK="--testnet-magic=1"
        elif NETWORK == 'testnet':
            NETWORK="--testnet-magic=42"
        pass

class SubmitResult:
    def __init__(self,process,txid):
        self.process:CompletedProcess=process
        self.txid:str=txid
log_cli= 'LOG_CLI' in os.environ and os.environ['LOG_CLI'].lower() not in ('no','off','false','0')
# Utility function to run cardano-cli commands
def run_cli_command(command: List[str],raise_error=True):
    if log_cli:
        print("> " + " ".join(command))
    try:
        result = subprocess.run(command, capture_output=True, text=True,check=raise_error)
    except  subprocess.CalledProcessError  as e:
        print(e.stdout)
        print(e.stderr)
        raise e
    if raise_error:
        return result.stdout.strip()
    return result
class Key:
    def __init__(self,private,public,id):
        self.private=private
        self.public=public
        self.id=id # this is either public key hash or certificate file.

class Wallet:
    
    def __init__(self, payment_vkey=None, payment_skey=None, stake_vkey=None, stake_skey=None, address=None):
        self.payment_vkey = payment_vkey
        self.payment_skey = payment_skey
        self.stake_vkey = stake_vkey
        self.stake_skey = stake_skey
        self.address = address

class WalletStore:
    
    def __init__(self,keys_dir ):
        self.keys_dir=keys_dir

    def gen_wallet(self,cli:'CardanoCLI'):
        
        payment_vkey = os.path.join(self.keys_dir, "payment.vkey")
        payment_skey = os.path.join(self.keys_dir, "payment.skey")
        stake_vkey = os.path.join(self.keys_dir, "stake.vkey")
        stake_skey = os.path.join(self.keys_dir, "stake.skey")
        payment_addr = os.path.join(self.keys_dir, "payment.addr")
        
        # Generate keys
        cli.cardano_cli( "address", "key-gen", ["--verification-key-file", payment_vkey, "--signing-key-file", payment_skey])
        cli.cardano_cli("stake-address", "key-gen", ["--verification-key-file", stake_vkey, "--signing-key-file", stake_skey])
        
        # Build the payment address
        cli.cardano_cli( "address", "build", ["--payment-verification-key-file", payment_vkey, "--stake-verification-key-file", stake_vkey, "--out-file", payment_addr],include_network=True)
        
        # Read the payment address from the file
        with open(payment_addr, 'r') as f:
            address = f.read().strip()

        return Wallet(payment_vkey, payment_skey, stake_vkey, stake_skey, address)

    def gen_drep_key(self,cli:'CardanoCLI'):
        drep_vkey = os.path.join(self.keys_dir, "drep.vkey")
        drep_skey = os.path.join(self.keys_dir, "drep.skey")
        drep_id = os.path.join(self.keys_dir, "drep.id.hex.txt")
        
        cli.cardano_cli_conway("governance", "drep",["key-gen", "--verification-key-file", drep_vkey, "--signing-key-file", drep_skey])
        cli.cardano_cli_conway("governance", "drep", ["id","--drep-verification-key-file",drep_vkey,"--out-file",drep_id,"--output-format","hex"])
        with open(drep_id, 'r') as f:
            id = f.read().strip()
            
        return Key(drep_skey,drep_vkey,id)

    def load_drep_key(self)->Key:
        drep_vkey = os.path.join(self.keys_dir, "drep.vkey")
        drep_skey = os.path.join(self.keys_dir, "drep.skey")
        drep_id = os.path.join(self.keys_dir, "drep.id.hex.txt")
        
        with open(drep_id) as f:
            drep_bech32=f.read().strip()
            return Key(drep_skey,drep_vkey,drep_bech32)
        
    def file_path(self,fname:str):
        return os.path.join(self.keys_dir, fname) 

    def gen_cc_keys(self,cli:'CardanoCLI')->(Key):
        cold_vkey = self.file_path("cc-cold.vkey")
        cold_skey = self.file_path("cc-cold.skey")
        cold_key_hash = self.file_path("cc-key.hash")
        
        hot_vkey = self.file_path("cc-hot.vkey")
        hot_skey = self.file_path("cc-hot.skey")
        authorization_cert=self.file_path("cc-hot-key-authorization.cert")
        

        cli.cardano_cli_conway("governance","committee",[
            "key-gen-cold",
            "--cold-verification-key-file",cold_vkey,
            "--cold-signing-key-file", cold_skey
        ])

        cc_id=cli.cardano_cli_conway("governance","committee",[
            "key-hash",
            "--verification-key-file",cold_vkey,
        ])
    
        with open(cold_key_hash,"wt") as f:
            f.write(cc_id)
            
        cli.cardano_cli_conway("governance","committee",[
            "key-gen-hot",
            "--verification-key-file",hot_vkey,
            "--signing-key-file", hot_skey
        ])  

        cli.cardano_cli_conway("governance","committee",[
            "create-hot-key-authorization-certificate",
            "--cold-verification-key-file",cold_vkey,
            "--hot-key-file", hot_vkey,
            "--out-file",authorization_cert
        ])
        return (Key(hot_skey,hot_vkey,cc_id),Key(cold_skey,cold_vkey,authorization_cert))

    def load_cc_cold_keys(self):
        cold_vkey = self.file_path("cc-cold.vkey")
        cold_skey = self.file_path("cc-cold.skey")
        cold_key_hash = self.file_path("cc-key.hash")
        with open(cold_key_hash) as f:
            cold_key_id=f.read()

        return Key(cold_skey,cold_vkey,cold_key_id)
    
    def load_cc_hot_keys(self):      
        hot_vkey = self.file_path("cc-hot.vkey")
        hot_skey = self.file_path("cc-hot.skey")
        authorization_cert=self.file_path("cc-hot-key-authorization.cert")
        return Key(hot_skey,hot_vkey,authorization_cert)
        
        
    def load_wallet(self):
        payment_vkey = os.path.join(self.keys_dir, "payment.vkey")
        payment_skey = os.path.join(self.keys_dir, "payment.skey")
        stake_vkey = os.path.join(self.keys_dir, "stake.vkey")
        stake_skey = os.path.join(self.keys_dir, "stake.skey")
        with open(os.path.join(self.keys_dir, "payment.addr")) as f:
            payment_addr=f.read().strip()

        return Wallet(payment_vkey, payment_skey, stake_vkey, stake_skey, payment_addr)

class CardanoCLI:
    def __init__(self, network="--mainnet", socket_path=None):
        self.network = network
        self.socket_path = socket_path

    def cardano_cli(self, command_type, command, params, include_network=False, include_socket=False,raise_error=True):
        base_command = ["cardano-cli", command_type, command] + params
        if include_socket and self.socket_path:
            base_command.extend(["--socket-path", self.socket_path])
        if include_network:
            base_command.append(self.network)
        return run_cli_command(base_command,raise_error=raise_error)
    
    def build_tx(self,wallet:Wallet,tx_name:str,commands:List[str],add_collateral=False):
        # Collect the UTXOs
        utxos:dict = self.query_utxos_json(wallet)
        tx_ins = []
        for utxo in utxos.keys():
            tx_ins.extend(["--tx-in", utxo])
        
        if add_collateral:
            commands.extend(["--tx-in-collateral",list(utxos.keys())[0]])
        
        # Build the transaction
        tx_body_file = os.path.join(KEYS_DIR, tx_name+"_tx.raw")


        self.cardano_cli_conway("transaction", "build", 
                          (commands+ tx_ins +["--out-file",tx_body_file,"--change-address", wallet.address]),
                        include_network=True, include_socket=True)
        return tx_body_file
        
    def build_and_submit(self,wallet:Wallet,tx_name:str,commands:List[str],raise_error=True,extra_keys=[],add_collateral=False):

        signed_tx_file = os.path.join(KEYS_DIR, tx_name+"_signed_tx.json")

        tx_body_file=self.build_tx(wallet,tx_name,commands,add_collateral) 
        return self.sign_and_submit(wallet,tx_body_file,signed_tx_file,raise_error=raise_error,extra_keys=extra_keys)
        

    
    def cardano_cli_conway(self, command_type, command, params=[], include_network=False, include_socket=False,raise_error=True):
        
        base_command = ["cardano-cli","conway", command_type, command] + params
        if include_socket and self.socket_path:
            base_command.extend(["--socket-path", self.socket_path])
        if include_network:
            base_command.append(self.network)
        return run_cli_command(base_command,raise_error=raise_error)    
    
    def load_gov_state(self,):
        gov_state=self.cardano_cli_conway("query","gov-state",include_network=True,include_socket=True)
        self.gov_state=json.loads(gov_state)


    def propose(self,wallet:Wallet,args):
        self.load_gov_state()
        proposal_type=args[0] if len (args) >0 else ''
        proposal_file=proposal_type+".proposal"
        req_prev=["create-no-confidence","update-committee","create-constitution","create-protocol-parameters-update","create-hardfork"]
        no_prev=["create-treasury-withdrawal","create-info"]
        require_guardrail=['create-treasury-withdrawal',"create-protocol-parameters-update"]
        prev_gov_action=[]
        build_extra_args=[]
        guardrail_script_file = os.path.join(KEYS_DIR, "guardrails-script.plutus")        

        
            
        if proposal_type in req_prev:
            prev_actions=self.gov_state['nextRatifyState']['nextEnactState']['prevGovActionIds']
            
            action_key={
                "create-no-confidence": "Committee",
                "update-committee": "Committee",
                "create-constitution": "Constitution",
                "create-protocol-parameters-update": "PParamUpdate",
                "create-hardfork": "Hardfork",
            }
            prev_action=prev_actions[action_key[proposal_type]]
            
            if prev_action: 
                prev_gov_action=["--prev-governance-action-tx-id", prev_action['txId'],
                                 "--prev-governance-action-index",str(prev_action['govActionIx'])]
                
        if proposal_type not in req_prev and proposal_type not in no_prev:
            print("Expected one of the following ")
            print(req_prev+no_prev)
            return
            
        
        deposit=self.gov_state["currentPParams"]["govActionDeposit"]
        extra_args=[
            "--governance-action-deposit",str(deposit),
            "--deposit-return-stake-verification-key-file",wallet.stake_vkey,
            "--out-file", proposal_file,
            '--mainnet'   if 'mainnet' in self.network  else '--testnet'
        ]
        require_collateral=False
        if proposal_type in require_guardrail:
            if self.gov_state['constitution']['script']:
                require_collateral=True
                # set the proposal script file.
                if '--proposal-script-file' not in args:
                    build_extra_args.extend([ "--proposal-script-file", guardrail_script_file,])
                    
                extra_args.extend(["--constitution-script-hash",self.gov_state['constitution']['script']])
                build_extra_args.extend([
                    "--proposal-redeemer-value","{}"
            ])

        self.cardano_cli_conway("governance","action",args+extra_args+prev_gov_action)
        tx=self.build_and_submit(wallet,'propose-gov-action-'+proposal_type,[
            "--proposal-file", proposal_file   
        ]+build_extra_args,add_collateral=require_collateral)
        print("Transaction submitted :",tx)
        print("GovAction Id          :",tx+'#0')
        

    def register_stake(self, wallet: Wallet):
        stake_cert = os.path.join(KEYS_DIR, "stake_reg.cert")
        # Generate stake key registration certificate
        self.load_gov_state()
        

        self.cardano_cli_conway("stake-address", "registration-certificate", 
                         ["--stake-verification-key-file", wallet.stake_vkey, "--key-reg-deposit-amt",
                          str(self.gov_state["currentPParams"]["stakeAddressDeposit"])
                          ,"--out-file", stake_cert], include_network=False, include_socket=False)
        
        submit_result:SubmitResult=self.build_and_submit(wallet,'drep_reg',
            ["--witness-override","2", 
                                "--certificate-file", stake_cert]
        ,raise_error=False,extra_keys=[wallet.stake_skey])


        # Sign and Submit the transaction
        process:subprocess.CompletedProcess = submit_result.process
        result:str=process.stdout
        if process.returncode != 0 :
            if "StakeKeyRegisteredDELEG" in process.stderr:
                print("Stake key was already registered ...")
                print("Nothing was done on-chain.")
            else:
                raise Exception("Process failed "+result + process.stderr)
        else:
            print(f"Stake registration transaction submitted successfully! Tx ID: {submit_result.txid}")


    def vote(self,vote,wallet:Wallet,key:Key,role:str,action_tx,action_tx_index):
        
        if(role=='drep'):
            key_arg="--drep-verification-key-file"
        elif role == "cc":
            key_arg="--cc-hot-verification-key-file"
        elif role == 'spo':
            key_arg="--cold-verification-key-file"
        vote_file=os.path.join(KEYS_DIR,"vote_"+vote+"_"+action_tx+'_'+action_tx_index+".vote")
        self.cardano_cli_conway("governance","vote",[
            
            "create",
            "--"+vote,
            "--governance-action-tx-id", action_tx,
            "--governance-action-index",action_tx_index,
            key_arg,key.public,
            "--out-file",vote_file
        ])
        
        result=self.build_and_submit(wallet,'vote'+"_"+action_tx+'_'+action_tx_index,[
            "--vote-file", vote_file,
            "--witness-override", "2"
        ],extra_keys=[key.private],raise_error=False)
        process=result.process
        if 'GovActionsDoNotExist' in process.stderr:
            print("ERROR: Gov Action doesn't exist on chain : ",action_tx+"#"+action_tx_index)
            print("Nothing was done on-chain")
        
    def register_drep(self, wallet: Wallet, drep: Key):
        drep_cert = os.path.join(KEYS_DIR, "drep_reg.cert")
        # Generate DRep registration certificate
        self.load_gov_state()
        
        # generate cert.        
        self.cardano_cli_conway("governance", "drep", 
                        [ "registration-certificate","--drep-verification-key-file", drep.public, "--key-reg-deposit-amt",
                        str(self.gov_state["currentPParams"]["dRepDeposit"])
                        ,"--out-file", drep_cert])
        
    
        submit_result:SubmitResult=self.build_and_submit(wallet,'drep_reg',
            ["--witness-override","2", 
            "--certificate-file", drep_cert]
            
        ,raise_error=False,extra_keys=[drep.private])

        # Sign and Submit the transaction

        if submit_result.process.returncode != 0 :
            if "ConwayDRepAlreadyRegistered" in submit_result.process.stderr:
                print("DRep key was already registered ...")
                print("Nothing was done on-chain.")
            else:
                raise Exception("Process failed "+submit_result.process.stdout + submit_result.process.stderr)
        else:
            print(f"DRep registration transaction submitted successfully!\nTx ID: {submit_result.txid}")
    
        

    def sign_and_submit(self,wallet:Wallet,tx_raw_file,signed_tx_file,raise_error=True,extra_keys=[])->Optional[SubmitResult]:
        # Sign the transaction
        extra_sigs=["--signing-key-file="+key_file for key_file in extra_keys]

        self.cardano_cli_conway("transaction", "sign", 
                         ["--tx-body-file", tx_raw_file, "--signing-key-file", wallet.payment_skey, 
                          "--out-file", signed_tx_file]+ extra_sigs
                         )
        result = self.cardano_cli_conway("transaction", "submit", ["--tx-file", signed_tx_file], include_network=True, include_socket=True,raise_error=raise_error)

        if not raise_error:
            return SubmitResult(result,self.get_tx_id(tx_raw_file))
        return self.get_tx_id(tx_raw_file)
    
    def delegate(self,wallet:Wallet,own_drep:Key,drep:str):
        delegation_cert = os.path.join(KEYS_DIR, "vote_deleg.cert")

        if drep == 'abstain':
            delegation=["--always-abstain"]
        elif drep == 'no-confidence' or drep == 'noconfidence':
            delegation=["--always-no-confidence"]
        elif drep == 'self':
            
            delegation=["--drep-key-hash",own_drep.id]
        else:
            wallet.stake_vkey
            delegation=["--drep-key-hash", drep]
            
        self.cardano_cli_conway('stake-address','vote-delegation-certificate',[
            "--stake-verification-key-file", wallet.stake_vkey
        ] + delegation + [
            "--out-file",
            delegation_cert
        ])
            
        result:SubmitResult=self.build_and_submit(wallet,'vote_deleg',
            ["--witness-override","2", 
            "--certificate-file", delegation_cert],extra_keys=[wallet.stake_skey],raise_error=False)
        process=result.process
        if(process.returncode!=0):
            if 'StakeKeyNotRegisteredDELEG' in process.stderr:
                print("ERROR: Drep is not registered:",drep)
            elif 'StakeKeyNotRegisteredDELEG' in process.stderr:
                print("Your stake key is not registered")
                print("run > gov-cli register stake")
                print("To register your stake")        
            else:
                raise Exception("Process failed "+process.stdout + process.stderr)
        else:
            print("Submitted :",result.txid)

    def cc_authorize_hot_key(self,wallet:Wallet,hot_key:Key,cold_key:Key):

        txid=self.build_and_submit(wallet,'cc_hot_key_register',[
            "--certificate-file",hot_key.id,
            "--witness-override","2"
        ],extra_keys=[cold_key.private])
        
        print("Submitted :",txid)


        
    def query_utxos(self, wallet: Wallet):
        utxos = self.cardano_cli("query", "utxo", ["--address", wallet.address], include_network=True, include_socket=True,)
        return utxos

    def query_utxos_json(self, wallet: Wallet):
        utxos = self.cardano_cli("query", "utxo", ["--address", wallet.address ,"--out-file","utxo.json"], include_network=True, include_socket=True,)
        with open("utxo.json") as f:
            utxos=json.load(f)
        return utxos


    def get_tx_id(self,tx_file):
        return self.cardano_cli("transaction","txid",["--tx-file",tx_file])


def main():
    if len(sys.argv) < 2:
        print("Usage: python cardano_cli.py <command> [options]")
        sys.exit(1)

    command = sys.argv[1]
    cli = CardanoCLI(network=NETWORK, socket_path=CARDANO_NODE_SOCKET_PATH)
    
    def vote(store:WalletStore,role):
        gov_action=sys.argv[3]
        vote= sys.argv[4] if len(sys.argv) >4 else 'yes'

        functions={
            'cc': store.load_cc_hot_keys,
            'drep':store.load_drep_key,
            'spo': store.load_drep_key
        }
        gov_action_split=gov_action.rsplit('#',1)
        
        key=functions[role]()
        cli.vote(vote,store.load_wallet(),key,role,gov_action_split[0],gov_action_split[1])
        
    
    if command == "gen":
        if len(sys.argv)>2:
            if sys.argv[2] == "drep":
                drep=WalletStore(KEYS_DIR).gen_drep_key(cli)
                print(f"Drep generated with key-hash : {drep.id}")
            elif sys.argv[2] == "cc":
                (hot,cold) = WalletStore(KEYS_DIR).gen_cc_keys(cli)
                print(f"Generated cold and hot keys")
                print(f"Generated CC keyHash : {hot.id}")
                print(f"You must issue \"register cc\" to register the hot keys")
            elif sys.argv[2] in ('wallet' or 'stake'):
                wallet = WalletStore(KEYS_DIR).gen_wallet(cli)
                print(f"New wallet generated with address: {wallet.address}")  
            else:
                print("Unexpected command for gen : Expected one of ",['wallet','drep','cc'] )

        else:
            # Generate new wallet
            wallet = WalletStore(KEYS_DIR).gen_wallet(cli)
            print(f"New wallet generated with address: {wallet.address}")
            print("=====================================")

            (hot,cold) = WalletStore(KEYS_DIR).gen_cc_keys(cli)
            print(f"Generated cold and hot keys")
            print(f"Generated CC keyHash : {hot.id}")
            print(f"You must issue \"register cc\" to register the hot keys")
            print("=====================================")
            
            drep = WalletStore(KEYS_DIR).gen_drep_key(cli)
            print(f"Drep generated with key-hash : {drep.id}")
        
    elif command == "wallet":
        store = WalletStore(KEYS_DIR)
        try:
            wallet = store.load_wallet()
            print(f"Address       : {wallet.address}")
        except:
            print(":: Wallet not generated > gov-cli gen wallet")

        try:
            wallet = store.load_drep_key()
            print(f"Drep Key Hash : {wallet.id}")
        except:
            print(":: Drep not generated > gov-cli gen drep")
            
        try:
            wallet = store.load_cc_cold_keys()
            print(f"CC key Hash   : {wallet.id}")
        except:
            print(":: CC keys not generated > gov-cli gen cc")
        

    elif command == "register":
        store=WalletStore(KEYS_DIR)
        wallet = store.load_wallet()
        if len(sys.argv)>2:
            if sys.argv[2] == "drep":
                drep=store.load_drep_key()
                cli.register_drep(wallet,drep)
                print(f"Drep ID : {drep.id}")
            elif sys.argv[2] == "stake":
               cli.register_stake(wallet)
            elif sys.argv[2] in ("cckeys","cc_keys","cc-keys","cc","cckey","cc_key","cc-key"):
                cli.cc_authorize_hot_key(wallet,store.load_cc_hot_keys(),store.load_cc_cold_keys())
                
            else:
                print("Invalid option for register \"" + sys.argv[2]+"\". Expected \"drep\" or \"stake\"")

        else:
            # Register stake key
            cli.register_stake(wallet)
    elif command == 'delegate':
        store=WalletStore(KEYS_DIR)
        wallet = store.load_wallet()
        drep= store.load_drep_key()
        if len(sys.argv) ==3:
            cli.delegate(wallet,drep,sys.argv[2])
        else:
            print("Usage:\n   gov-cli delegate [no-confidence|abstain|drep_id]")

    elif command == "propose":
        store=WalletStore(KEYS_DIR)
        other_args=sys.argv[2:]
        cli.propose(store.load_wallet(),other_args)

    elif command == 'drep' or command == 'cc' or command == 'spo' :
        store=WalletStore(KEYS_DIR)

        vote(store,command)
  
    elif command =='vote':
        store=WalletStore(KEYS_DIR)
        vote(store,sys.argv[2])
        
    elif command == "ls":
        if len(sys.argv) == 3:
            to_list=sys.argv[2]
            if to_list == 'drep':
                result=cli.cardano_cli_conway("query", "drep-state", ['--all-dreps'],include_network=True,include_socket=True)
                print(result)
        cli.load_gov_state()
        print(json.dumps(cli.gov_state['proposals'],indent=2))
        

    elif command == "balance":
        if len(sys.argv) == 2:
            with open(os.path.join(KEYS_DIR, "payment.addr")) as f:
                address=f.read().strip()
        elif len(sys.argv) == 3:
            address = sys.argv[2]
        else:
            print("Usage: python cardano_cli.py balance [address]")
            sys.exit(1)

        # Query UTXOs for the specified address
        print("queryutxo")
        wallet = Wallet(payment_vkey=None, payment_skey=None, stake_vkey=None, stake_skey=None, address=address)
        result=cli.query_utxos(wallet)
        print(result)
    elif command == "transfer":
        if len(sys.argv) != 5:
            print("Usage: python cardano_cli.py transfer <address> <value>")
            sys.exit(1)
        address = sys.argv[2]
        amount = sys.argv[3]
    elif command == "tip":
        result = cli.cardano_cli("query","tip",[],include_network=True,include_socket=True)
        print(result)
    elif command == 'guardrail':
        if len(sys.argv) ==4 and sys.argv[2] =='load':
            guardrail_script_file = os.path.join(KEYS_DIR, "guardrails-script.plutus")        
            shutil.copyfile(sys.argv[3], guardrail_script_file)
            print("Saved file :",guardrail_script_file)
        else:           
            print("Usage: python guardrail load <guardrail script file>")
    elif command == 'tx':
        p2 = sys.argv[2]
        if p2 =='help':
            result=cli.cardano_cli('transaction','build',['--help'])
            print(result)
        elif p2 =='contract' or p2== 'script':
            tx=cli.build_and_submit(WalletStore(KEYS_DIR).load_wallet(),'cli.tx',sys.argv[3:],add_collateral=True)
            print('Tx Submitted :',tx)
        else:
            tx=cli.build_and_submit(WalletStore(KEYS_DIR).load_wallet(),'cli.tx',sys.argv[2:])
            print('Tx Submitted :',tx)
            
    else:
        print("Unknown command")
        

if __name__ == "__main__":
    main()