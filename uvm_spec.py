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
        b = constant & 0xFFFFFF  # Обеспечиваем 24 бита
        
        # Упаковка в little-endian
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
        b = offset & 0xFFFF  # Обеспечиваем 16 бит
        
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
        b = address & 0xFFFFFF  # Обеспечиваем 24 бита
        
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
        b = address & 0xFFFFFF  # Обеспечиваем 24 бита
        
        return [
            a & 0xFF,           # Байт 0: код операции
            (b >> 16) & 0xFF,   # Байт 1: старшие 8 бит адреса
            (b >> 8) & 0xFF,    # Байт 2: средние 8 бит адреса
            b & 0xFF            # Байт 3: младшие 8 бит адреса
        ]
