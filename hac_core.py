# Простой пример "сжатия" — инверсия текста (заглушка HAC)
def hac_compress(text: str) -> str:
    return text[::-1]

def hac_decompress(text: str) -> str:
    return text[::-1]
