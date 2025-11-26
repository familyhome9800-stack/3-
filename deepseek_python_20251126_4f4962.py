class Command:
    def __init__(self, mnemonic, args=None):
        self.mnemonic = mnemonic
        self.args = args or []
    
    def __repr__(self):
        return f"Command({self.mnemonic}, {self.args})"

class Assembler:
    def __init__(self):
        self.commands = []
        self.labels = {}
        
    def parse_line(self, line):
        line = line.strip()
        if not line or line.startswith(';'):
            return None
            
        # Удаление комментариев
        if ';' in line:
            line = line.split(';')[0].strip()
        
        # Обработка меток
        if line.endswith(':'):
            label = line[:-1]
            self.labels[label] = len(self.commands)
            return None
            
        parts = line.split()
        if not parts:
            return None
            
        mnemonic = parts[0].upper()
        args = []
        
        for arg in parts[1:]:
            if ',' in arg:
                args.extend(a.strip() for a in arg.split(','))
            else:
                args.append(arg.strip())
                
        args = [a for a in args if a]
        
        return Command(mnemonic, args)
    
    def assemble(self, source_code):
        lines = source_code.split('\n')
        self.commands = []
        self.labels = {}
        
        # Первый проход - сбор меток и команд
        for line in lines:
            parsed = self.parse_line(line)
            if parsed and parsed.mnemonic:
                self.commands.append(parsed)
        
        # Второй проход - разрешение меток
        resolved_commands = []
        for cmd in self.commands:
            resolved_args = []
            for arg in cmd.args:
                if arg in self.labels:
                    resolved_args.append(str(self.labels[arg]))
                else:
                    resolved_args.append(arg)
            resolved_commands.append(Command(cmd.mnemonic, resolved_args))
        
        return resolved_commands
    
    def parse_number(self, s):
        s = str(s).strip()
        if s.startswith('0x'):
            return self.hex_to_int(s[2:])
        return int(s)
    
    def hex_to_int(self, hex_str):
        hex_str = hex_str.upper()
        result = 0
        for char in hex_str:
            if '0' <= char <= '9':
                result = result * 16 + (ord(char) - ord('0'))
            elif 'A' <= char <= 'F':
                result = result * 16 + (ord(char) - ord('A') + 10)
        return result
    
    def int_to_hex(self, num, digits=2):
        if num == 0:
            return "0" * digits
            
        hex_digits = "0123456789ABCDEF"
        result = ""
        n = num
        while n > 0:
            result = hex_digits[n % 16] + result
            n = n // 16
        return result.zfill(digits)