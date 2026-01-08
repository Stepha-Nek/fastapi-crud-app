import pytest
from app.calculations import add, subtract, multiply, divide,BankAccount, InsufficientFunds  #importing the add function from calculations.py file


#fixtures, FUNCTIONS THAT RETURN DATA, can be used in multiple tests, to avoid code duplication
@pytest.fixture
def zero_bank_account():
    print("creating empty bank account")
    return BankAccount()  #so you have a bank account with 0 balance


@pytest.fixture
def bank_account():
    return BankAccount(50)#bank account with initial balance of 50




@pytest.mark.parametrize("num1, num2, expected", [#cam also use x,y and result instead of num1, num2, expected
    (2, 3, 5),
    (5, 3, 8),
    (4, 10, 14),
])
def test_add(num1, num2, expected):

    assert add(num1, num2) == expected #checking if the sum is equal to 5, if true test passes, if false test fails, and you will see an error


def test_subtract():
    print("testing subtract function")

    assert subtract(5, 3) == 2

def test_multiply():
    print("testing multiply function")

    assert multiply(2, 3) == 6

def test_divide():
    print("testing divide function")

    assert divide(6, 3) == 2.0

    #BANK ACCOUNT TESTS


def test_bank_set_initial_amount(bank_account):

    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    print("testing my bank account")
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):

    bank_account.withdraw(20) #testing the bank account balamce if 20 was withdrawn, in the fixture, the bank balance is given as 50
    assert bank_account.balance == 30


def test_deposit(bank_account):

    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_collect_interest(bank_account):

    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

    #instead of writing multiple tests for different transactions, we can use parametrize to do it in one test


@pytest.mark.parametrize("deposited, withdrew, expected", [ 
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)

])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds): #tellling pytest to expect an exception, so it wont fail, it will pass, cos an exception will cause the code to fail
        bank_account.withdraw(200) #the error has to be defined, the insufficient funds error is a type of exception, if another type of exception was defined in the calculations.py and another is used in the test, failure is expected