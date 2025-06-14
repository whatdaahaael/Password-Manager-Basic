#Password Generator Project
import random
from CryptIt import letters, numbers, symbols

class GeneratePassword:
  def __init__(self, minletters=8, maxletters=10, minsym=2, maxsym=2, minnum=2, maxnum=2):
    self.nr_letters = random.randint(minletters, maxletters)
    self.nr_symbols = random.randint(minsym, maxsym)
    self.nr_numbers = random.randint(minnum, maxnum)

  def GetNewPass(self):
    password_list = []

    password_list += [random.choice(letters) for i in range(self.nr_letters)]
    password_list += [random.choice(symbols) for i in range(self.nr_symbols)]
    password_list += [random.choice(numbers) for i in range(self.nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)

    return password

