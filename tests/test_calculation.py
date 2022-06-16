from app.calculation import add, Bank, InsuficentBalance
import pytest


@pytest.fixture
def zero_bank():
    return Bank()


@pytest.fixture
def bank():
    return Bank(50)


@pytest.mark.parametrize("num1, num2, result", [(2, 3, 5), (6, 4, 10), (14, 18, 32)])
def test_add(num1, num2, result):
    assert add(num1, num2) == result


def test_bank_initial_balance(bank):
    assert bank.balance == 50


def test_bank_default_balance(zero_bank):
    assert zero_bank.balance == 0


def test_bank_deposite(bank):
    bank.deposite(30)
    assert bank.balance == 80


def test_bank_withdraw(bank):
    bank.withdraw(20)
    assert bank.balance == 30


def test_bank_interest(bank):
    bank.collect_interest()
    assert round(bank.balance, 4) == 55


@pytest.mark.parametrize(
    "deposited, withdrew, result", [(200, 100, 100), (50, 10, 40), (1200, 200, 1000)]
)
def test_bank_transaction(zero_bank, deposited, withdrew, result):
    zero_bank.deposite(deposited)
    zero_bank.withdraw(withdrew)
    assert zero_bank.balance == result


def test_insuficent_fund(bank):
    with pytest.raises(Exception):
        bank.withdraw(100)
