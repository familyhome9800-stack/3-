class UVMSpec:
    """Спецификация УВМ для варианта 26"""
    
    # Коды операций
    LOAD_CONST = 202    # 0xCA - Загрузка константы
    READ_MEM = 156      # 0x9C - Чтение из памяти
    WRITE_MEM = 93      # 0x5D - Запись в память
    SUB = 175           # 0xAF - Вычитание
    
    @staticmethod
    def encode_load_const(constant):
        """
        Кодирует команду LOAD константы
        Формат: A=202 (8 бит), B=constant (24 бита)
        Размер: 4 байта
        """
        a = UVMSpec.LOAD_CONST
        b = constant & 0xFFFFFF  # Обеспечиваем 24 бита
        
        return [
            a & 0xFF,           # Байт 0: код операции
            (b >> 16) & 0xFF,   # Байт 1: старшие 8 бит константы
            (b >> 8) & 0xFF,    # Байт 2: средние 8 бит константы  
            b & 0xFF            # Байт 3: младшие 8 бит константы
        ]
    
    @staticmethod
    def encode_read_mem(offset):
        """
        Кодирует команду READ из памяти
        Формат: A=156 (8 бит), B=offset (16 бит)
        Размер: 3 байта
        """
        a = UVMSpec.READ_MEM
        b = offset & 0xFFFF  # Обеспечиваем 16 бит
        
        return [
            a & 0xFF,        # Байт 0: код операции
            (b >> 8) & 0xFF, # Байт 1: старшие 8 бит смещения
            b & 0xFF         # Байт 2: младшие 8 бит смещения
        ]
    
    @staticmethod
    def encode_write_mem(address):
        """
        Кодирует команду WRITE в память
        Формат: A=93 (8 бит), B=address (24 бита)
        Размер: 4 байта
        """
        a = UVMSpec.WRITE_MEM
        b = address & 0xFFFFFF  # Обеспечиваем 24 бита
        
        return [
            a & 0xFF,           # Байт 0: код операции
            (b >> 16) & 0xFF,   # Байт 1: старшие 8 бит адреса
            (b >> 8) & 0xFF,    # Байт 2: средние 8 бит адреса
            b & 0xFF            # Байт 3: младшие 8 бит адреса
        ]
    
    @staticmethod
    def encode_sub(address):
        """
        Кодирует команду SUB (вычитание)
        Формат: A=175 (8 бит), B=address (24 бита)
        Размер: 4 байта
        """
        a = UVMSpec.SUB
        b = address & 0xFFFFFF  # Обеспечиваем 24 бита
        
        return [
            a & 0xFF,           # Байт 0: код операции
            (b >> 16) & 0xFF,   # Байт 1: старшие 8 бит адреса
            (b >> 8) & 0xFF,    # Байт 2: средние 8 бит адреса
            b & 0xFF            # Байт 3: младшие 8 бит адреса
        ]
