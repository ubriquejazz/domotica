#include "funciones.h"

int pin_tx;

void uart_init(int pin) {
    pin_tx = pin;
    P1OUT |= pin;               // Línea UART en reposo (ALTO)
}

void uart_write(unsigned char caracter) {
    unsigned char bit_count = 8;

    // 1. BIT DE START (Línea a BAJO)
    P1OUT &= ~pin_tx;
    __delay_cycles(BIT_TIME); // Espera exacta de 208 ciclos

    // 2. ENVIAR LOS 8 BITS DE DATOS (LSB primero)
    while (bit_count > 0) {
        if (caracter & 0x01) {
            P1OUT |= pin_tx;   // Es un 1
        } else {
            P1OUT &= ~pin_tx;  // Es un 0
        }
        
        __delay_cycles(BIT_TIME); // Espera exacta por cada bit
        caracter >>= 1;
        bit_count--;
    }

    // 3. BIT DE STOP (Línea a ALTO)
    P1OUT |= pin_tx;
    __delay_cycles(BIT_TIME); // Asegura el tiempo de parada
}

// Función para convertir un número a texto dentro de un buffer
// Devuelve el puntero al final del texto insertado
char* unsigned_to_str(unsigned long num, char* buf) {
    char temp[10];
    int i = 0;
    if (num == 0) {
        *buf++ = '0';
        return buf;
    }
    while (num > 0) {
        temp[i++] = (num % 10) + '0';
        num /= 10;
    }
    while (i > 0) {
        *buf++ = temp[--i];
    }
    return buf;
}

// Copia una cadena de texto fija en el buffer
char* copy_str(const char* src, char* dest) {
    while (*src) {
        *dest++ = *src++;
    }
    return dest;
}

void process_meas(unsigned long ciclos, char* out_buffer) {
    unsigned long distancia_cm = ciclos / 3; 
    long altura_agua_cm = 220 - distancia_cm;

    // Caso Depósito Lleno / Zona muerta
    if (distancia_cm < 20) {
        out_buffer = copy_str("D: LLENO | V: 6000L\r\n", out_buffer);
        *out_buffer = '\0'; // Cerrar la cadena
        return;
    }
    if (altura_agua_cm < 0) altura_agua_cm = 0;

    // Calcular litros (31.4 litros por cm)
    unsigned long litros_actuales = (altura_agua_cm * 314) / 10;
    if (litros_actuales > 6000) litros_actuales = 6000;

    // Construimos la cadena en memoria de forma ultra eficiente:
    out_buffer = copy_str("D: ", out_buffer);
    out_buffer = unsigned_to_str(distancia_cm, out_buffer);
    out_buffer = copy_str("cm | H: ", out_buffer);
    out_buffer = unsigned_to_str(altura_agua_cm, out_buffer);
    out_buffer = copy_str("cm | V: ", out_buffer);
    out_buffer = unsigned_to_str(litros_actuales, out_buffer);
    out_buffer = copy_str("L\r\n", out_buffer);
    
    *out_buffer = '\0'; // Asegurar el fin de cadena string en C
}
