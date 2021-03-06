/* seed_sbox.c */
/*
    This file is part of the AVR-Crypto-Lib.
    Copyright (C) 2008  Daniel Otte (daniel.otte@rub.de)

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
/**
 * \file	seed_sbox.c
 * \author	Daniel Otte 
 * \date	2007-06-1
 * \brief 	sboxes and constants for seed
 * \par License	
 * GPL
 * 
 */

#include <stdint.h>
#include <avr/pgmspace.h>

const uint8_t seed_sbox1[256] PROGMEM ={
	169,  133,  214,  211,   84,   29,  172,   37, 
	 93,   67,   24,   30,   81,  252,  202,   99, 
	 40,   68,   32,  157,  224,  226,  200,   23, 
	165,  143,    3,  123,  187,   19,  210,  238, 
	112,  140,   63,  168,   50,  221,  246,  116, 
	236,  149,   11,   87,   92,   91,  189,    1, 
	 36,   28,  115,  152,   16,  204,  242,  217, 
	 44,   231, 114,  131,  155,  209,  134,  201, 
	 96,   80,  163,  235,   13,  182,  158,   79, 
	183,   90,  198,  120,  166,   18,  175,  213, 
	 97,  195,  180,   65,   82,  125,  141,    8, 
	 31,  153,    0,   25,    4,   83,  247,  225, 
	253,  118,   47,   39,  176,  139,   14,  171, 
	162,  110,  147,   77,  105,  124,    9,   10, 
	191,  239,  243,  197,  135,   20,  254,  100, 
	222,   46,   75,   26,    6,   33,  107,  102, 
	  2,  245,  146,  138,   12,  179,  126,  208, 
	122,   71,  150,  229,   38,  128,  173,  223, 
	161,   48,   55,  174,   54,   21,   34,   56, 
	244,  167,   69,   76,  129,  233,  132,  151, 
	 53,  203,  206,   60,  113,   17,  199,  137, 
	117,  251,  218,  248,  148,   89,  130,  196, 
	255,   73,   57,  103,  192,  207,  215,  184, 
	 15,  142,   66,   35,  145,  108,  219,  164, 
	 52,  241,   72,  194,  111,   61,   45,   64, 
	190,   62,  188,  193,  170,  186,   78,   85, 
	 59,  220,  104,  127,  156,  216,   74,   86, 
	119,  160,  237,   70,  181,   43,  101,  250, 
	227,  185,  177,  159,   94,  249,  230,  178, 
	 49,  234,  109,   95,  228,  240,  205,  136, 
	 22,   58,   88,  212,   98,   41,    7,   51, 
	232,   27,    5,  121,  144,  106,   42,  154
};

const uint8_t seed_sbox2[256] PROGMEM ={
	 56,  232,   45,  166,  207,  222,  179,  184, 
	175,   96,   85,  199,   68,  111,  107,   91, 
	195,   98,   51,  181,   41,  160,  226,  167, 
	211,  145,   17,    6,   28,  188,   54,   75, 
	239,  136,  108,  168,   23,  196,   22,  244, 
	194,   69,  225,  214,   63,   61,  142,  152, 
	 40,   78,  246,   62,  165,  249,   13,  223, 
	216,   43,  102,  122,   39,   47,  241,  114, 
	 66,  212,   65,  192,  115,  103,  172,  139, 
	247,  173,  128,   31,  202,   44,  170,   52, 
	210,   11,  238,  233,   93,  148,   24,  248, 
	 87,  174,    8,  197,   19,  205,  134,  185, 
	255,  125,  193,   49,  245,  138,  106,  177, 
	209,   32,  215,    2,   34,    4,  104,  113, 
	  7,  219,  157,  153,   97,  190,  230,   89, 
	221,   81,  144,  220,  154,  163,  171,  208, 
	129,   15,   71,   26,  227,  236,  141,  191, 
	150,  123,   92,  162,  161,   99,   35,   77, 
	200,  158,  156,   58,   12,   46,  186,  110, 
	159,   90,  242,  146,  243,   73,  120,  204, 
	 21,  251,  112,  117,  127,   53,   16,    3, 
	100,  109,  198,  116,  213,  180,  234,    9, 
	118,   25,  254,   64,   18,  224,  189,    5, 
	250,    1,  240,   42,   94,  169,   86,   67, 
	133,   20,  137,  155,  176,  229,   72,  121, 
	151,  252,   30,  130,   33,  140,   27,   95, 
	119,   84,  178,   29,   37,   79,    0,   70, 
	237,   88,   82,  235,  126,  218,  201,  253, 
	 48,  149,  101,   60,  182,  228,  187,  124, 
	 14,   80,   57,   38,   50,  132,  105,  147, 
	 55,  231,   36,  164,  203,   83,   10,  135, 
	217,   76,  131,  143,  206,   59,   74,  183 
};

/* key constants */
const uint32_t seed_kc[16] PROGMEM ={
	0xb979379e, 
	0x73f36e3c,
	0xe6e6dd78, 
	0xcccdbbf1, 
	0x999b77e3, 
	0x3337efc6, 
	0x676ede8d, 
	0xcfdcbc1b, 
	0x9eb97937,
	0x3c73f36e,	
	0x78e6e6dd,
	0xf1cccdbb,
	0xe3999b77,
	0xc63337ef,
	0x8d676ede,
	0x1bcfdcbc
};

