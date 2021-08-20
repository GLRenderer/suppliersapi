import decimal
from math import ceil
from enum import Enum, auto


class Currency(Enum):
    MX = auto()
    US = auto()
    CA = auto()
    RU = auto()
    EU = auto()


class Digit2Word:
    """ Converts any quantity into its equivalent phrase (Spanish)"""
    currencies = {
        Currency.MX: ("pesos", "M. N."),
        Currency.US: ("dolares americanos", "US Dollar"),
        Currency.CA: ("dolares canadienses", "CA Dollar"),
        Currency.EU: ("euros", "(E)"),
        Currency.RU: ("rublos rusos", "RU Ruble")
    }

    digits = {
        0: "cero",
        1: "un",
        2: "dos",
        3: "tres",
        4: "cuatro",
        5: "cinco",
        6: "séis",
        7: "siete",
        8: "ocho",
        9: "nueve",
        10: "diez",
        11: "once",
        12: "doce",
        13: "trece",
        15: "quince",
        16: "dieciséis",
        17: "diecisiete",
        18: "dieciocho",
        19: "diecinueve",
        20: "veinte",
        21: "veintiún",
        22: "veintidos",
        23: "veintitres",
        24: "veinticuatro",
        25: "veinticinco",
        26: "vientiséis",
        27: "vientisiete",
        28: "vientiocho",
        29: "vientinueve",
    }
    tens = {
        3: "treinta",
        4: "cuarenta",
        5: "cincuenta",
        6: "sesenta",
        7: "setenta",
        8: "ochenta",
        9: "noventa",
    }
    hunds = {
        0: "",
        1: "cien",
        2: "doscientos",
        3: "trescientos",
        4: "cuatrocientos",
        5: "quinientos",
        6: "seiscientos",
        7: "setecientos",
        8: "ochocientos",
        9: "novecientos",
    }
    exponent_counter = {
        1: "",
        2: "mil ",
        3: "millones ",
        4: "mil ",
        5: "billones ",
        6: "mil ",
        7: "trillones ",
        8: "mil ",
        9: "cuatrillones ",
    }

    @staticmethod
    def hundreds(num: str) -> str:
        num = int(num)
        h, r = divmod(num, 100)
        result = Digit2Word.hunds[h]
        if r == 0:
            return result
        if h == 1:
            result += "to "
        elif h != 0:
            result += " "

        if 1 <= r < 30:
            result += Digit2Word.digits[r] + " "
        else:
            t, r = divmod(r, 10)
            result += Digit2Word.tens[t] + f" y {Digit2Word.digits[r]} " if r else " "
        return result

    @staticmethod
    def convert(num: str):
        constN = 3
        result = ""
        quantity = num
        n_digits = len(quantity)
        groups = int(ceil(n_digits/3.0))
        g_digits = quantity[::-1]
        g_digits = [(g_digits[i:i + constN]) for i in range(0, n_digits, constN)]
        g_digits = [q[::-1] for q in g_digits]
        for i, g in enumerate(g_digits, start=1):
            partial = Digit2Word.hundreds(g) + Digit2Word.exponent_counter[i]
            if partial == "un mil ":
                partial = "mil "
            if i == 3 and partial == "un millones ":
                partial = partial[:-5]
                partial += "ón "
            # if i == 4 and partial == "un mil millones ":
            #     partial = "mil millones "
            if i == 5 and partial == "un billones ":
                partial = partial[:-5]
                partial += "ón "
            if i == 6 and partial == "un trillones ":
                partial = partial[:-5]
                partial += "ón "
            if i == 9 and partial == "un cuatrillones ":
                partial = partial[:-5]
                partial += "ón "
            result = partial + result
        return result

    def __init__(self, num: str, currency: Currency = Currency.MX):
        self.currency = currency
        self.currency_descriptor = self.currencies[self.currency][0]
        self.currency_ending = self.currencies[self.currency][1]
        entry = num.split(".")
        self.value = entry[0]
        if len(entry) > 1:
            self.cents = entry[1]
        else:
            self.cents = "00"

    @classmethod
    def from_float(cls, num: float):
        entry = str(decimal.Decimal.from_float(num))
        # if len(entry > 2):
        #     raise ValueError("Invalid entry! Value represent a float")
        # if not entry[0].isdigit() or not entry[1].isdigit():
        #     raise ValueError("String does not represent a float value")
        # num = float(num)
        return cls(entry)

    def __str__(self):
        return f"{Digit2Word.convert(self.value)}{self.currency_descriptor} {self.cents}/100 {self.currency_ending}"


def main() -> None:
    d2w = Digit2Word("981234.42")
    print(str(d2w))

if __name__ == "__main__":
    main()
