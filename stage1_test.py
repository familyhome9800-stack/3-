from asm_parser import Assembler, read_program_file
from uvm_spec import UVMSpec

def run_stage1(input_file, test_mode=False):
    """Выполняет этап 1: перевод программы в промежуточное представление"""
    assembler = Assembler()
    
    print("=== ЭТАП 1: Перевод программы в промежуточное представление ===")
    print(f"Входной файл: {input_file}")
    print("-" * 60)
    
    # Чтение программы из файла
    source_code = read_program_file(input_file)
    if source_code is None:
        return
    
    # Вывод исходного кода
    print("Исходный код программы:")
    print(source_code)
    print("-" * 60)
    
    # Парсинг программы
    commands = assembler.assemble(source_code)
    
    print("\nВнутреннее представление программы:")
    print("-" * 60)
    
    if test_mode:
        # В режиме тестирования выводим в формате полей и значений
        print("Формат: Код_операции(Аргументы) -> [байты]")
        print("-" * 60)
        
        for i, cmd in enumerate(commands):
            if cmd.mnemonic == "LOAD" and len(cmd.args) == 1:
                const = assembler.parse_number(cmd.args[0])
                bytes_list = UVMSpec.encode_load_const(const)
                print(f"Команда {i:2d}: LOAD({const}) -> {[hex(b) for b in bytes_list]}")
                
            elif cmd.mnemonic == "READ" and len(cmd.args) == 1:
                offset = assembler.parse_number(cmd.args[0])
                bytes_list = UVMSpec.encode_read_mem(offset)
                print(f"Команда {i:2d}: READ({offset}) -> {[hex(b) for b in bytes_list]}")
                
            elif cmd.mnemonic == "WRITE" and len(cmd.args) == 1:
                addr = assembler.parse_number(cmd.args[0])
                bytes_list = UVMSpec.encode_write_mem(addr)
                print(f"Команда {i:2d}: WRITE({addr}) -> {[hex(b) for b in bytes_list]}")
                
            elif cmd.mnemonic == "SUB" and len(cmd.args) == 1:
                addr = assembler.parse_number(cmd.args[0])
                bytes_list = UVMSpec.encode_sub(addr)
                print(f"Команда {i:2d}: SUB({addr}) -> {[hex(b) for b in bytes_list]}")
                
            else:
                print(f"Команда {i:2d}: {cmd}")
    else:
        # Обычный вывод промежуточного представления
        for i, cmd in enumerate(commands):
            print(f"Команда {i:2d}: {cmd}")
    
    print("-" * 60)
    return commands

def test_specification():
    """Проверяет тестовые случаи из спецификации УВМ"""
    print("\nПроверка тестовых случаев из спецификации УВМ:")
    print("-" * 60)
    
    tests = [
        ("LOAD 553", 553, UVMSpec.encode_load_const),
        ("READ 268", 268, UVMSpec.encode_read_mem),
        ("WRITE 617", 617, UVMSpec.encode_write_mem),
        ("SUB 455", 455, UVMSpec.encode_sub)
    ]
    
    expected_results = [
        [0xCA, 0x29, 0x02, 0x00],
        [0x9C, 0x0C, 0x01],
        [0x5D, 0x69, 0x02, 0x00],
        [0xAF, 0xC7, 0x01, 0x00]
    ]
    
    all_passed = True
    for (name, value, encoder), expected in zip(tests, expected_results):
        result = encoder(value)
        passed = result == expected
        all_passed = all_passed and passed
        
        print(f"{name:15} -> Ожидается: {[hex(x) for x in expected]}")
        print(f"{'':15}   Получено:  {[hex(x) for x in result]}")
        print(f"{'':15}   Статус:    {'ПРОЙДЕНО' if passed else 'ОШИБКА'}")
        print()
    
    return all_passed

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Ассемблер УВМ - Этап 1: Перевод программы в промежуточное представление',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python stage1_main.py program.asm            # Обычный режим
  python stage1_main.py program.asm --test     # Режим тестирования
  python stage1_main.py --spec-test            # Только проверка спецификации
        """
    )
    
    parser.add_argument(
        'input_file',
        nargs='?',
        help='Путь к исходному файлу с текстом программы'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Режим тестирования (вывод в формате полей и значений)'
    )
    
    parser.add_argument(
        '--spec-test',
        action='store_true',
        help='Проверить только тестовые случаи из спецификации УВМ'
    )
    
    args = parser.parse_args()
    
    print("АССЕМБЛЕР УЧЕБНОЙ ВИРТУАЛЬНОЙ МАШИНЫ (УВМ)")
    print("Вариант 26 - Конфигурационное управление")
    print("=" * 60)
    
    if args.spec_test:
        # Только проверка спецификации
        test_specification()
    elif args.input_file:
        # Основной режим работы
        commands = run_stage1(args.input_file, args.test)
        
        if args.test:
            print("\nДополнительная проверка спецификации:")
            print("-" * 60)
            test_specification()
    else:
        parser.print_help()
        
        # Создаем пример программы, если файл не указан
        print("\n" + "=" * 60)
        print("Пример программы для тестирования (сохраните как test.asm):")
        print("=" * 60)
        example_program = """; Пример программы для УВМ
; Команды соответствуют тестовым случаям из спецификации

LOAD 553      ; Загрузить константу 553
READ 268      ; Прочитать из памяти (аккумулятор + 268)
WRITE 617     ; Записать аккумулятор по адресу 617
SUB 455       ; Вычесть значение из памяти по адресу 455

; Пример с шестнадцатеричными числами
LOAD 0x229    ; 553 в hex
READ 0x10C    ; 268 в hex
WRITE 0x269   ; 617 в hex
SUB 0x1C7     ; 455 в hex"""
        
        print(example_program)

if __name__ == "__main__":
    main()
