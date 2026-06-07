#include <msp430.h>
#include "funciones.h"

#define EN1       BIT0      // Pin 2, P1.0
#define TXD       BIT1      // Pin 3, P1.1
#define IN        BIT2      // Pin 4, P1.2 (in)
#define ECHO      BIT3      // Pin 5, P1.3 (in)
#define TRIG      BIT4      // Pin 6, P1.4
#define EN2       BIT5      // Pin 7, P1.5

#define WAKEUP_TIME 4 // segundos
volatile unsigned int wake_counter = 0;

void print(char *cadena) {
    while (*cadena) {
        uart_write(*cadena);
        cadena++;
    }
}

void print_long(unsigned long numero) {
    char buffer[11];
    int i = 0;

    if (numero == 0) {
        uart_write('0');
        return;
    }
    while (numero > 0) {
        buffer[i] = (numero % 10) + '0';
        numero /= 10;
        i++;
    }
    while (i > 0) {
        i--;
        uart_write(buffer[i]);
    }
}

void pulso_trigger() {
    P1OUT |= TRIG;
    __delay_cycles(10);      // 10 ciclos a 1MHz = 10 microsegundos
    P1OUT &= ~TRIG;
}

unsigned long compute_cycles(unsigned long max) {
    unsigned long duracion_ciclos = 0;
    
    unsigned int timeout1 = 0;
    while ((P1IN & ECHO) == 0) {
        timeout1++;
        if (timeout1 > max) { 
            break; // Rompe el bucle si el sensor no empieza a responder
        }
    }
    unsigned int timeout2 = 0;
    while ((P1IN & ECHO) != 0) {
        duracion_ciclos++;
        timeout2++;
            
            // Si el pin se queda en ALTO por un error del sensor
            if (timeout2 > max) {
                break;
            }
            __delay_cycles(1); 
        }

    if (timeout1 > max) {
        print("Error: Timeout inicial\r\n");
        return 0;
    }
    if (timeout2 > max) {
        print("Error: Timeout\r\n");
        return 0;
    }
    return duracion_ciclos;
}

int main(void) {
    
    unsigned long ciclos;
    
    WDTCTL = WDTPW | WDTHOLD;   // Detener Watchdog

    // Calibración estricta del DCO a 1 MHz
    if (CALBC1_1MHZ == 0xFF) {  
        while(1); 
    }
    DCOCTL = CALDCO_1MHZ;       
    BCSCTL1 = CALBC1_1MHZ;

    // Timer interrupt configuration
    BCSCTL3 |= LFXT1S_2;
    TACTL = TASSEL_1 + MC_1; // TASSEL_1 selects ACLK, MC_1 is Up-mode
    TACCR0 = 12000 - 1;     // Since VLO is ~12000 Hz                     
    TACCTL0 = CCIE;         // Enable Timer interrupt

    // Port configuration
    P1DIR |= EN1 | EN2;     // EN1, EN2 como salidas
    P1DIR |= TXD | TRIG;    // TXD, TRIG como salidas
    P1OUT &= ~(EN1 | EN2 | TRIG) ;  // Disble peripherals (low power)
    uart_init(TXD);

    __enable_interrupt();   // Enable global interrupts

    while (1) {
        __bis_SR_register(LPM3_bits + GIE);   // Go to deep sleep (LPM3)

        P1OUT |= EN2;           // Habilitamos el AJ-SR04
        __delay_cycles(10);     // 10 ciclos a 1MHz = 10 microsegundos
        P1OUT |= EN1;           // Habilitamos el MAX3485
        __delay_cycles(10); 

        pulso_trigger();
        ciclos = compute_cycles(6000); // timeout
#if(1)
        char mensaje[40];
        process_meas(ciclos, mensaje);
        print(mensaje);
#else
        print_long(ciclos);
        print("\n\r");
#endif

    P1OUT &= ~(EN1 | EN2);
    }
}

// Timer A0 interrupt service routine (Fires every 1 second)
#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector=TIMERA0_VECTOR
__interrupt void Timer_A (void)
#elif defined(__GNUC__)
void __attribute__ ((interrupt(TIMERA0_VECTOR))) Timer_A (void)
#endif
{
    wake_counter++;                           // Add 1 second to our count
    
    if (wake_counter >= WAKEUP_TIME) {                  // Check for 4 seconds
        wake_counter = 0;                     // Reset counter
        __bic_SR_register_on_exit(LPM3_bits); // Wake up the main loop
    }
}