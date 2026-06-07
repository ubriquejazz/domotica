#ifndef FUNCIONES_H
#define FUNCIONES_H

/*
 * Date: 2022-03
 * File: profes.c (sesion 10 y 7)
 */

#include <msp430.h>

#define BIT_TIME  208       // Ciclos de CPU para 4800 baudios a 1MHz

void uart_init(int pin);
void uart_write(unsigned char caracter);
void process_meas(unsigned long ciclos, char* outbuff);

#endif