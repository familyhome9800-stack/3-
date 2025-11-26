from stage1_test import test_stage1
from code_generator import test_stage2

def main():
    print("АССЕМБЛЕР И ИНТЕРПРЕТАТОР ДЛЯ УВМ - ВАРИАНТ 26")
    print("=" * 50)
    
    # Запуск этапа 1
    test_stage1()
    
    # Запуск этапа 2  
    test_stage2()
    
    print("\n" + "=" * 50)
    print("Этапы 1 и 2 завершены успешно!")

if __name__ == "__main__":
    main()