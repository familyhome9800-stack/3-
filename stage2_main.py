from uvm_spec import UVMSpec

class Command:
    """Простой класс команды для этапа 2"""
    def __init__(self, mnemonic, args=None):
        self.mnemonic = mnemonic
        self.args = args or []
    
    def __repr__(self):
        return f"Command({self.mnemonic}, {self.args})"

class UVMSpec:
    # Коды операций для варианта 26
    LOAD_CONST = 202    # 0xCA
    READ_MEM = 156      # 0x9C
    WRITE_MEM = 93      # 0x5D
    SUB = 175           # 0xAF
    
    @staticmethod
    def encode_load_const(constant):
        """Кодирует команду LOAD константы"""
        # A=202 (8 бит), B=constant (24 бита)
        a = UVMSpec.LOAD_CONST
        b = constant & 0xFFFFFF
        
        return [
            a & 0xFF,           # Байт 0: код операции
            (b >> 16) & 0xFF,   # Байт 1: старшие 8 бит константы
            (b >> 8) & 0xFF,    # Байт 2: средние 8 бит константы  
            b & 0xFF            # Байт 3: младшие 8 бит константы
        ]
    
    @staticmethod
    def encode_read_mem(offset):
        """Кодирует команду READ из памяти"""
        # A=156 (8 бит), B=offset (16 бит)
        a = UVMSpec.READ_MEM
        b = offset & 0xFFFF
        
        return [
            a & 0xFF,        # Байт 0: код операции
            (b >> 8) & 0xFF, # Байт 1: старшие 8 бит смещения
            b & 0xFF         # Байт 2: младшие 8 бит смещения
        ]
    
    @staticmethod
    def encode_write_mem(address):
        """Кодирует команду WRITE в память"""
        # A=93 (8 бит), B=address (24 бита)
        a = UVMSpec.WRITE_MEM
        b = address & 0xFFFFFF
        
        return [
            a & 0xFF,           # Байт 0: код операции
            (b >> 16) & 0xFF,   # Байт 1: старшие 8 бит адреса
            (b >> 8) & 0xFF,    # Байт 2: средние 8 бит адреса
            b & 0xFF            # Байт 3: младшие 8 бит адреса
        ]
    
    @staticmethod
    def encode_sub(address):
        """Кодирует команду SUB (вычитание)"""
        # A=175 (8 бит), B=address (24 бита)
        a = UVMSpec.SUB
        b = address & 0xFFFFFF
        
        return [
            a & 0xFF,           # Байт 0: код операции
            (b >> 16) & 0xFF,   # Байт 1: старшие 8 бит адреса
            (b >> 8) & 0xFF,    # Байт 2: средние 8 бит адреса
            b & 0xFF            # Байт 3: младшие 8 бит адреса
        ]

class Command:
    """Простой класс команды для этапа 2"""
    def __init__(self, mnemonic, args=None):
        self.mnemonic = mnemonic
        self.args = args or []
    
    def __repr__(self):
        return f"Command({self.mnemonic}, {self.args})"

def parse_number(s):
    """Парсит число из строки"""
    s = str(s).strip()
    if s.startswith('0x'):
        # hex to int
        hex_str = s[2:].upper()
        result = 0
        for char in hex_str:
            if '0' <= char <= '9':
                result = result * 16 + (ord(char) - ord('0'))
            elif 'A' <= char <= 'F':
                result = result * 16 + (ord(char) - ord('A') + 10)
        return result
    return int(s)

def generate_machine_code(commands):
    """Генерирует машинный код из списка команд"""
    machine_code = []
    
    for cmd in commands:
        if cmd.mnemonic == "LOAD":
            if len(cmd.args) == 1:
                constant = parse_number(cmd.args[0])
                machine_code.extend(UVMSpec.encode_load_const(constant))
        
        elif cmd.mnemonic == "READ":
            if len(cmd.args) == 1:
                offset = parse_number(cmd.args[0])
                machine_code.extend(UVMSpec.encode_read_mem(offset))
        
        elif cmd.mnemonic == "WRITE":
            if len(cmd.args) == 1:
                address = parse_number(cmd.args[0])
                machine_code.extend(UVMSpec.encode_write_mem(address))
        
        elif cmd.mnemonic == "SUB":
            if len(cmd.args) == 1:
                address = parse_number(cmd.args[0])
                machine_code.extend(UVMSpec.encode_sub(address))
    
    return machine_code

def save_binary_file(machine_code, filename):
    """Сохраняет машинный код в бинарный файл"""
    try:
        with open(filename, 'wb') as f:
            for byte in machine_code:
                f.write(bytes([byte]))
        return True
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return False

