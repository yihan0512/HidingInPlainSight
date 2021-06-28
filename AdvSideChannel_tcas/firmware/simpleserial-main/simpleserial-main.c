/*
    This file is part of the ChipWhisperer Example Targets
    Copyright (C) 2012-2017 NewAE Technology Inc.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include "hal.h"
#include "simpleserial.h"
#include <stdlib.h>
#include <string.h>
#include "tcas_lessfcns.c"

// #include "flash.h"


// void flash_initialize()
// {
// 	HAL_FLASH_Unlock();
// }

// void flash_deinitialize()
// {
// 	HAL_FLASH_Lock();
// }

// void flash_erase(uint8_t sector)
// {
//     uint32_t error = 0;
//     FLASH_EraseInitTypeDef FLASH_EraseInitStruct =
//     {
//     	.TypeErase = FLASH_TYPEERASE_SECTORS,
// 	.Sector = (uint32_t)sector,
// 	.NbSectors = 1,
// 	.VoltageRange = FLASH_VOLTAGE_RANGE_3
//     };

//     HAL_FLASHEx_Erase(&FLASH_EraseInitStruct,&error);
// }

// uint8_t flash_write(volatile uint32_t* address, uint32_t *data, uint16_t size)
// {
//    for (int i = 0; i < size; i++)
//      if (HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, (*address)+(i*4), data[i]) != HAL_OK)
//     	return 1;
//    return 0;
// }

void loop(void) {

    // serial communication init
    char *ascii_buf;
    char *tokens;
    char c;
    int i;
    int arr[13];
    int actuation;

    ascii_buf = malloc(500*sizeof(char));


    c = getch();
    i = 0;
    while (c != '\n') {
        ascii_buf[i] = c;
        c = getch();
        i++;
    }
    ascii_buf[i] = '\0';

    tokens = strtok(ascii_buf, " \000");
    i = 1;
    while (tokens != NULL) {
        arr[i] = atoi(tokens);
        tokens = strtok(NULL, " \000");
        i++;
    }

    if (i != 13) {
        putch('e');
        putch('r');
        putch('r');
        putch('o');
        putch('r');
        putch('!');
        putch('\n');
        return;
    }

    free(ascii_buf);


    initialize();
    Cur_Vertical_Sep = arr[1];
    High_Confidence = arr[2];
    Two_of_Three_Reports_Valid = arr[3];
    Own_Tracked_Alt = arr[4];
    Own_Tracked_Alt_Rate = arr[5];
    Other_Tracked_Alt = arr[6];
    Alt_Layer_Value = arr[7];
    Up_Separation = arr[8];
    Down_Separation = arr[9];
    Other_RAC = arr[10];
    Other_Capability = arr[11];
    Climb_Inhibit = arr[12];


    trigger_high();
    alt_sep_test();
    actuation = alt_sep_result + '0';
    trigger_low();

    putch(actuation);


    // putch(alt_sep_result+'0');
    putch('\n');

    putch('d');
    putch('o');
    putch('n');
    putch('e');
    putch('!');
    putch('\n');
}


int main(void)
{
    platform_init();
    init_uart();
    trigger_setup();

    putch('h');
    putch('e');
    putch('l');
    putch('l');
    putch('o');
    putch('\n');

	simpleserial_init();

    while(1) 
    {
        loop();
    }
}
