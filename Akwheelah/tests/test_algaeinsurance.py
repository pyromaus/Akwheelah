from brownie import AlgaeInsurance, accounts, network, exceptions
import brownie
from web3 import Web3
import pytest


def test_constructor():
    owner = accounts[0]
    premium = 1000000000000000000  # 1 ETH
    payout = 10000000000000000000  # 10 ETH
    initialBal = (
        15000000000000000000  # 15 ETH contract starting balance (for le payouts)
    )
    algaeThreshold = 50  # 50 bajillion algae or something like that mang hyuehyuehyue

    # owner deploys insurance contract with 100 ETH starting balance
    algae1 = AlgaeInsurance.deploy(
        premium, payout, algaeThreshold, {"from": owner, "amount": initialBal}
    )

    assert algae1.premium() == premium
    assert algae1.payout() == payout
    assert algae1.threshold() == algaeThreshold
    assert algae1.policyActive() == True
    assert algae1.bloom() == False


def test_buy_policy():
    owner = accounts[0]
    buyer = accounts[1]
    premium = 1000000000000000000
    payout = 10000000000000000000
    initialBal = 15000000000000000000
    algaeThreshold = 50

    # deploying again
    algae1 = AlgaeInsurance.deploy(
        premium, payout, algaeThreshold, {"from": owner, "amount": initialBal}
    )

    # buyer purchases insurance protection
    tx = algae1.buyPolicy({"from": buyer, "amount": premium})

    policy_holder1 = algae1.getPolicyholderByIndex(0)
    assert buyer.address == policy_holder1

    policy_balance = algae1.getPolicyBalance(policy_holder1)
    assert premium == policy_balance
    assert premium == tx.value


def test_contract_with_function():
    owner = accounts[0]
    premium = 1000000000000000000
    payout = 10000000000000000000
    initialBal = 15000000000000000000
    algaeThreshold = 50

    # deploying 1ce again
    algae1 = AlgaeInsurance.deploy(
        premium, payout, algaeThreshold, {"from": owner, "amount": initialBal}
    )

    # setting test values for algae threshold payout and measured algae oracle response
    test_threshold = 69
    test_measurement = 420
    algae1.testContractWith(69, 420, {"from": owner})
    assert test_threshold == algae1.threshold()
    assert test_measurement == algae1.measuredAlgae()


def test_check_bloom():
    owner = accounts[0]
    buyer = accounts[1]
    premium = 1000000000000000000
    payout = 10000000000000000000
    initialBal = 15000000000000000000
    algaeThreshold = 50

    # deployin
    algae1 = AlgaeInsurance.deploy(
        premium, payout, algaeThreshold, {"from": owner, "amount": initialBal}
    )

    # homie buys the thing
    algae1.buyPolicy({"from": buyer, "amount": premium})

    # set test values for a negative bool
    algae1.testContractWith(69, 33, {"from": owner})

    # check bloom bby
    algae1.checkAlgaeBloom({"from": owner})
    assert algae1.bloom() == False
    assert algae1.policyActive() == True

    # set test values for a positive bool; get buyer balance before payout
    algae1.testContractWith(69, 420, {"from": owner})
    before_balance = buyer.balance()

    # check bloomz + if buyer got paid
    algae1.checkAlgaeBloom({"from": owner})
    after_balance = buyer.balance()
    assert algae1.bloom() == True
    assert algae1.policyActive() == False
    assert after_balance - before_balance == payout

    # try to buy an unactive policy
    # with brownie.reverts():
    #     algae1.buyPolicy({"from": buyer, "amount": premium})


def test_close_policy():
    owner = accounts[0]
    buyer = accounts[1]
    premium = 1000000000000000000
    payout = 10000000000000000000
    initialBal = 15000000000000000000
    algaeThreshold = 50

    # deploy
    algae1 = AlgaeInsurance.deploy(
        premium, payout, algaeThreshold, {"from": owner, "amount": initialBal}
    )

    # anxious buyer wants peace of mind
    algae1.buyPolicy({"from": buyer, "amount": premium})
    before_balance = buyer.balance()

    # buyer tries to close policy himself, phails
    # with brownie.reverts():
    #     algae1.closePolicy({"from": buyer})

    # close policy and compare buyer balances
    algae1.closePolicy({"from": owner})
    after_balance = buyer.balance()
    assert after_balance - before_balance == premium

    # policy holder balance set to 0
    assert algae1.getPolicyBalance(buyer.address) == 0


def test_deposit_funds():
    owner = accounts[0]
    daddy = accounts[3]
    premium = 1000000000000000000
    payout = 10000000000000000000
    initialBal = 15000000000000000000
    algaeThreshold = 50

    # deployrreeeeeEEEEEEEEE
    algae1 = AlgaeInsurance.deploy(
        premium, payout, algaeThreshold, {"from": owner, "amount": initialBal}
    )
    contract_before_bal = algae1.balance()

    # kerrazy tehsts m8
    funds_from_daddy = algae1.depositFunds({"from": daddy, "amount": premium})
    contract_after_bal = algae1.balance()

    assert funds_from_daddy.value == contract_after_bal - contract_before_bal
    assert funds_from_daddy.value == premium
    assert premium == contract_after_bal - contract_before_bal
    assert funds_from_daddy.receiver == algae1.address


def test_activate_policy():
    owner = accounts[0]
    buyer = accounts[1]
    premium = 1000000000000000000
    payout = 10000000000000000000
    initialBal = 15000000000000000000
    algaeThreshold = 50

    # how many times we gonna deploy, brownie??
    algae1 = AlgaeInsurance.deploy(
        premium, payout, algaeThreshold, {"from": owner, "amount": initialBal}
    )

    # get a payout to deactivate the policy
    algae1.buyPolicy({"from": buyer, "amount": premium})
    algae1.testContractWith(69, 420, {"from": owner})
    algae1.checkAlgaeBloom({"from": owner})

    # buyer tries to buy another policy and activate it too. what a schmuck
    # with brownie.reverts():
    #     algae1.buyPolicy({"from": buyer, "amount": premium})
    assert algae1.policyActive() == False
    assert algae1.bloom() == True
    # with brownie.reverts():
    #     algae1.activatePolicy({"from": buyer})

    # owner re-activates the policy
    algae1.activatePolicy({"from": owner})
    assert algae1.policyActive() == True
    assert algae1.bloom() == False
