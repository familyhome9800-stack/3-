from asm_parser import Assembler, read_program_file
from uvm_spec import UVMSpec

class CodeGenerator:
    def __init__(self):
        self.assembler = Assembler()
    
    def generate_machine_code(self, source_code):
        """Генерирует машинный код из исходного кода"""
        commands = self.assembler.assemble(source_code)
        machine_code = []
        
        for cmd in commands:
            if cmd.mnemonic == "LOAD":
                if len(cmd.args) == 1:
                    constant = self.assembler.parse_number(cmd.args[0])
                    machine_code.extend(UVMSpec.encode_load_const(constant))
                else:
                    print(f"Ошибка: команда LOAD требует 1 аргумент, получено {len(cmd.args)}")
            
            elif cmd.mnemonic == "READ":
                if len(cmd.args) == 1:
                    offset = self.assembler.parse_number(cmd.args[0])
                    machine_code.extend(UVMSpec.encode_read_mem(offset))
                else:
                    print(f"Ошибка: команда READ требует 1 аргумент, получено {len(cmd.args)}")
            
            elif cmd.mnemonic == "WRITE":
                if len(cmd.args) == 1:
                    address = self.assembler.parse_number(cmd.args[0])
                    machine_code.extend(UVMSpec.encode_write_mem(address))
                else:
                    print(f"Ошибка: команда WRITE требует 1 аргумент, получено {len(cmd.args)}")
            
            elif cmd.mnemonic == "SUB":
                if len(cmd.args) == 1:
                    address = self.assembler.parse_number(cmd.args[0])
                    machine_code.extend(UVMSpec.encode_sub(address))
                else:
                    print(f"Ошибка: команда SUB требует 1 аргумент, получено {len(cmd.args)}")
            
            else:
                print(f"Предупреждение: неизвестная мнемоника '{cmd.mnemonic}'")
        
        return machine_code
    
    def save_binary_file(self, machine_code, filename):
        """Сохраняет машинный код в бинарный файл"""
        try:
            with open(filename, 'wb') as f:
                for byte in machine_code:
                    f.write(bytes([byte]))
            return True
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return False
    
    def format_bytes_hex(self, machine_code):
        """Форматирует байты в hex строки"""
        result = []
        for byte in machine_code:
            hex_str = f"{byte:02X}"
            result.append(f"0x{hex_str}")
        return result

def test_specification_sequences():
    """Проверяет тестовые байтовые последовательности из спецификации"""
    print("\nТестовые байтовые последовательности из спецификации УВМ:")
    print("-" * 60)
    
    # Тестовые случаи для варианта 26
    test_cases = [
        ("LOAD 553", [0xCA, 0x29, 0x02, 0x00]),
        ("READ 268", [0x9C, 0x0C, 0x01]),
        ("WRITE 617", [0x5D, 0x69, 0x02, 0x00]),
        ("SUB 455", [0xAF, 0xC7, 0x01, 0x00]),
    ]
    
    all_passed = True
    for command, expected_bytes in test_cases:
        print(f"Тест: {command}")
        
        # Создаем ассемблер и генерируем код
        generator = CodeGenerator()
        test_program = command + "\n"
        generated_code = generator.generate_machine_code(test_program)
        
        # Форматируем вывод
        expected_hex = [f"0x{b:02X}" for b in expected_bytes]
        generated_hex = [f"0x{b:02X}" for b in generated_code]
        
        passed = generated_code == expected_bytes
        
        print(f"  Ожидается: {' '.join(expected_hex)}")
        print(f"  Получено:  {' '.join(generated_hex)}")
        print(f"  Результат: {'ПРОЙДЕНО' if passed else 'ОШИБКА'}")
        print()
        
        all_passed = all_passed and passed
    
    return all_passed

def create_test_asm_file():
    """Создает тестовый ASM файл с примерами из спецификации"""
    content = """; Тестовый файл для проверки спецификации УВМ
; Этот файл должен генерировать тестовые байтовые последовательности

; Тестовые команды из спецификации (вариант 26):
LOAD 553      ; Должно быть: 0xCA 0x29 0x02 0x00
READ 268      ; Должно быть: 0x9C 0x0C 0x01
WRITE 617     ; Должно быть: 0x5D 0x69 0x02 0x00
SUB 455       ; Должно быть: 0xAF 0xC7 0x01 0x00

; Дополнительные тесты с hex:
LOAD 0x229    ; 553 в hex
READ 0x10C    ; 268 в hex
WRITE 0x269   ; 617 в hex
SUB 0x1C7     ; 455 в hex"""
    
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
  python code_generator.py program.asm program.bin          # Обычная компиляция
  python code_generator.py program.asm program.bin --test   # Режим тестирования
  python code_generator.py --create-test                    # Создать тестовый файл
  python code_generator.py --spec-test                      # Проверить спецификацию
        """
    )
    
    parser.add_argument(
        'input_file',
        nargs='?',
        help='Путь к исходному файлу с текстом программы'
    )
    
    parser.add_argument(
        'output_file',
        nargs='?',
        help='Путь к двоичному файлу-результату'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Режим тестирования (вывод байтового формата)'
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
        # Проверка тестовых последовательностей из спецификации
        test_specification_sequences()
    
    elif args.create_test:
        # Создание тестового файла
        create_test_asm_file()
    
    elif args.input_file and args.output_file:
        # Основной режим компиляции
        generator = CodeGenerator()
        
        # Чтение исходного кода
        source_code = read_program_file(args.input_file)
        if source_code is None:
            return
        
        print(f"Компиляция файла: {args.input_file}")
        print(f"Выходной файл: {args.output_file}")
        print("-" * 60)
        
        # Генерация машинного кода
        machine_code = generator.generate_machine_code(source_code)
        
        if not machine_code:
            print("Ошибка: не удалось сгенерировать машинный код")
            return
        
        # Сохранение в файл
        if generator.save_binary_file(machine_code, args.output_file):
            print(f"Файл успешно сохранен: {args.output_file}")
        
        # Вывод информации
        print(f"Размер двоичного файла: {len(machine_code)} байт")
        
        if args.test:
            # Режим тестирования - вывод байтов
            print("\nБайтовое представление (как в спецификации):")
            print("-" * 60)
            hex_bytes = generator.format_bytes_hex(machine_code)
            
            # Выводим по 8 байт в строке
            for i in range(0, len(hex_bytes), 8):
                line_bytes = hex_bytes[i:i+8]
                print(" ".join(line_bytes))
            
            # Проверка спецификации
            print("\n" + "=" * 60)
            print("Дополнительная проверка спецификации:")
            test_specification_sequences()
    
    else:
        parser.print_help()
        
        # Пример использования
        print("\n" + "=" * 60)
        print("Пример тестовой программы (сохраните как example.asm):")
        print("=" * 60)
        
        example_program = """; 
        print(example_program)
        
        print("\n" + "=" * 60)
        print("Команды для тестирования:")
        print("  python code_generator.py --create-test")
        print("  python code_generator.py test_spec.asm output.bin --test")
        print("  python code_generator.py --spec-test")

if __name__ == "__main__":
    main()
