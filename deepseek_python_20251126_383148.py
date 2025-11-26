from asm_parser import Assembler
from uvm_spec import UVMSpec

class CodeGenerator:
    def __init__(self):
        self.assembler = Assembler()
    
    def generate_machine_code(self, source_code):
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
        # Создаем бинарный файл
        try:
            with open(filename, 'wb') as f:
                for byte in machine_code:
                    f.write(bytes([byte]))
            print(f"Файл '{filename}' успешно сохранен")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
    
    def format_bytes_hex(self, machine_code):
        result = []
        for byte in machine_code:
            result.append(f"0x{self.assembler.int_to_hex(byte)}")
        return result

def test_stage2():
    generator = CodeGenerator()
    
    print("\n=== ЭТАП 2: Формирование машинного кода ===\n")
    
    # Программа, соответствующая тестовым случаям из спецификации
    test_program = """
    ; Программа, соответствующая тестовым байтовым последовательностям
    LOAD 553      ; Должна сгенерировать: 0xCA, 0x29, 0x02, 0x00
    READ 268      ; Должна сгенерировать: 0x9C, 0x0C, 0x01
    WRITE 617     ; Должна сгенерировать: 0x5D, 0x69, 0x02, 0x00
    SUB 455       ; Должна сгенерировать: 0xAF, 0xC7, 0x01, 0x00
    """
    
    # Генерация машинного кода
    machine_code = generator.generate_machine_code(test_program)
    
    print("Результат ассемблирования:")
    print(f"  Размер двоичного файла: {len(machine_code)} байт")
    
    # Форматированный вывод байтов
    hex_bytes = generator.format_bytes_hex(machine_code)
    print("  Байтовое представление:")
    print("    " + " ".join(hex_bytes))
    
    # Сохранение в файл
    generator.save_binary_file(machine_code, "program.bin")
    
    # Проверка соответствия спецификации
    expected_bytes = [
        0xCA, 0x29, 0x02, 0x00,  # LOAD 553
        0x9C, 0x0C, 0x01,        # READ 268  
        0x5D, 0x69, 0x02, 0x00,  # WRITE 617
        0xAF, 0xC7, 0x01, 0x00   # SUB 455
    ]
    
    print(f"\nПроверка соответствия спецификации:")
    print(f"  Ожидаемая последовательность: {[hex(x) for x in expected_bytes]}")
    print(f"  Полученная последовательность: {[hex(x) for x in machine_code]}")
    print(f"  Полное совпадение: {machine_code == expected_bytes}")
    
    # Дополнительная проверка с шестнадцатеричными числами
    print("\nТест с шестнадцатеричными числами:")
    hex_program = """
    LOAD 0x229    ; 553 в hex
    READ 0x10C    ; 268 в hex  
    WRITE 0x269   ; 617 в hex
    SUB 0x1C7     ; 455 в hex
    """
    
    hex_machine_code = generator.generate_machine_code(hex_program)
    print(f"  Результат с hex числами: {[hex(x) for x in hex_machine_code]}")
    print(f"  Совпадение с ожидаемым: {hex_machine_code == expected_bytes}")

if __name__ == "__main__":
    test_stage2()