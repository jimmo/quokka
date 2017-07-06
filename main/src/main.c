#include <libopencm3/cm3/cortex.h>
#include <libopencm3/stm32/flash.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/syscfg.h>
#include <libopencm3/stm32/timer.h>
#include <libopencm3/cm3/nvic.h>
#include <libopencm3/cm3/systick.h>
#include <libopencm3/cm3/vector.h>

#include "sh1106.h"

void sys_tick_handler(void) {
  gpio_toggle(GPIOC, GPIO13);
}

static void systick_setup(int hz) {
  cm_disable_interrupts();
  systick_set_frequency(hz, rcc_ahb_frequency);
  systick_interrupt_enable();
  systick_counter_enable();
  cm_enable_interrupts();
}

static void clock_setup(void) {
  rcc_clock_setup_in_hsi_out_48mhz();
  rcc_periph_clock_enable(RCC_GPIOA);
  rcc_periph_clock_enable(RCC_GPIOB);
  rcc_periph_clock_enable(RCC_GPIOC);
}

static void gpio_setup(void) {
  gpio_mode_setup(GPIOC, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO13);
  gpio_mode_setup(GPIOC, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO14);
  gpio_mode_setup(GPIOC, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO15);

  gpio_mode_setup(GPIOB, GPIO_MODE_INPUT, GPIO_PUPD_NONE, GPIO12);
  gpio_mode_setup(GPIOC, GPIO_MODE_INPUT, GPIO_PUPD_NONE, GPIO6);
  gpio_mode_setup(GPIOC, GPIO_MODE_INPUT, GPIO_PUPD_NONE, GPIO8);
  gpio_mode_setup(GPIOC, GPIO_MODE_INPUT, GPIO_PUPD_NONE, GPIO9);

  gpio_clear(GPIOC, GPIO13);
  gpio_clear(GPIOC, GPIO14);
  gpio_clear(GPIOC, GPIO15);
}

int main(void) {
  clock_setup();
  gpio_setup();

  systick_setup(1);

  sh1106_begin(false, 128, 0);

  while (1) {
    sh1106_gotoXY(0, 0);
    if (!gpio_get(GPIOB, GPIO12)) {
      sh1106_write('a');
    } else {
      sh1106_write('_');
    }
    if (!gpio_get(GPIOC, GPIO6)) {
      sh1106_write('b');
    } else {
      sh1106_write('_');
    }
    if (!gpio_get(GPIOC, GPIO8)) {
      sh1106_write('c');
    } else {
      sh1106_write('_');
    }
    if (!gpio_get(GPIOC, GPIO9)) {
      sh1106_write('d');
    } else {
      sh1106_write('_');
    }
    gpio_toggle(GPIOC, GPIO14);
    for (int i = 0; i < 200000; i++) {
      __asm__("nop");
    }
  }
}
