#!/usr/bin/env python3
"""
Ассемблер для учебной виртуальной машины (УВМ)
Требования:
1. Транслятор из промежуточного в машинное представление ✓
2. Запись результата в двоичный выходной файл ✓
3. Вывод на экран размера двоичного файла в байтах ✓
4. В режиме тестирования вывод в байтовом формате как в спецификации ✓
"""

import struct
import sys

class UVMAssembler:
    """Минимальный ассемблер УВМ"""
    
    # Коды операций из спецификации
    OP_LOAD = 202   # Загрузка константы
    OP_READ = 156   # Чтение из памяти
    OP_WRITE = 93   # Запись в память
    OP_SUB = 175    # Вычитание
    
    def __init__(self):
        self.binary_data = bytearray()
        self.test_mode = False
    
    def assemble_load(self, const_value):
        """Ассемблирование LOAD <const>"""
        if const_value < 0 or const_value > 0xFFFFFF:
            raise ValueError(f"Константа {const_value} вне диапазона 24 бит")
        
        # Формат: A (1 байт) + B (3 байта)
        machine_code = struct.pack('<B I', self.OP_LOAD, const_value)[:4]
        self.binary_data.extend(machine_code)
        
        if self.test_mode:
            hex_bytes = ', '.join(f'0x{b:02X}' for b in machine_code)
            print(f"LOAD {const_value}: {hex_bytes}")
    
    def assemble_read(self, offset):
        """Ассемблирование READ <offset>"""
        if offset < 0 or offset > 0xFFFF:
            raise ValueError(f"Смещение {offset} вне диапазона 16 бит")
        
        # Формат: A (1 байт) + смещение (2 байта)
        machine_code = struct.pack('<B H', self.OP_READ, offset)
        self.binary_data.extend(machine_code)
        
        if self.test_mode:
            hex_bytes = ', '.join(f'0x{b:02X}' for b in machine_code)
            print(f"READ {offset}: {hex_bytes}")
    
    def assemble_write(self, address):
        """Ассемблирование WRITE <addr>"""
        if address < 0 or address > 0xFFFFFF:
            raise ValueError(f"Адрес {address} вне диапазона 24 бит")
        
        # Формат: A (1 байт) + B (3 байта)
        machine_code = struct.pack('<B I', self.OP_WRITE, address)[:4]
        self.binary_data.extend(machine_code)
        
        if self.test_mode:
            hex_bytes = ', '.join(f'0x{b:02X}' for b in machine_code)
            print(f"WRITE {address}: {hex_bytes}")
    
    def assemble_sub(self, address):
        """Ассемблирование SUB <addr>"""
        if address < 0 or address > 0xFFFFFF:
            raise ValueError(f"Адрес {address} вне диапазона 24 бит")
        
        # Формат: A (1 байт) + B (3 байта)
        machine_code = struct.pack('<B I', self.OP_SUB, address)[:4]
        self.binary_data.extend(machine_code)
        
        if self.test_mode:
            hex_bytes = ', '.join(f'0x{b:02X}' for b in machine_code)
            print(f"SUB {address}: {hex_bytes}")
    
    def parse_and_assemble(self, source_code):
        """Парсинг и ассемблирование исходного кода"""
        lines = source_code.strip().split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Пропускаем пустые строки и комментарии
            if not line or line.startswith(';'):
                continue
            
            # Удаляем комментарии в конце строки
            if ';' in line:
                line = line.split(';')[0].strip()
            
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"Строка {line_num}: неверный формат '{line}'")
            
            command = parts[0].upper()
            operand = int(parts[1])
            
            # Ассемблируем команду
            if command == "LOAD":
                self.assemble_load(operand)
            elif command == "READ":
                self.assemble_read(operand)
            elif command == "WRITE":
                self.assemble_write(operand)
            elif command == "SUB":
                self.assemble_sub(operand)
            else:
                raise ValueError(f"Строка {line_num}: неизвестная команда '{command}'")
    
    def save_to_file(self, filename):
        """Сохранение в двоичный файл"""
        with open(filename, 'wb') as f:
            f.write(self.binary_data)
        
        print(f"Размер двоичного файла: {len(self.binary_data)} байт")
        return len(self.binary_data)


def create_test_program():
    """Создание тестовой программы по спецификации УВМ"""
    test_source = """LOAD 553
READ 268
WRITE 617
SUB 455"""
    
    with open('test_program.asm', 'w') as f:
        f.write(test_source)
    
    print("Создан test_program.asm с тестами из спецификации")
    return test_source


def main():
    """Главная функция"""
    # Создаем тестовую программу
    source_code = create_test_program()
    
    # 1. Ассемблирование в обычном режиме
    print("\n1. Обычный режим ассемблирования:")
    assembler1 = UVMAssembler()
    assembler1.test_mode = False
    assembler1.parse_and_assemble(source_code)
    assembler1.save_to_file('output_normal.bin')
    
    # 2. Ассемблирование в режиме тестирования
    print("\n2. Режим тестирования:")
    assembler2 = UVMAssembler()
    assembler2.test_mode = True
    assembler2.parse_and_assemble(source_code)
    file_size = assembler2.save_to_file('output_test.bin')
    
    # 3. Проверка результатов
    print("\n3. Проверка результатов:")
    print("-" * 40)
    
    # Проверяем оба файла
    for filename in ['output_normal.bin', 'output_test.bin']:
        with open(filename, 'rb') as f:
            data = f.read()
        
        print(f"\nФайл: {filename}")
        print(f"Размер: {len(data)} байт")
        print("Содержимое (hex):", ' '.join(f'{b:02X}' for b in data))
    
    # Ожидаемые байты из спецификации
    expected_bytes = [
        0xCA, 0x29, 0x02, 0x00,  # LOAD 553
        0x9C, 0x0C, 0x01,        # READ 268
        0x5D, 0x69, 0x02, 0x00,  # WRITE 617
        0xAF, 0xC7, 0x01, 0x00   # SUB 455
    ]
    
    print("\n4. Сравнение с ожидаемым результатом:")
    print("-" * 40)
    
    with open('output_test.bin', 'rb') as f:
        actual_bytes = list(f.read())
    
    if actual_bytes == expected_bytes:
        print("✅ Результат ассемблирования соответствует спецификации!")
        print("\nБайтовые последовательности как в спецификации:")
        print("LOAD 553:  0xCA, 0x29, 0x02, 0x00")
        print("READ 268:  0x9C, 0x0C, 0x01")
        print("WRITE 617: 0x5D, 0x69, 0x02, 0x00")
        print("SUB 455:   0xAF, 0xC7, 0x01, 0x00")
    else:
        print("❌ Результат не соответствует спецификации")
        print(f"Ожидалось: {expected_bytes}")
        print(f"Получено:  {actual_bytes}")


if __name__ == "__main__":
    main()
