   1              	# 1 "simpleserial-main.s"
   1              		.cpu cortex-m4
   0              	
   0              	
   2              		.eabi_attribute 27, 1
   3              		.eabi_attribute 28, 1
   4              		.eabi_attribute 20, 1
   5              		.eabi_attribute 21, 1
   6              		.eabi_attribute 23, 3
   7              		.eabi_attribute 24, 1
   8              		.eabi_attribute 25, 1
   9              		.eabi_attribute 26, 1
  10              		.eabi_attribute 30, 4
  11              		.eabi_attribute 34, 1
  12              		.eabi_attribute 18, 4
  13              		.file	"simpleserial-main.c"
   1              	/*
   2              	    This file is part of the ChipWhisperer Example Targets
   3              	    Copyright (C) 2012-2017 NewAE Technology Inc.
   4              	
   5              	    This program is free software: you can redistribute it and/or modify
   6              	    it under the terms of the GNU General Public License as published by
   7              	    the Free Software Foundation, either version 3 of the License, or
   8              	    (at your option) any later version.
   9              	
  10              	    This program is distributed in the hope that it will be useful,
  11              	    but WITHOUT ANY WARRANTY; without even the implied warranty of
  12              	    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  13              	    GNU General Public License for more details.
  14              	
  15              	    You should have received a copy of the GNU General Public License
  16              	    along with this program.  If not, see <http://www.gnu.org/licenses/>.
  17              	*/
  18              	
  19              	#include "hal.h"
  20              	#include "simpleserial.h"
  21              	#include <stdlib.h>
  22              	#include <string.h>
  23              	#include "tcas_lessfcns.c"
  24              	
  25              	// #include "flash.h"
  26              	
  27              	
  28              	// void flash_initialize()
   1:tcas_lessfcns.c **** 
   2:tcas_lessfcns.c **** /*  -*- Last-Edit:  Fri Jan 29 11:13:27 1993 by Tarak S. Goradia; -*- */
   3:tcas_lessfcns.c **** /* $Log: tcas.c,v $
   4:tcas_lessfcns.c ****  * Revision 1.2  1993/03/12  19:29:50  foster
   5:tcas_lessfcns.c ****  * Correct logic bug which didn't allow output of 2 - hf
   6:tcas_lessfcns.c ****  * */
   7:tcas_lessfcns.c **** 
   8:tcas_lessfcns.c **** #include <stdio.h>
   9:tcas_lessfcns.c **** #include <stdlib.h>
  10:tcas_lessfcns.c **** 
  11:tcas_lessfcns.c **** #include "hal.h"
  12:tcas_lessfcns.c **** 
  13:tcas_lessfcns.c **** 
  14:tcas_lessfcns.c **** // #define OLEV       600		/* in feets/minute */
  15:tcas_lessfcns.c **** // #define MAXALTDIFF 600		/* max altitude difference in feet */
  16:tcas_lessfcns.c **** // #define MINSEP     300          /* min separation in feet */
  17:tcas_lessfcns.c **** // #define NOZCROSS   100		/* in feet */
  18:tcas_lessfcns.c **** // 				/* variables */
  19:tcas_lessfcns.c **** 
  20:tcas_lessfcns.c **** int alt_sep_result;
  21:tcas_lessfcns.c **** 
  22:tcas_lessfcns.c **** int OLEV = 600;
  23:tcas_lessfcns.c **** int MAXALTDIFF=600;
  24:tcas_lessfcns.c **** int MINSEP=300;
  25:tcas_lessfcns.c **** int NOZCROSS=100;
  26:tcas_lessfcns.c **** 
  27:tcas_lessfcns.c **** typedef int bool;
  28:tcas_lessfcns.c **** 
  29:tcas_lessfcns.c **** int Cur_Vertical_Sep;
  30:tcas_lessfcns.c **** bool High_Confidence;
  31:tcas_lessfcns.c **** bool Two_of_Three_Reports_Valid;
  32:tcas_lessfcns.c **** 
  33:tcas_lessfcns.c **** int Own_Tracked_Alt;
  34:tcas_lessfcns.c **** int Own_Tracked_Alt_Rate;
  35:tcas_lessfcns.c **** int Other_Tracked_Alt;
  36:tcas_lessfcns.c **** 
  37:tcas_lessfcns.c **** int Alt_Layer_Value;		/* 0, 1, 2, 3 */
  38:tcas_lessfcns.c **** int Positive_RA_Alt_Thresh[4];
  39:tcas_lessfcns.c **** 
  40:tcas_lessfcns.c **** int Up_Separation;
  41:tcas_lessfcns.c **** int Down_Separation;
  42:tcas_lessfcns.c **** 
  43:tcas_lessfcns.c **** 				/* state variables */
  44:tcas_lessfcns.c **** int Other_RAC;			/* NO_INTENT, DO_NOT_CLIMB, DO_NOT_DESCEND */
  45:tcas_lessfcns.c **** #define NO_INTENT 0
  46:tcas_lessfcns.c **** #define DO_NOT_CLIMB 1
  47:tcas_lessfcns.c **** #define DO_NOT_DESCEND 2
  48:tcas_lessfcns.c **** 
  49:tcas_lessfcns.c **** int Other_Capability;		/* TCAS_TA, OTHER */
  50:tcas_lessfcns.c **** #define TCAS_TA 1
  51:tcas_lessfcns.c **** #define OTHER 2
  52:tcas_lessfcns.c **** 
  53:tcas_lessfcns.c **** int Climb_Inhibit;		/* true/false */
  54:tcas_lessfcns.c **** 
  55:tcas_lessfcns.c **** #define UNRESOLVED 0
  56:tcas_lessfcns.c **** #define UPWARD_RA 1
  57:tcas_lessfcns.c **** #define DOWNWARD_RA 2
  58:tcas_lessfcns.c **** 
  59:tcas_lessfcns.c **** //bool Own_Below_Threat();
  60:tcas_lessfcns.c **** //bool Own_Above_Threat();
  61:tcas_lessfcns.c **** 
  62:tcas_lessfcns.c **** void initialize(void)
  63:tcas_lessfcns.c **** {
  29              	// {
  30              	// 	HAL_FLASH_Unlock();
  31              	// }
  32              	
  33              	// void flash_deinitialize()
  64:tcas_lessfcns.c ****     Positive_RA_Alt_Thresh[0] = 400;
  34              	// {
  35              	// 	HAL_FLASH_Lock();
  36 0000 064B     	// }
  65:tcas_lessfcns.c ****     Positive_RA_Alt_Thresh[1] = 500;
  37              	
  38 0002 4FF4FA72 	// void flash_erase(uint8_t sector)
  39 0006 4FF4C871 	// {
  40 000a C3E90012 	//     uint32_t error = 0;
  66:tcas_lessfcns.c ****     Positive_RA_Alt_Thresh[2] = 640;
  41              	//     FLASH_EraseInitTypeDef FLASH_EraseInitStruct =
  67:tcas_lessfcns.c ****     Positive_RA_Alt_Thresh[3] = 740;
  42              	//     {
  43 000e 4FF42070 	//     	.TypeErase = FLASH_TYPEERASE_SECTORS,
  44 0012 4FF43972 	// 	.Sector = (uint32_t)sector,
  45 0016 C3E90202 	// 	.NbSectors = 1,
  68:tcas_lessfcns.c **** }
  46              	// 	.VoltageRange = FLASH_VOLTAGE_RANGE_3
  47 001a 7047     	//     };
  48              	
  49              	//     HAL_FLASHEx_Erase(&FLASH_EraseInitStruct,&error);
  50              	// }
  51 001c 00000000 	
  52              	// uint8_t flash_write(volatile uint32_t* address, uint32_t *data, uint16_t size)
  53              	// {
  54              	//    for (int i = 0; i < size; i++)
  55              	//      if (HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, (*address)+(i*4), data[i]) != HAL_OK)
  56              	//     	return 1;
  57              	//    return 0;
  58              	// }
  59              	
  60              	void loop(void) {
  61              	
  62              	    // serial communication init
  63              	    char *ascii_buf;
  64              	    char *tokens;
  69:tcas_lessfcns.c **** 
  70:tcas_lessfcns.c **** //int ALIM ()
  71:tcas_lessfcns.c **** //{
  72:tcas_lessfcns.c **** // return Positive_RA_Alt_Thresh[Alt_Layer_Value];
  73:tcas_lessfcns.c **** //}
  74:tcas_lessfcns.c **** 
  75:tcas_lessfcns.c **** //int Inhibit_Biased_Climb ()
  76:tcas_lessfcns.c **** //{
  77:tcas_lessfcns.c **** //    return (Climb_Inhibit ? Up_Separation + NOZCROSS : Up_Separation);
  78:tcas_lessfcns.c **** //}
  79:tcas_lessfcns.c **** 
  80:tcas_lessfcns.c **** bool Non_Crossing_Biased_Climb(void)
  81:tcas_lessfcns.c **** {
  65              	    char c;
  66              	    int i;
  67              	    int arr[13];
  68              	    int actuation;
  69              	
  82:tcas_lessfcns.c ****     int upward_preferred;
  70              	    ascii_buf = malloc(500*sizeof(char));
  83:tcas_lessfcns.c ****     // int upward_crossing_situation;
  84:tcas_lessfcns.c ****     bool result;
  71              	
  85:tcas_lessfcns.c **** 
  86:tcas_lessfcns.c ****     // upward_preferred = (Climb_Inhibit ? Up_Separation + NOZCROSS : Up_Separation) > Down_Separat
  87:tcas_lessfcns.c ****     if (Climb_Inhibit) 
  72              	
  88:tcas_lessfcns.c ****     {
  89:tcas_lessfcns.c ****         upward_preferred = Up_Separation + NOZCROSS;
  73              	    c = getch();
  74 0000 164B     	    i = 0;
  87:tcas_lessfcns.c ****     {
  75              	    while (c != '\n') {
  76 0002 D3E90421 	        ascii_buf[i] = c;
  77 0006 A1B1     	        c = getch();
  78              	        i++;
  79              	    }
  90:tcas_lessfcns.c ****     }
  91:tcas_lessfcns.c ****     else
  92:tcas_lessfcns.c ****     {
  93:tcas_lessfcns.c ****         upward_preferred = Up_Separation > Down_Separation;
  94:tcas_lessfcns.c ****     }
  95:tcas_lessfcns.c ****     if (upward_preferred)
  80              	    ascii_buf[i] = '\0';
  89:tcas_lessfcns.c ****     }
  81              	
  82 0008 1549     	    tokens = strtok(ascii_buf, " \000");
  89:tcas_lessfcns.c ****     }
  83              	    i = 1;
  84 000a 0968     	    while (tokens != NULL) {
  85              	        arr[i] = atoi(tokens);
  86 000c CA42     	        tokens = strtok(NULL, " \000");
  87 000e 13D1     	        i++;
  88              	    }
  89              	
  90              	    if (i != 13) {
  91              	        putch('e');
  80:tcas_lessfcns.c **** {
  92              	        putch('r');
  93              	        putch('r');
  96:tcas_lessfcns.c ****     {
  97:tcas_lessfcns.c **** 	result = !((Own_Tracked_Alt < Other_Tracked_Alt)) || (((Own_Tracked_Alt < Other_Tracked_Alt)) && (
  98:tcas_lessfcns.c ****     }
  99:tcas_lessfcns.c ****     else
 100:tcas_lessfcns.c ****     {	
 101:tcas_lessfcns.c **** 	result = (Other_Tracked_Alt < Own_Tracked_Alt) && (Cur_Vertical_Sep >= MINSEP) && (Up_Separation >
  94              	        putch('o');
  95              	        putch('r');
  96 0010 D3E90710 	        putch('!');
  97 0014 8842     	        putch('\n');
  98 0016 1EDA     	        return;
  99              	    }
 100 0018 1149     	
 101 001a 986A     	    free(ascii_buf);
 102 001c 4968     	
 103 001e 8842     	
 104 0020 19DB     	    initialize();
 105              	    Cur_Vertical_Sep = arr[1];
 106 0022 596A     	    High_Confidence = arr[2];
 107              	    Two_of_Three_Reports_Valid = arr[3];
 108 0024 53F82100 	    Own_Tracked_Alt = arr[4];
 109 0028 9042     	    Own_Tracked_Alt_Rate = arr[5];
 110 002a CCBF     	    Other_Tracked_Alt = arr[6];
 111 002c 0020     	    Alt_Layer_Value = arr[7];
 112 002e 0120     	    Up_Separation = arr[8];
 113 0030 7047     	    Down_Separation = arr[9];
 114              	    Other_RAC = arr[10];
 115              	    Other_Capability = arr[11];
 116              	    Climb_Inhibit = arr[12];
  93:tcas_lessfcns.c ****     }
 117              	
 118              	
  95:tcas_lessfcns.c ****     {
 119              	    trigger_high();
  95:tcas_lessfcns.c ****     {
 120              	    alt_sep_test();
 121 0032 9969     	    actuation = alt_sep_result + '0';
 122 0034 9142     	    trigger_low();
 123 0036 EBDA     	
 124              	    putch(actuation);
 125              	
  97:tcas_lessfcns.c ****     }
 126              	
  97:tcas_lessfcns.c ****     }
 127              	    // putch(alt_sep_result+'0');
 128 0038 D3E90712 	    putch('\n');
 129 003c 9142     	
 130 003e 08DA     	    putch('d');
  97:tcas_lessfcns.c ****     }
 131              	    putch('o');
 132 0040 5A6A     	    putch('n');
  97:tcas_lessfcns.c ****     }
 133              	    putch('e');
 134 0042 53F82200 	    putch('!');
 135 0046 9B69     	    putch('\n');
 136 0048 9842     	}
 137 004a B4BF     	
 138 004c 0020     	
 139 004e 0120     	int main(void)
 140 0050 7047     	{
 141              	    platform_init();
  97:tcas_lessfcns.c ****     }
 142              	    init_uart();
 143 0052 0120     	    trigger_setup();
 144 0054 7047     	
 145              	    putch('h');
 146              	    putch('e');
 147              	    putch('l');
 148              	    putch('l');
 149 0056 0020     	    putch('o');
 150              	    putch('\n');
 151              	
 152              		simpleserial_init();
 153              	
 102:tcas_lessfcns.c ****     }
 103:tcas_lessfcns.c ****     return result;
 154              	    while(1) 
 104:tcas_lessfcns.c **** }
 155              	    {
 156 0058 7047     	        loop();
 157              	    }
 158 005a 00BF     	}
 159              	...
 105:tcas_lessfcns.c **** 
 106:tcas_lessfcns.c **** bool Non_Crossing_Biased_Descend(void)
 107:tcas_lessfcns.c **** {
 108:tcas_lessfcns.c ****     int upward_preferred;
 109:tcas_lessfcns.c ****     // int upward_crossing_situation;
 110:tcas_lessfcns.c ****     bool result;
 111:tcas_lessfcns.c **** 
 112:tcas_lessfcns.c ****     // upward_preferred = (Climb_Inhibit ? Up_Separation + NOZCROSS : Up_Separation) > Down_Separat
 113:tcas_lessfcns.c ****     if (Climb_Inhibit) 
 114:tcas_lessfcns.c ****     {
 115:tcas_lessfcns.c ****         upward_preferred = Up_Separation + NOZCROSS;
 113:tcas_lessfcns.c ****     {
 116:tcas_lessfcns.c ****     }
 117:tcas_lessfcns.c ****     else
 118:tcas_lessfcns.c ****     {
 119:tcas_lessfcns.c ****         upward_preferred = Up_Separation > Down_Separation;
 120:tcas_lessfcns.c ****     }
 121:tcas_lessfcns.c ****     if (upward_preferred)
 115:tcas_lessfcns.c ****     }
 115:tcas_lessfcns.c ****     }
 122:tcas_lessfcns.c ****     {
 123:tcas_lessfcns.c **** 	result = (Own_Tracked_Alt < Other_Tracked_Alt) && (Cur_Vertical_Sep >= MINSEP) && (Down_Separation
 124:tcas_lessfcns.c ****     }
 125:tcas_lessfcns.c ****     else
 126:tcas_lessfcns.c ****     {
 127:tcas_lessfcns.c **** 	result = !((Other_Tracked_Alt < Own_Tracked_Alt)) || (((Other_Tracked_Alt < Own_Tracked_Alt)) && (
 119:tcas_lessfcns.c ****     }
 121:tcas_lessfcns.c ****     {
 121:tcas_lessfcns.c ****     {
 106:tcas_lessfcns.c **** {
 123:tcas_lessfcns.c ****     }
 123:tcas_lessfcns.c ****     }
 123:tcas_lessfcns.c ****     }
 123:tcas_lessfcns.c ****     }
 123:tcas_lessfcns.c ****     }
 123:tcas_lessfcns.c ****     }
 123:tcas_lessfcns.c ****     }
 128:tcas_lessfcns.c ****     }
 129:tcas_lessfcns.c ****     return result;
 130:tcas_lessfcns.c **** }
 131:tcas_lessfcns.c **** 
 132:tcas_lessfcns.c **** //bool Own_Below_Threat()
 133:tcas_lessfcns.c **** //{
 134:tcas_lessfcns.c **** //    return (Own_Tracked_Alt < Other_Tracked_Alt);
 135:tcas_lessfcns.c **** //}
 136:tcas_lessfcns.c **** 
 137:tcas_lessfcns.c **** //bool Own_Above_Threat()
 138:tcas_lessfcns.c **** //{
 139:tcas_lessfcns.c **** //    return (Other_Tracked_Alt < Own_Tracked_Alt);
 140:tcas_lessfcns.c **** //}
 141:tcas_lessfcns.c **** 
 142:tcas_lessfcns.c **** void alt_sep_test(void)
 143:tcas_lessfcns.c **** {
 144:tcas_lessfcns.c ****     bool enabled, tcas_equipped, intent_not_known;
 145:tcas_lessfcns.c ****     bool need_upward_RA, need_downward_RA;
 146:tcas_lessfcns.c ****     int alt_sep;
 147:tcas_lessfcns.c **** 
 148:tcas_lessfcns.c ****     enabled = High_Confidence && (Own_Tracked_Alt_Rate <= OLEV) && (Cur_Vertical_Sep > MAXALTDIFF);
 143:tcas_lessfcns.c ****     bool enabled, tcas_equipped, intent_not_known;
 149:tcas_lessfcns.c ****     tcas_equipped = Other_Capability == TCAS_TA;
 150:tcas_lessfcns.c ****     if (Two_of_Three_Reports_Valid == 0) {
 151:tcas_lessfcns.c ****         intent_not_known = Two_of_Three_Reports_Valid; 
 152:tcas_lessfcns.c ****     } else {
 153:tcas_lessfcns.c ****         intent_not_known = Two_of_Three_Reports_Valid && Other_RAC == NO_INTENT;
 154:tcas_lessfcns.c ****     }
 155:tcas_lessfcns.c ****     
 156:tcas_lessfcns.c ****     alt_sep = UNRESOLVED;
 157:tcas_lessfcns.c ****     
 158:tcas_lessfcns.c ****     // trigger_low();
 159:tcas_lessfcns.c ****     // putch(alt_sep);
 160:tcas_lessfcns.c **** 
 161:tcas_lessfcns.c ****     if (enabled && ((tcas_equipped && intent_not_known) || !tcas_equipped))
 162:tcas_lessfcns.c ****     {
 163:tcas_lessfcns.c **** 	need_upward_RA = Non_Crossing_Biased_Climb() && (Own_Tracked_Alt < Other_Tracked_Alt);
 164:tcas_lessfcns.c **** 	need_downward_RA = Non_Crossing_Biased_Descend() && (Other_Tracked_Alt < Own_Tracked_Alt);
 165:tcas_lessfcns.c **** 	if (need_upward_RA && need_downward_RA)
 166:tcas_lessfcns.c ****         /* unreachable: requires Own_Below_Threat and Own_Above_Threat
 167:tcas_lessfcns.c ****            to both be true - that requires Own_Tracked_Alt < Other_Tracked_Alt
 168:tcas_lessfcns.c ****            and Other_Tracked_Alt < Own_Tracked_Alt, which isn't possible */
 169:tcas_lessfcns.c **** 	    alt_sep = UNRESOLVED;
 170:tcas_lessfcns.c **** 	else if (need_upward_RA)
 171:tcas_lessfcns.c **** 	    alt_sep = UPWARD_RA;
 172:tcas_lessfcns.c **** 	else if (need_downward_RA)
 173:tcas_lessfcns.c **** 	    alt_sep = DOWNWARD_RA;
 174:tcas_lessfcns.c **** 	else
 175:tcas_lessfcns.c **** 	    alt_sep = UNRESOLVED;
 176:tcas_lessfcns.c ****     }
 177:tcas_lessfcns.c ****     alt_sep_result = alt_sep;
 178:tcas_lessfcns.c **** }
 148:tcas_lessfcns.c ****     tcas_equipped = Other_Capability == TCAS_TA;
 156:tcas_lessfcns.c ****     
 156:tcas_lessfcns.c ****     
 165:tcas_lessfcns.c ****         /* unreachable: requires Own_Below_Threat and Own_Above_Threat
 156:tcas_lessfcns.c ****     
 156:tcas_lessfcns.c ****     
  60:simpleserial-main.c **** void loop(void) {
  63:simpleserial-main.c ****     char *ascii_buf;
  64:simpleserial-main.c ****     char *tokens;
  65:simpleserial-main.c ****     char c;
  66:simpleserial-main.c ****     int i;
  67:simpleserial-main.c ****     int arr[13];
  68:simpleserial-main.c ****     int actuation;
  70:simpleserial-main.c ****     ascii_buf = malloc(500*sizeof(char));
  60:simpleserial-main.c **** void loop(void) {
  70:simpleserial-main.c ****     ascii_buf = malloc(500*sizeof(char));
  60:simpleserial-main.c **** void loop(void) {
  70:simpleserial-main.c ****     ascii_buf = malloc(500*sizeof(char));
  73:simpleserial-main.c ****     c = getch();
  73:simpleserial-main.c ****     c = getch();
  74:simpleserial-main.c ****     i = 0;
  75:simpleserial-main.c ****     while (c != '\n') {
  75:simpleserial-main.c ****     while (c != '\n') {
  80:simpleserial-main.c ****     ascii_buf[i] = '\0';
  80:simpleserial-main.c ****     ascii_buf[i] = '\0';
  82:simpleserial-main.c ****     tokens = strtok(ascii_buf, " \000");
  82:simpleserial-main.c ****     tokens = strtok(ascii_buf, " \000");
  86:simpleserial-main.c ****         tokens = strtok(NULL, " \000");
  82:simpleserial-main.c ****     tokens = strtok(ascii_buf, " \000");
  82:simpleserial-main.c ****     tokens = strtok(ascii_buf, " \000");
  83:simpleserial-main.c ****     i = 1;
  84:simpleserial-main.c ****     while (tokens != NULL) {
  83:simpleserial-main.c ****     i = 1;
  85:simpleserial-main.c ****         arr[i] = atoi(tokens);
  84:simpleserial-main.c ****     while (tokens != NULL) {
  90:simpleserial-main.c ****     if (i != 13) {
  90:simpleserial-main.c ****     if (i != 13) {
  91:simpleserial-main.c ****         putch('e');
  91:simpleserial-main.c ****         putch('e');
  92:simpleserial-main.c ****         putch('r');
  93:simpleserial-main.c ****         putch('r');
  94:simpleserial-main.c ****         putch('o');
  95:simpleserial-main.c ****         putch('r');
 133:simpleserial-main.c ****     putch('e');
 134:simpleserial-main.c ****     putch('!');
 135:simpleserial-main.c ****     putch('\n');
 136:simpleserial-main.c **** }
 135:simpleserial-main.c ****     putch('\n');
  76:simpleserial-main.c ****         ascii_buf[i] = c;
  76:simpleserial-main.c ****         ascii_buf[i] = c;
  77:simpleserial-main.c ****         c = getch();
  77:simpleserial-main.c ****         c = getch();
  78:simpleserial-main.c ****         i++;
  85:simpleserial-main.c ****         arr[i] = atoi(tokens);
  85:simpleserial-main.c ****         arr[i] = atoi(tokens);
  86:simpleserial-main.c ****         tokens = strtok(NULL, " \000");
  85:simpleserial-main.c ****         arr[i] = atoi(tokens);
  86:simpleserial-main.c ****         tokens = strtok(NULL, " \000");
  86:simpleserial-main.c ****         tokens = strtok(NULL, " \000");
  87:simpleserial-main.c ****         i++;
  87:simpleserial-main.c ****         i++;
  87:simpleserial-main.c ****         i++;
 101:simpleserial-main.c ****     free(ascii_buf);
 105:simpleserial-main.c ****     Cur_Vertical_Sep = arr[1];
 101:simpleserial-main.c ****     free(ascii_buf);
 104:simpleserial-main.c ****     initialize();
 105:simpleserial-main.c ****     Cur_Vertical_Sep = arr[1];
 105:simpleserial-main.c ****     Cur_Vertical_Sep = arr[1];
 106:simpleserial-main.c ****     High_Confidence = arr[2];
 106:simpleserial-main.c ****     High_Confidence = arr[2];
 107:simpleserial-main.c ****     Two_of_Three_Reports_Valid = arr[3];
 107:simpleserial-main.c ****     Two_of_Three_Reports_Valid = arr[3];
 108:simpleserial-main.c ****     Own_Tracked_Alt = arr[4];
 108:simpleserial-main.c ****     Own_Tracked_Alt = arr[4];
 109:simpleserial-main.c ****     Own_Tracked_Alt_Rate = arr[5];
 109:simpleserial-main.c ****     Own_Tracked_Alt_Rate = arr[5];
 110:simpleserial-main.c ****     Other_Tracked_Alt = arr[6];
 110:simpleserial-main.c ****     Other_Tracked_Alt = arr[6];
 111:simpleserial-main.c ****     Alt_Layer_Value = arr[7];
 111:simpleserial-main.c ****     Alt_Layer_Value = arr[7];
 112:simpleserial-main.c ****     Up_Separation = arr[8];
 112:simpleserial-main.c ****     Up_Separation = arr[8];
 113:simpleserial-main.c ****     Down_Separation = arr[9];
 113:simpleserial-main.c ****     Down_Separation = arr[9];
 114:simpleserial-main.c ****     Other_RAC = arr[10];
 114:simpleserial-main.c ****     Other_RAC = arr[10];
 115:simpleserial-main.c ****     Other_Capability = arr[11];
 115:simpleserial-main.c ****     Other_Capability = arr[11];
 116:simpleserial-main.c ****     Climb_Inhibit = arr[12];
 116:simpleserial-main.c ****     Climb_Inhibit = arr[12];
 119:simpleserial-main.c ****     trigger_high();
 120:simpleserial-main.c ****     alt_sep_test();
 121:simpleserial-main.c ****     actuation = alt_sep_result + '0';
 121:simpleserial-main.c ****     actuation = alt_sep_result + '0';
 122:simpleserial-main.c ****     trigger_low();
 124:simpleserial-main.c ****     putch(actuation);
 128:simpleserial-main.c ****     putch('\n');
 130:simpleserial-main.c ****     putch('d');
 131:simpleserial-main.c ****     putch('o');
 132:simpleserial-main.c ****     putch('n');
 133:simpleserial-main.c ****     putch('e');
 140:simpleserial-main.c **** {
 141:simpleserial-main.c ****     platform_init();
 140:simpleserial-main.c **** {
 141:simpleserial-main.c ****     platform_init();
 142:simpleserial-main.c ****     init_uart();
 143:simpleserial-main.c ****     trigger_setup();
 145:simpleserial-main.c ****     putch('h');
 146:simpleserial-main.c ****     putch('e');
 147:simpleserial-main.c ****     putch('l');
 148:simpleserial-main.c ****     putch('l');
 149:simpleserial-main.c ****     putch('o');
 150:simpleserial-main.c ****     putch('\n');
 152:simpleserial-main.c **** 	simpleserial_init();
 154:simpleserial-main.c ****     while(1) 
 156:simpleserial-main.c ****         loop();
 154:simpleserial-main.c ****     while(1) 
DEFINED SYMBOLS
                            *ABS*:0000000000000000 simpleserial-main.c
 simpleserial-main.c:18     .text.initialize:0000000000000000 $t
 simpleserial-main.c:26     .text.initialize:0000000000000000 initialize
 simpleserial-main.c:51     .text.initialize:000000000000001c $d
 simpleserial-main.c:56     .text.Non_Crossing_Biased_Climb:0000000000000000 $t
 simpleserial-main.c:63     .text.Non_Crossing_Biased_Climb:0000000000000000 Non_Crossing_Biased_Climb
 simpleserial-main.c:160    .text.Non_Crossing_Biased_Climb:000000000000005c $d
 simpleserial-main.c:166    .text.Non_Crossing_Biased_Descend:0000000000000000 $t
 simpleserial-main.c:173    .text.Non_Crossing_Biased_Descend:0000000000000000 Non_Crossing_Biased_Descend
 simpleserial-main.c:268    .text.Non_Crossing_Biased_Descend:0000000000000054 $d
 simpleserial-main.c:274    .text.alt_sep_test:0000000000000000 $t
 simpleserial-main.c:281    .text.alt_sep_test:0000000000000000 alt_sep_test
 simpleserial-main.c:411    .text.alt_sep_test:000000000000007c $d
 simpleserial-main.c:417    .text.loop:0000000000000000 $t
 simpleserial-main.c:424    .text.loop:0000000000000000 loop
 simpleserial-main.c:687    .text.loop:00000000000000fc $d
 simpleserial-main.c:693    .text.startup.main:0000000000000000 $t
 simpleserial-main.c:700    .text.startup.main:0000000000000000 main
 simpleserial-main.c:814    .bss:0000000000000014 Climb_Inhibit
 simpleserial-main.c:854    .bss:000000000000003c Other_Capability
 simpleserial-main.c:850    .bss:0000000000000038 Other_RAC
 simpleserial-main.c:818    .bss:0000000000000018 Down_Separation
 simpleserial-main.c:810    .bss:0000000000000010 Up_Separation
 simpleserial-main.c:806    .bss:0000000000000000 Positive_RA_Alt_Thresh
 simpleserial-main.c:830    .bss:0000000000000024 Alt_Layer_Value
 simpleserial-main.c:826    .bss:0000000000000020 Other_Tracked_Alt
 simpleserial-main.c:842    .bss:0000000000000030 Own_Tracked_Alt_Rate
 simpleserial-main.c:822    .bss:000000000000001c Own_Tracked_Alt
 simpleserial-main.c:846    .bss:0000000000000034 Two_of_Three_Reports_Valid
 simpleserial-main.c:838    .bss:000000000000002c High_Confidence
 simpleserial-main.c:834    .bss:0000000000000028 Cur_Vertical_Sep
 simpleserial-main.c:787    .data:0000000000000000 NOZCROSS
 simpleserial-main.c:791    .data:0000000000000004 MINSEP
 simpleserial-main.c:799    .data:000000000000000c MAXALTDIFF
 simpleserial-main.c:795    .data:0000000000000008 OLEV
 simpleserial-main.c:858    .bss:0000000000000040 alt_sep_result
 simpleserial-main.c:783    .data:0000000000000000 $d
 simpleserial-main.c:802    .bss:0000000000000000 $d
 simpleserial-main.c:9104   .text.loop:0000000000000104 $d
 simpleserial-main.c:9104   .text.alt_sep_test:0000000000000084 $d
                           .group:0000000000000000 wm4.0.75aa3f87a3295f1a54f386bb6026daaa
                           .group:0000000000000000 wm4.hal.h.20.434d30cf9ff4efcf6c4d61bfe409a912
                           .group:0000000000000000 wm4._newlib_version.h.4.1ef4e12f167f8b69d7c30054be56050d
                           .group:0000000000000000 wm4.features.h.33.5bd1eea2d80518b50f7af0b5ce6750e0
                           .group:0000000000000000 wm4._default_types.h.15.247e5cd201eca3442cbf5404108c4935
                           .group:0000000000000000 wm4._intsup.h.10.48bafbb683905c4daa4565a85aeeb264
                           .group:0000000000000000 wm4._stdint.h.10.c24fa3af3bc1706662bb5593a907e841
                           .group:0000000000000000 wm4.stdint.h.23.d53047a68f4a85177f80b422d52785ed
                           .group:0000000000000000 wm4.hal.h.144.a6ad02c83803dda3733c9d6b559976d1
                           .group:0000000000000000 wm4.ieeefp.h.77.f33a4dce62116f6f5175ff8bae57a54c
                           .group:0000000000000000 wm4.newlib.h.8.44edc94185c26bcddc48010a7181c2d2
                           .group:0000000000000000 wm4.config.h.224.c701144a7b0518c6ee9b9b5465b79f81
                           .group:0000000000000000 wm4._ansi.h.31.de524f58584151836e90d8620a16f8e8
                           .group:0000000000000000 wm4.stdlib.h.13.4ed386f5c1a80d71e72172885d946ef2
                           .group:0000000000000000 wm4.stddef.h.181.13772e73e5434e8cc4fafaaddad2b5da
                           .group:0000000000000000 wm4.stddef.h.39.1bfffcccc3897d82880a055878218da6
                           .group:0000000000000000 wm4._types.h.20.dd0d04dca3800a0d2a6129b87f3adbb2
                           .group:0000000000000000 wm4.stddef.h.155.3588ebfdd1e8c7ede80509bb9c3b8009
                           .group:0000000000000000 wm4._types.h.127.34941de1b2539d59d5cac00e0dd27a45
                           .group:0000000000000000 wm4.reent.h.17.e292bf8b0bec6c96e131a54347145a30
                           .group:0000000000000000 wm4.lock.h.2.1461d1fff82dffe8bfddc23307f6484f
                           .group:0000000000000000 wm4.reent.h.77.dcd6129ff07fe81bd5636db29abe53b2
                           .group:0000000000000000 wm4.cdefs.h.49.3d0fe8ea14e93bda8c589d4f684b21b8
                           .group:0000000000000000 wm4.alloca.h.8.dfc0c703c47ec3e69746825b17d9e66d
                           .group:0000000000000000 wm4.stdlib.h.56.f4862cfbf4363a1db01842d5bdf72c18
                           .group:0000000000000000 wm4.string.h.8.c4b8571ce60dff2817f43fec8b86aecd
                           .group:0000000000000000 wm4.stddef.h.155.ba788add86a0e365f264484f110c3c29
                           .group:0000000000000000 wm4.stdio.h.27.3fc80220048df77954e38daec3bb9670
                           .group:0000000000000000 wm4.stdarg.h.34.3a23a216c0c293b3d2ea2e89281481e6
                           .group:0000000000000000 wm4.types.h.40.8b6acba56cefbb11746718204edc8f5e
                           .group:0000000000000000 wm4._endian.h.31.65a10590763c3dde1ac4a7f66d7d4891
                           .group:0000000000000000 wm4.endian.h.9.49f3a4695c1b61e8a0808de3c4a106cb
                           .group:0000000000000000 wm4._timeval.h.32.bec3221fa7a9bb0bdde696c9c57e47d2
                           .group:0000000000000000 wm4.timespec.h.41.d855182eb0e690443ab8651bcedca6e1
                           .group:0000000000000000 wm4.select.h.19.97ca6fd0c752a0f3b6719fd314d361e6
                           .group:0000000000000000 wm4.types.h.51.5571ec98f267d17d3c670b7a3ba33afa
                           .group:0000000000000000 wm4.sched.h.22.c60982713a5c428609783c78f9c78d95
                           .group:0000000000000000 wm4._pthreadtypes.h.36.fcee9961c35163dde6267ef772ad1972
                           .group:0000000000000000 wm4.stdio.h.2.4aa87247282eca6c8f36f9de33d8df1a
                           .group:0000000000000000 wm4.stdio.h.81.932d0c162786b883f622b8d05c120c78
                           .group:0000000000000000 wm4.tcas_lessfcns.c.45.33ea9667074cfc38824974e1ad988fb0

UNDEFINED SYMBOLS
malloc
getch
strtok
putch
atoi
free
trigger_high
trigger_low
platform_init
init_uart
trigger_setup
simpleserial_init
