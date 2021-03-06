/***********************************************************************************************************************
 * This file was generated by the MCUXpresso Config Tools. Any manual edits made to this file
 * will be overwritten if the respective MCUXpresso Config Tools is used to update this file.
 **********************************************************************************************************************/
/*
 * How to setup clock using clock driver functions:
 *
 * 1. CLOCK_SetSimSafeDivs, to make sure core clock, bus clock, flexbus clock
 *    and flash clock are in allowed range during clock mode switch.
 *
 * 2. Call CLOCK_Osc0Init to setup OSC clock, if it is used in target mode.
 *
 * 3. Set MCG configuration, MCG includes three parts: FLL clock, PLL clock and
 *    internal reference clock(MCGIRCLK). Follow the steps to setup:
 *
 *    1). Call CLOCK_BootToXxxMode to set MCG to target mode.
 *
 *    2). If target mode is FBI/BLPI/PBI mode, the MCGIRCLK has been configured
 *        correctly. For other modes, need to call CLOCK_SetInternalRefClkConfig
 *        explicitly to setup MCGIRCLK.
 *
 *    3). Don't need to configure FLL explicitly, because if target mode is FLL
 *        mode, then FLL has been configured by the function CLOCK_BootToXxxMode,
 *        if the target mode is not FLL mode, the FLL is disabled.
 *
 *    4). If target mode is PEE/PBE/PEI/PBI mode, then the related PLL has been
 *        setup by CLOCK_BootToXxxMode. In FBE/FBI/FEE/FBE mode, the PLL could
 *        be enabled independently, call CLOCK_EnablePll0 explicitly in this case.
 *
 * 4. Call CLOCK_SetSimConfig to set the clock configuration in SIM.
 */

/* clang-format off */
/* TEXT BELOW IS USED AS SETTING FOR TOOLS *************************************
!!GlobalInfo
product: Clocks v4.1
processor: MK82FN256xxx15
package_id: MK82FN256VLQ15
mcu_data: ksdk2_0
processor_version: 4.0.1
 * BE CAREFUL MODIFYING THIS COMMENT - IT IS YAML SETTINGS FOR TOOLS **********/
/* clang-format on */

#include "clock_config.h"

/*******************************************************************************
 * Definitions
 ******************************************************************************/
#define MCG_IRCLK_DISABLE                                 0U  /*!< MCGIRCLK disabled */
#define MCG_PLL_DISABLE                                   0U  /*!< MCGPLLCLK disabled */
#define OSC_CAP0P                                         0U  /*!< Oscillator 0pF capacitor load */
#define SIM_LPUART_CLK_SEL_OSCERCLK_CLK                   2U  /*!< LPUART clock select: OSCERCLK clock */
#define SIM_OSC32KSEL_OSC32KCLK_CLK                       0U  /*!< OSC32KSEL select: OSC32KCLK clock */
#define SIM_PLLFLLSEL_MCGFLLCLK_CLK                       0U  /*!< PLLFLL select: MCGFLLCLK clock */
#define SIM_TRACE_CLK_DIV_1                               0U  /*!< Trace clock divider divisor: divided by 1 */
#define SIM_TRACE_CLK_FRAC_1                              0U  /*!< Trace clock divider fraction: multiplied by 1 */
#define SIM_TRACE_CLK_SEL_CORE_SYSTEM_CLK                 1U  /*!< Trace clock select: Core/system clock */

/*******************************************************************************
 * Variables
 ******************************************************************************/
/* System clock frequency. */
extern uint32_t SystemCoreClock;

/*******************************************************************************
 * Code
 ******************************************************************************/
/*FUNCTION**********************************************************************
 *
 * Function Name : CLOCK_CONFIG_FllStableDelay
 * Description   : This function is used to delay for FLL stable.
 *
 *END**************************************************************************/
static void CLOCK_CONFIG_FllStableDelay(void)
{
    uint32_t i = 30000U;
    while (i--)
    {
        __NOP();
    }
}

/*******************************************************************************
 ************************ BOARD_InitBootClocks function ************************
 ******************************************************************************/
void BOARD_InitBootClocks(void)
{
    BOARD_BootClockRUN();
}

/*******************************************************************************
 ********************** Configuration BOARD_BootClockRUN ***********************
 ******************************************************************************/
/* clang-format off */
/* TEXT BELOW IS USED AS SETTING FOR TOOLS *************************************
!!Configuration
name: BOARD_BootClockRUN
called_from_default_init: true
outputs:
- {id: Bus_clock.outFreq, value: 7.37 MHz}
- {id: Core_clock.outFreq, value: 7.37 MHz}
- {id: Flash_clock.outFreq, value: 7.37 MHz}
- {id: FlexBus_clock.outFreq, value: 7.37 MHz}
- {id: LPO_clock.outFreq, value: 1 kHz}
- {id: LPUARTCLK.outFreq, value: 7.37 MHz}
- {id: MCGFFCLK.outFreq, value: 57.578125/2 kHz}
- {id: MCGFLLCLK.outFreq, value: 21.07359375 MHz}
- {id: OSCERCLK.outFreq, value: 7.37 MHz}
- {id: OSCERCLK_UNDIV.outFreq, value: 7.37 MHz}
- {id: PLLFLLCLK.outFreq, value: 21.07359375 MHz}
- {id: System_clock.outFreq, value: 7.37 MHz}
- {id: TRACECLKIN.outFreq, value: 7.37 MHz}
settings:
- {id: MCGMode, value: FBE}
- {id: LPUARTClkConfig, value: 'yes'}
- {id: MCG.CLKS.sel, value: MCG.OSCSEL}
- {id: MCG.FLL_mul.scale, value: '732'}
- {id: MCG.FRDIV.scale, value: '256'}
- {id: MCG.IREFS.sel, value: MCG.FRDIV}
- {id: MCG_C2_RANGE0_CFG, value: High}
- {id: MCG_C2_RANGE0_FRDIV_CFG, value: High}
- {id: OSC_CR_ERCLKEN_CFG, value: Enabled}
- {id: OSC_CR_ERCLKEN_UNDIV_CFG, value: Enabled}
- {id: OSC_CR_EREFSTEN_CFG, value: Enabled}
- {id: OSC_CR_EREFSTEN_UNDIV_CFG, value: Enabled}
- {id: SIM.LPUARTSRCSEL.sel, value: OSC.OSCERCLK}
- {id: SIM.OUTDIV3.scale, value: '1', locked: true}
- {id: SIM.OUTDIV4.scale, value: '1', locked: true}
- {id: TraceClkConfig, value: 'yes'}
sources:
- {id: OSC.OSC.outFreq, value: 7.37 MHz, enabled: true}
 * BE CAREFUL MODIFYING THIS COMMENT - IT IS YAML SETTINGS FOR TOOLS **********/
