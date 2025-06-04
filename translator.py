# coding: utf-8

def load_mapping(filename="base.txt"):
    mapping = {}
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or '-' not in line:
                continue
            latin, cyrillic = line.split('-', 1)
            mapping[latin] = cyrillic
    return mapping

def translate(text, mapping):
    result = []
    for char in text:
        if char in mapping:
            result.append(mapping[char])
        elif char.lower() in mapping and char.isalpha():
            mapped = mapping[char.lower()]
            result.append(mapped.upper() if char.isupper() else mapped)
        else:
            result.append(char)
    return ''.join(result)

if __name__ == "__main__":
    mapping = load_mapping()
    input_text = input("Введите текст на английской раскладке: ")
    print("Результат:", translate(input_text, mapping))
