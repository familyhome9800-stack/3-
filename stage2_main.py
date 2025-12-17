import argparse

class UVMSpec:
    """Спецификация УВМ для варианта 26"""
    
    # Коды операций
    LOAD_CONST = 202    # 0xCA - Загрузка константы
    READ_MEM = 156      # 0x9C - Чтение из памяти
    WRITE_MEM = 93      # 0x5D - Запись в память
    SUB = 175           # 0xAF - Вычитание
    
    @staticmethod
    def encode_load_const(constant):
        """Кодирует команду LOAD константы - 4 байта"""
        a = UVMSpec.LOAD_CONST
        b = constant & 0xFFFFFF
        return [
            a & 0xFF,
            (b >> 16) & 0xFF,
            (b >> 8) & 0xFF,
            b & 0xFF
        ]
    
    @staticmethod
    def encode_read_mem(offset):
        """Кодирует команду READ из памяти - 3 байта"""
        a = UVMSpec.READ_MEM
        b = offset & 0xFFFF
        return [
            a & 0xFF,
            (b >> 8) & 0xFF,
            b & 0xFF
        ]
    
    @staticmethod
    def encode_write_mem(address):
        """Кодирует команду WRITE в память - 4 байта"""
        a = UVMSpec.WRITE_MEM
        b = address & 0xFFFFFF
        return [
            a & 0xFF,
            (b >> 16) & 0xFF,
            (b >> 8) & 0xFF,
            b & 0xFF
        ]
    
    @staticmethod
    def encode_sub(address):
        """Кодирует команду SUB (вычитание) - 4 байта"""
        a = UVMSpec.SUB
        b = address & 0xFFFFFF
        return [
            a & 0xFF,
            (b >> 16) & 0xFF,
            (b >> 8) & 0xFF,
            b & 0xFF
        ]

class Command:
    """Представление команды в промежуточном формате"""
    def __init__(self, mnemonic, args=None):
        self.mnemonic = mnemonic.upper()
        self.args = args or []
    
    def __repr__(self):
        return f"Command('{self.mnemonic}', {self.args})"

def parse_number(s):
    """Парсит число из строки (десятичное или шестнадцатеричное)"""
    s = str(s).strip()
    if s.startswith('0x'):
        # Шестнадцатеричное
        hex_str = s[2:].upper()
        result = 0
        for char in hex_str:
            if '0' <= char <= '9':
                result = result * 16 + (ord(char) - ord('0'))
            elif 'A' <= char <= 'F':
                result = result * 16 + (ord(char) - ord('A') + 10)
        return result
    # Десятичное
    return int(s)

def generate_machine_code(commands):
    """
    Транслятор из промежуточного в машинное представление
    Возвращает список байтов машинного кода
    """
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
    """
    Записывает результат ассемблирования в двоичный выходной файл
    Возвращает True если успешно, False если ошибка
    """
    try:
        with open(filename, 'wb') as f:
            for byte in machine_code:
                f.write(bytes([byte]))
        return True
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return False

def format_bytes_hex(machine_code):
    """Форматирует байты в hex строки как в спецификации УВМ"""
    return [f"0x{b:02X}" for b in machine_code]

def test_specification_sequences():
    """
    Проверяет соответствие тестовым байтовым последовательностям из спецификации УВМ
    Возвращает True если все тесты пройдены
    """
    print("=" * 60)
    print("ПРОВЕРКА ТЕСТОВЫХ БАЙТОВЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ")
    print("=" * 60)
    
    # Тестовые команды из спецификации (вариант 26)
    test_commands = [
        Command("LOAD", ["553"]),
        Command("READ", ["268"]),
        Command("WRITE", ["617"]),
        Command("SUB", ["455"])
    ]
    
    # Ожидаемые байтовые последовательности из спецификации
    expected_sequences = [
        [0xCA, 0x29, 0x02, 0x00],  # LOAD 553
        [0x9C, 0x0C, 0x01],        # READ 268
        [0x5D, 0x69, 0x02, 0x00],  # WRITE 617
        [0xAF, 0xC7, 0x01, 0x00]   # SUB 455
    ]
    
    all_passed = True
    
    # Проверяем каждую команду отдельно
    for i, (cmd, expected) in enumerate(zip(test_commands, expected_sequences)):
        # Генерируем машинный код для одной команды
        generated = generate_machine_code([cmd])
        
        # Форматируем для вывода
        cmd_str = f"{cmd.mnemonic} {cmd.args[0]}"
        expected_hex = format_bytes_hex(expected)
        generated_hex = format_bytes_hex(generated)
        
        passed = generated == expected
        
        print(f"\nТест {i+1}: {cmd_str}")
        print(f"  Ожидается: {' '.join(expected_hex)}")
        print(f"  Получено:  {' '.join(generated_hex)}")
        print(f"  Результат: {'✓ ПРОЙДЕНО' if passed else '✗ ОШИБКА'}")
        
        all_passed = all_passed and passed
    
    # Проверяем всю программу целиком
    print("\n" + "-" * 60)
    print("Проверка полной программы:")
    
    full_program_code = generate_machine_code(test_commands)
    expected_full = []
    for seq in expected_sequences:
        expected_full.extend(seq)
    
    full_passed = full_program_code == expected_full
    print(f"  Полная программа: {'✓ СОВПАДАЕТ' if full_passed else '✗ НЕ СОВПАДАЕТ'}")
    
    print("\n" + "=" * 60)
    if all_passed and full_passed:
        print("✓ ВСЕ ТЕСТЫ ИЗ СПЕЦИФИКАЦИИ ПРОЙДЕНЫ")
    else:
        print("✗ ЕСТЬ ОШИБКИ В ТЕСТАХ")
    
    return all_passed and full_passed, test_commands

