#include <iostream>
#include <double-conversion/double-conversion.h>
#include <double-conversion/utils.h>

using namespace double_conversion;

int main() {
    char buffer[128];
    StringBuilder builder(buffer, 128);
    
    // Используем стандартный EcmaScript конвертер для преобразования числа в строку
    DoubleToStringConverter::EcmaScriptConverter().ToShortest(3.14159, &builder);
    
    std::cout << "Converted: " << builder.Finalize() << std::endl;
    return 0;
}