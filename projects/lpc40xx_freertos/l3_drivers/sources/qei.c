#include <stdint.h>
#include <stdio.h>

#include "qei.h"

#include "lpc40xx.h"

void qei_init(uint32_t max_pos) {
  LPC_SC->PCONP |= (1 << 18); // set QEI bit in PCONP register to power QEI

  LPC_QEI->CONF &= ~(1 << 1); // clear SIGMODE bit to enable quadrature phase mode
  LPC_QEI->CONF |= (1 << 2);  // set capmode

  LPC_QEI->CON |= (1 << 0);  // set RESP bit of the configuration register to reset position
  LPC_QEI->CON &= ~(1 << 0); // clear RESP bit of the configuration register

  LPC_QEI->MAXPOS = (max_pos & 0xFFFFFFFF);        // set max pos to 1 foot = 850 ticks
  LPC_QEI->CMPOS0 = ((max_pos >> 1) & 0xFFFFFFFF); // set compare0 for a 1/2 of maxpos
}

void qei_reset_position(void) {
  LPC_QEI->CON |= (1 << 0);  // set RESP bit of the configuration register to reset position
  LPC_QEI->CON &= ~(1 << 0); // clear RESP bit of the configuration register
}

uint32_t qei_get_position(void) {
  uint32_t result = 33;
  result = (LPC_QEI->POS & 0xFFFFFFFF);

  return (result);
}

void qei_enable_interrupt(qei_interrupt_number inter_num) { LPC_QEI->IES &= (1 << inter_num); }

void qei_clear_interrupt(qei_interrupt_number inter_num) { LPC_QEI->CLR |= (1 << inter_num); }