/* clang-format on */

/*******************************************************************************
 * Variables for BOARD_BootClockRUN configuration
 ******************************************************************************/
const mcg_config_t mcgConfig_BOARD_BootClockRUN =
    {
        .mcgMode = kMCG_ModeFBE,                  /* FBE - FLL Bypassed External */
        .irclkEnableMode = MCG_IRCLK_DISABLE,     /* MCGIRCLK disabled */
        .ircs = kMCG_IrcSlow,                     /* Slow internal reference clock selected */
        .fcrdiv = 0x1U,                           /* Fast IRC divider: divided by 2 */
        .frdiv = 0x3U,                            /* FLL reference clock divider: divided by 256 */
        .drs = kMCG_DrsLow,                       /* Low frequency range */
        .dmx32 = kMCG_Dmx32Fine,                  /* DCO is fine-tuned for maximum frequency with 32.768 kHz reference */
        .oscsel = kMCG_OscselOsc,                 /* Selects System Oscillator (OSCCLK) */
        .pll0Config =
            {
                .enableMode = MCG_PLL_DISABLE,    /* MCGPLLCLK disabled */
                .prdiv = 0x0U,                    /* PLL Reference divider: divided by 1 */
                .vdiv = 0x0U,                     /* VCO divider: multiplied by 16 */
            },
    };
const sim_clock_config_t simConfig_BOARD_BootClockRUN =
    {
        .pllFllSel = SIM_PLLFLLSEL_MCGFLLCLK_CLK, /* PLLFLL select: MCGFLLCLK clock */
        .pllFllDiv = 0,                           /* PLLFLLSEL clock divider divisor: divided by 1 */
        .pllFllFrac = 0,                          /* PLLFLLSEL clock divider fraction: multiplied by 1 */
        .er32kSrc = SIM_OSC32KSEL_OSC32KCLK_CLK,  /* OSC32KSEL select: OSC32KCLK clock */
        .clkdiv1 = 0x0U,                          /* SIM_CLKDIV1 - OUTDIV1: /1, OUTDIV2: /1, OUTDIV3: /1, OUTDIV4: /1 */
    };
const osc_config_t oscConfig_BOARD_BootClockRUN =
    {
        .freq = 7370000U,                         /* Oscillator frequency: 7370000Hz */
        .capLoad = (OSC_CAP0P),                   /* Oscillator capacity load: 0pF */
        .workMode = kOSC_ModeExt,                 /* Use external clock */
        .oscerConfig =
            {
                .enableMode = kOSC_ErClkEnable | kOSC_ErClkEnableInStop,/* Enable external reference clock, enable external reference clock in STOP mode */
                .erclkDiv = 0,                    /* Divider for OSCERCLK: divided by 1 */
            }
    };

/*******************************************************************************
 * Code for BOARD_BootClockRUN configuration
 ******************************************************************************/
void BOARD_BootClockRUN(void)
{
    /* Set the system clock dividers in SIM to safe value. */
    CLOCK_SetSimSafeDivs();
    /* Initializes OSC0 according to board configuration. */
    CLOCK_InitOsc0(&oscConfig_BOARD_BootClockRUN);
    CLOCK_SetXtal0Freq(oscConfig_BOARD_BootClockRUN.freq);
    /* Set MCG to FBE mode. */
    CLOCK_SetExternalRefClkConfig(mcgConfig_BOARD_BootClockRUN.oscsel);
    CLOCK_SetFbeMode(mcgConfig_BOARD_BootClockRUN.frdiv,
                     mcgConfig_BOARD_BootClockRUN.dmx32,
                     mcgConfig_BOARD_BootClockRUN.drs,
                     CLOCK_CONFIG_FllStableDelay);
    /* Set the clock configuration in SIM module. */
    CLOCK_SetSimConfig(&simConfig_BOARD_BootClockRUN);
    /* Set SystemCoreClock variable. */
    SystemCoreClock = BOARD_BOOTCLOCKRUN_CORE_CLOCK;
    /* Set LPUART clock source. */
    CLOCK_SetLpuartClock(SIM_LPUART_CLK_SEL_OSCERCLK_CLK);
    /* Set debug trace clock source. */
    CLOCK_SetTraceClock(SIM_TRACE_CLK_SEL_CORE_SYSTEM_CLK, SIM_TRACE_CLK_DIV_1, SIM_TRACE_CLK_FRAC_1);
}