def create_test_asm_file():
    """
    Создает файл на языке ассемблера, результат трансляции которого
    соответствует всем тестовым байтовым последовательностям из спецификации УВМ
    """
    content = 
    
    try:
        with open("test_spec.asm", "w", encoding="utf-8") as f:
            f.write(content)
        print("✓ Создан файл 'test_spec.asm' с тестовой программой")
        return True
    except Exception as e:
        print(f"✗ Ошибка при создании файла: {e}")
        return False

def parse_intermediate_file(filename):

    commands = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith(';'):
                    parts = line.split()
                    if parts:
                        mnemonic = parts[0]
                        args = parts[1:] if len(parts) > 1 else []
                        commands.append(Command(mnemonic, args))
        return commands
    except FileNotFoundError:
        print(f"✗ Файл '{filename}' не найден")
        return None
    except Exception as e:
        print(f"✗ Ошибка при чтении файла: {e}")
        return None

def main():
    """Главная функция CLI приложения"""
    parser = argparse.ArgumentParser(
        description='Ассемблер УВМ - Этап 2: Формирование машинного кода',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""

    )
    
    parser.add_argument(
        'input_file',
        nargs='?',
        help='Файл с промежуточным представлением команд'
    )
    
    parser.add_argument(
        'output_file',
        nargs='?',
        help='Двоичный файл для сохранения машинного кода'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Режим тестирования (вывод байтового формата)'
    )
    
    parser.add_argument(
        '--create-test',
        action='store_true',
        help='Создать тестовый ASM файл для проверки спецификации'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("АССЕМБЛЕР УВМ - ЭТАП 2: ФОРМИРОВАНИЕ МАШИННОГО КОДА")
    print("=" * 60)
    
    if args.create_test:
        # Создание тестового файла
        create_test_asm_file()
        print("\nДля проверки созданного файла:")
        print("1. Запустите этап 1: python stage1_main.py test_spec.asm")
        print("2. Сохраните промежуточное представление")
        print("3. Запустите этап 2 с полученным файлом")
    
    elif not args.input_file or not args.output_file:
        # Проверка спецификации если не указаны файлы
        print("\nПРОВЕРКА СПЕЦИФИКАЦИИ УВМ")
        test_passed, _ = test_specification_sequences()
        
        if test_passed:
            print("\nДля использования ассемблера:")
            print("  python stage2_main.py <входной_файл> <выходной_файл>")
            print("\nПример промежуточного файла (commands.txt):")
            print("  LOAD 553")
            print("  READ 268")
            print("  WRITE 617")
            print("  SUB 455")
        else:
            print("\n✗ Ассемблер не соответствует спецификации!")
    
    else:
        # Основной режим: трансляция промежуточного представления
        print(f"\nТРАНСЛЯЦИЯ ПРОМЕЖУТОЧНОГО ПРЕДСТАВЛЕНИЯ")
        print(f"Входной файл:  {args.input_file}")
        print(f"Выходной файл: {args.output_file}")
        print("-" * 60)
        
        # Чтение промежуточного представления
        commands = parse_intermediate_file(args.input_file)
        if commands is None:
            return
        
        print(f"Прочитано команд: {len(commands)}")
        
        # Генерация машинного кода
        machine_code = generate_machine_code(commands)
        
        if not machine_code:
            print("✗ Не удалось сгенерировать машинный код")
            return
        
        # Сохранение в двоичный файл
        if save_binary_file(machine_code, args.output_file):
            print(f"✓ Машинный код сохранен в: {args.output_file}")
        
        # Вывод размера файла в байтах
        print(f"✓ Размер двоичного файла: {len(machine_code)} байт")
        
        if args.test:
            # Режим тестирования: вывод байтового формата
            print("\n" + "=" * 60)
            print("РЕЖИМ ТЕСТИРОВАНИЯ - БАЙТОВОЕ ПРЕДСТАВЛЕНИЕ")
            print("=" * 60)
            
            hex_bytes = format_bytes_hex(machine_code)
            
            # Выводим как в спецификации УВМ
            print("Сгенерированные байты:")
            for i in range(0, len(hex_bytes), 8):
                line_bytes = hex_bytes[i:i+8]
                print("  " + " ".join(line_bytes))
            
            # Проверка соответствия спецификации
            print("\n" + "-" * 60)
            print("ПРОВЕРКА СООТВЕТСТВИЯ СПЕЦИФИКАЦИИ:")
            test_specification_sequences()
        
        print("\n" + "=" * 60)
        print("ЭТАП 2 ВЫПОЛНЕН УСПЕШНО")
        print("=" * 60)

if __name__ == "__main__":
    main()