def test_specification():
    """Проверяет тестовые байтовые последовательности из спецификации"""
    print("\nТестовые байтовые последовательности из спецификации УВМ:")
    print("-" * 60)
    
    # Тестовые команды
    test_commands = [
        Command("LOAD", ["553"]),
        Command("READ", ["268"]),
        Command("WRITE", ["617"]),
        Command("SUB", ["455"])
    ]
    
    expected_results = [
        [0xCA, 0x29, 0x02, 0x00],
        [0x9C, 0x0C, 0x01],
        [0x5D, 0x69, 0x02, 0x00],
        [0xAF, 0xC7, 0x01, 0x00]
    ]
    
    all_passed = True
    for cmd, expected in zip(test_commands, expected_results):
        # Генерируем код для одной команды
        generated = generate_machine_code([cmd])
        
        # Форматируем вывод
        cmd_str = f"{cmd.mnemonic} {cmd.args[0]}"
        expected_hex = [f"0x{b:02X}" for b in expected]
        generated_hex = [f"0x{b:02X}" for b in generated]
        
        passed = generated == expected
        
        print(f"Тест: {cmd_str}")
        print(f"  Ожидается: {' '.join(expected_hex)}")
        print(f"  Получено:  {' '.join(generated_hex)}")
        print(f"  Статус: {'ПРОЙДЕНО' if passed else 'ОШИБКА'}")
        print()
        
        all_passed = all_passed and passed
    
    return all_passed, test_commands

def create_test_asm_file():
    """Создает тестовый ASM файл с тестовыми командами"""
    content = """; Тестовый файл для проверки спецификации УВМ
; Этот файл генерирует тестовые байтовые последовательности

LOAD 553      ; 0xCA 0x29 0x02 0x00
READ 268      ; 0x9C 0x0C 0x01
WRITE 617     ; 0x5D 0x69 0x02 0x00
SUB 455       ; 0xAF 0xC7 0x01 0x00"""
    
    try:
        with open("test_spec.asm", "w", encoding="utf-8") as f:
            f.write(content)
        print("Создан файл test_spec.asm с тестовой программой")
        return True
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Ассемблер УВМ - Этап 2: Формирование машинного кода',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python stage2_main.py --spec-test                 # Проверить спецификацию
  python stage2_main.py --create-test              # Создать тестовый файл
  python stage2_main.py test_output.bin --test     # Создать тестовую программу
        """
    )
    
    parser.add_argument(
        'output_file',
        nargs='?',
        help='Путь к двоичному файлу-результату'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Режим тестирования (создать тестовую программу)'
    )
    
    parser.add_argument(
        '--spec-test',
        action='store_true',
        help='Проверить тестовые байтовые последовательности из спецификации'
    )
    
    parser.add_argument(
        '--create-test',
        action='store_true',
        help='Создать тестовый ASM файл с примерами из спецификации'
    )
    
    args = parser.parse_args()
    
    print("АССЕМБЛЕР УЧЕБНОЙ ВИРТУАЛЬНОЙ МАШИНЫ (УВМ)")
    print("Этап 2: Формирование машинного кода")
    print("=" * 60)
    
    if args.spec_test:
        # Проверка тестовых последовательностей
        all_passed, test_commands = test_specification()
        if all_passed:
            print("✓ Все тесты из спецификации пройдены!")
    
    elif args.create_test:
        # Создание тестового ASM файла
        create_test_asm_file()
    
    elif args.test and args.output_file:
        # Создание тестовой программы и сохранение в файл
        print("Создание тестовой программы...")
        
        # Тестовые команды из спецификации
        test_commands = [
            Command("LOAD", ["553"]),
            Command("READ", ["268"]),
            Command("WRITE", ["617"]),
            Command("SUB", ["455"])
        ]
        
        # Генерируем машинный код
        machine_code = generate_machine_code(test_commands)
        
        # Сохраняем в файл
        if save_binary_file(machine_code, args.output_file):
            print(f"✓ Тестовая программа сохранена в: {args.output_file}")
            print(f"  Размер файла: {len(machine_code)} байт")
        
        # Выводим байты в режиме тестирования
        print("\nБайтовое представление (как в спецификации):")
        print("-" * 60)
        hex_bytes = [f"0x{b:02X}" for b in machine_code]
        
        # Выводим по 8 байт в строке
        for i in range(0, len(hex_bytes), 8):
            line_bytes = hex_bytes[i:i+8]
            print(" ".join(line_bytes))
        
        # Проверяем спецификацию
        print("\n" + "=" * 60)
        print("Проверка соответствия спецификации:")
        all_passed, _ = test_specification()
        if all_passed:
            print("✓ Программа соответствует тестовым последовательностям из спецификации!")
    
    else:
        parser.print_help()
        
        print("\n" + "=" * 60)
        print("Для проверки спецификации:")
        print("  python stage2_main.py --spec-test")
        print("\nДля создания тестовой программы:")
        print("  python stage2_main.py test_output.bin --test")
        print("\nДля создания тестового ASM файла:")
        print("  python stage2_main.py --create-test")

if __name__ == "__main__":
    main()
