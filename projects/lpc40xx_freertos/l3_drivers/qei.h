#pragma once

#include <stdint.h>

typedef enum {
  INX_INT = 0,
  TIM_INT,
  VELC_INT,
  DIR_INT,
  ERR_INT,
  ENCLK_INT,
  POS0_INT,
  POS1_INT,
  POS2_INT,
  REV0_INT,
  POS0REV_INT,
  POS1REV_INT,
  POS2REV_INT,
  REV1_INT,
  REV2_INT,
  MAXPOS_INT,
} qei_interrupt_number;

void qei_init(uint32_t max_pos);
void qei_reset_position(void);
uint32_t qei_get_position(void);

void qei_enable_interrupt(qei_interrupt_number inter_num);
void qei_clear_interrupt(qei_interrupt_number inter_num);
