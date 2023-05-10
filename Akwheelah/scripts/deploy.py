from brownie import AlgaeInsurance, accounts, network
from web3 import Web3

account = accounts[0]
buyer = accounts[1]
premium = 1000000000000000000 # 1 ETH
payout = 10000000000000000000 # 10 ETH
initialBal = 100000000000000000000 # 100 ETH contract starting balance (for le payouts)
algaeThreshold = 50 # 50 bajillion algae or something like that mang hyuehyuehyue

# owner deploys insurance contract with 100 ETH starting balance
algae1 = AlgaeInsurance.deploy(premium, payout, algaeThreshold, {"from": account, "amount": initialBal})

# buyer purchases insurance protection
algae1.buyPolicy({"from": buyer, "amount": premium})

# setting test values for algae threshold payout and measured algae oracle response
algae1.testContractWith(69, 420, {"from": account})

# check for payout bool
algae1.checkAlgaeBloom({"from": account})

