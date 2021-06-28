#ifndef NRF52840_HAL_H
#define NRF52840_HAL_H


#include <stdint.h>
void init_uart(void);
void putch(char c);
char getch(void);

void trigger_setup(void);
void trigger_low(void);
void trigger_high(void);

void HW_AES128_Init(void);
void HW_AES128_LoadKey(uint8_t* key);
void HW_AES128_Enc(uint8_t* pt);

#endif 
