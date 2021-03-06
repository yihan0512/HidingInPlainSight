/* This file is based on the excellent LUFA Library, which is:
  Copyright (C) Dean Camera, 2013. See www.lufa-lib.org
  
  Note it has been modified for the SAM3U by NewAE Technology Inc.,
  changes Copyright (C) NewAE Technology Inc, 2015. Changes have
  generally basterdized and reduced the functionality of the original
  code, so please see original code if using this to port. 
*/

/*
  Copyright 2013  Dean Camera (dean [at] fourwalledcubicle [dot] com)

  Permission to use, copy, modify, distribute, and sell this
  software and its documentation for any purpose is hereby granted
  without fee, provided that the above copyright notice appear in
  all copies and that both that the copyright notice and this
  permission notice and warranty disclaimer appear in supporting
  documentation, and that the name of the author not be used in
  advertising or publicity pertaining to distribution of the
  software without specific, written prior permission.

  The author disclaims all warranties with regard to this
  software, including all implied warranties of merchantability
  and fitness.  In no event shall the author be liable for any
  special, indirect or consequential damages or any damages
  whatsoever resulting from loss of use, data or profits, whether
  in an action of contract, negligence or other tortious action,
  arising out of or in connection with the use or performance of
  this software.
*/

/** \file
 *
 *  Header file for ISPProtocol.c.
 */

#ifndef _ISP_PROTOCOL_
#define _ISP_PROTOCOL_

	/* Includes: */
		#include <asf.h>
		#include "delay.h"
		#include "V2Protocol.h"

	/* Macros: */
		/** Mask for the reading or writing of the high byte in a FLASH word when issuing a low-level programming command. */
		#define READ_WRITE_HIGH_BYTE_MASK       (1 << 3)

		#define PROG_MODE_PAGED_WRITES_MASK     (1 << 0)
		#define PROG_MODE_WORD_TIMEDELAY_MASK   (1 << 1)
		#define PROG_MODE_WORD_VALUE_MASK       (1 << 2)
		#define PROG_MODE_WORD_READYBUSY_MASK   (1 << 3)
		#define PROG_MODE_PAGED_TIMEDELAY_MASK  (1 << 4)
		#define PROG_MODE_PAGED_VALUE_MASK      (1 << 5)
		#define PROG_MODE_PAGED_READYBUSY_MASK  (1 << 6)
		#define PROG_MODE_COMMIT_PAGE_MASK      (1 << 7)

	/* Function Prototypes: */
		void ISPProtocol_EnterISPMode(void);
		void ISPProtocol_LeaveISPMode(void);
		void ISPProtocol_ProgramMemory(const uint8_t V2Command, uint8_t * buffer);
		void ISPProtocol_ReadMemory(const uint8_t V2Command, uint8_t * buffer);
		void ISPProtocol_ChipErase(void);
		void ISPProtocol_ReadFuseLockSigOSCCAL(const uint8_t V2Command);
		void ISPProtocol_WriteFuseLock(const uint8_t V2Command);
		void ISPProtocol_SPIMulti(void);
		void ISPProtocol_DelayMS(uint8_t DelayMS);
#endif

