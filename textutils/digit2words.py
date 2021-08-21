from enum import Enum, auto


class Currency(Enum):
    MX = auto()
    US = auto()
    CA = auto()
    RU = auto()
    EU = auto()
    JP = auto()


currencies = {
    Currency.MX: ("＄", "pesos", "M. N."),
    Currency.US: ("＄", "dólares americanos", "US Dollar"),
    Currency.CA: ("C＄", "dólares canadienses", "CA Dollar"),
    Currency.EU: ("€", "euros", "€"),
    Currency.RU: ("₽", "rublos rusos", "RU Ruble"),
    Currency.JP: ("¥", "yen japónes", "JP Yen"),
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
hundreds = {
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
    10: "mil ",
}


def digit_triplets(num: str) -> str:
    num = int(num)
    h, r = divmod(num, 100)
    # Decode hundreds
    result = hundreds[h]
    if r == 0:
        return result
    if h == 1:
        result += "to "
    elif h != 0:
        result += " "
    # Decode tens and units
    if 1 <= r < 30:
        result += digits[r] + " "
    else:
        t, r = divmod(r, 10)
        result += tens[t] + f" y {digits[r]} " if r else " "
    return result


def convert(num: str):
    triplet = 3
    result = ""
    # Condition the input by removing possible commas and possible decimals
    quantity = num.replace(",", "").split(".")[0]
    n_digits = len(quantity)
    # Reverse the input and decode from least significant to most significant
    g_digits = quantity[::-1]
    g_digits = [(g_digits[i:i + triplet]) for i in range(0, n_digits, triplet)]
    g_digits = [q[::-1] for q in g_digits]
    last_loop = len(g_digits)
    for i, g in enumerate(g_digits, start=1):
        partial = digit_triplets(g) + exponent_counter[i]
        # Remove the phrase 'un mil ' and leave just 'mil '
        if partial == "un mil ":
            partial = "mil "
        # Convert plural into singular only when the most significant number is 1
        if i == last_loop and partial.startswith("un") and partial.endswith("llones "):
            partial = partial[:-5]
            partial += "ón "
        # Accumulate partial results
        result = partial + result
    # Return capitalized result
    return result.capitalize()


class Digit2Word:
    """ Converts any quantity into its equivalent phrase (Spanish)"""
    def __init__(self, num: str, currency: Currency = Currency.MX):
        self.currency_symbol = currencies[currency][0]
        self.currency_descriptor = currencies[currency][1]
        self.currency_ending = currencies[currency][2]
        entry = num.replace(",", "").split(".")
        self.value = entry[0]
        try:
            self.cents = str(int(round(int(entry[1])/10**(len(entry[1])-1), 1)*10))
        except IndexError as e:
            self.cents = "00"

    @classmethod
    def from_float(cls, num: float):
        return cls(str(num))

    def __str__(self):
        return f"{convert(self.value)}{self.currency_descriptor} {self.cents}/100 {self.currency_ending}"


def main() -> None:
    d2w = Digit2Word("49,231,234.4358", Currency.JP)
    print(str(d2w))


if __name__ == "__main__":
    main()
