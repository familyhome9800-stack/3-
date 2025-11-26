from asm_parser import Assembler
from uvm_spec import UVMSpec

def test_stage1():
    assembler = Assembler()
    
    # Тестовая программа для проверки спецификации
    test_program = """
    ; Тест загрузки константы
    LOAD 553
    
    ; Тест чтения из памяти  
    READ 268
    
    ; Тест записи в память
    WRITE 617
    
    ; Тест вычитания
    SUB 455
    """
    
    print("=== ЭТАП 1: Перевод программы в промежуточное представление ===\n")
    
    # Парсинг программы
    commands = assembler.assemble(test_program)
    
    print("Внутреннее представление программы:")
    for i, cmd in enumerate(commands):
        print(f"  Команда {i}: {cmd}")
    
    # Проверка тестовых случаев из спецификации
    print("\nПроверка тестовых случаев из спецификации УВМ:")
    
    # Тест 1: LOAD_CONST (A=202, B=553)
    expected1 = [0xCA, 0x29, 0x02, 0x00]
    result1 = UVMSpec.encode_load_const(553)
    print(f"  LOAD_CONST тест:")
    print(f"    Ожидается: {[hex(x) for x in expected1]}")
    print(f"    Получено:  {[hex(x) for x in result1]}")
    print(f"    Совпадение: {result1 == expected1}")
    
    # Тест 2: READ_MEM (A=156, B=268)
    expected2 = [0x9C, 0x0C, 0x01]
    result2 = UVMSpec.encode_read_mem(268)
    print(f"  READ_MEM тест:")
    print(f"    Ожидается: {[hex(x) for x in expected2]}")
    print(f"    Получено:  {[hex(x) for x in result2]}")
    print(f"    Совпадение: {result2 == expected2}")
    
    # Тест 3: WRITE_MEM (A=93, B=617)
    expected3 = [0x5D, 0x69, 0x02, 0x00]
    result3 = UVMSpec.encode_write_mem(617)
    print(f"  WRITE_MEM тест:")
    print(f"    Ожидается: {[hex(x) for x in expected3]}")
    print(f"    Получено:  {[hex(x) for x in result3]}")
    print(f"    Совпадение: {result3 == expected3}")
    
    # Тест 4: SUB (A=175, B=455)
    expected4 = [0xAF, 0xC7, 0x01, 0x00]
    result4 = UVMSpec.encode_sub(455)
    print(f"  SUB тест:")
    print(f"    Ожидается: {[hex(x) for x in expected4]}")
    print(f"    Получено:  {[hex(x) for x in result4]}")
    print(f"    Совпадение: {result4 == expected4}")
    
    # Проверка парсера чисел
    print("\nПроверка парсера чисел:")
    test_numbers = ["553", "0x229", "268", "617", "455"]
    for num_str in test_numbers:
        parsed = assembler.parse_number(num_str)
        print(f"  '{num_str}' -> {parsed} (0x{assembler.int_to_hex(parsed)})")

if __name__ == "__main__":
    test_stage1()
