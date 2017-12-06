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
  //rcc_clock_setup_in_hsi_out_48mhz();
  rcc_osc_on(RCC_HSI48);
  rcc_wait_for_osc_ready(RCC_HSI48);

  rcc_set_hpre(RCC_CFGR_HPRE_NODIV);
  rcc_set_ppre(RCC_CFGR_PPRE_NODIV);

  flash_set_ws(FLASH_ACR_LATENCY_024_048MHZ);

  rcc_set_sysclk_source(RCC_HSI48);

  //rcc_apb1_frequency = 48000000;
  //rcc_ahb_frequency = 48000000;


  rcc_periph_clock_enable(RCC_GPIOA);
  rcc_periph_clock_enable(RCC_GPIOB);
  rcc_periph_clock_enable(RCC_GPIOC);
  rcc_periph_clock_enable(RCC_GPIOF);
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

uint8_t quokka[] = {0,0,0,0,0,0,128,240,252,126,111,47,59,6,60,48,224,192,64,96,96,96,96,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,252,254,182,253,93,16,0,0,224,224,96,0,0,0,0,14,27,17,109,63,31,49,96,64,192,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,127,248,217,217,112,128,128,199,207,139,15,6,128,128,128,96,112,30,15,0,0,0,0,0,0,1,1,3,6,12,24,48,96,192,128,0,0,0,0,0,0,0,0,0,0,0,0,224,253,7,129,129,249,255,153,113,249,253,231,255,112,224,192,0,0,0,0,4,252,224,0,0,0,0,0,0,0,0,0,0,3,15,56,224,128,0,0,0,0,0,0,0,0,1,7,28,183,238,89,243,119,254,255,123,108,196,199,65,224,240,120,56,28,30,27,24,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,31,127,192,3,31,119,199,7,7,15,15,30,255,129,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,127,31,0,0,0,0,24,30,22,59,59,43,35,35,34,35,35,34,226,243,155,220,92,88,216,153,155,148,152,152,144,176,176,144,184,176,144,176,240,16,24,24,60,102,195,131,6,12,24,48,224,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,97,97,97,225,224,160,160,160,176,176,176,152,140,199,64,96,48,56,28,7};

int main(void) {
  clock_setup();
  gpio_setup();

  //systick_setup(1);

  for (int j = 0; j < 20; ++j) {
    gpio_toggle(GPIOC, GPIO13);
    gpio_toggle(GPIOC, GPIO14);
    gpio_toggle(GPIOC, GPIO15);
    for (volatile int i = 0; i < 200000; ++i) {
      __asm__("nop");
    }
  }

  sh1106_begin(0, 255, 3);
  sh1106_goto(0, 6);
  sh1106_write_str("hello, world!");

  sh1106_write_bitmap(quokka, 128-46, 0, 46, 8);

  while (1) {
    sh1106_goto(0, 0);
    if (!gpio_get(GPIOB, GPIO12)) {
      sh1106_write('a');
    } else {
      sh1106_write(' ');
    }
    if (!gpio_get(GPIOC, GPIO6)) {
      sh1106_write('b');
    } else {
      sh1106_write(' ');
    }
    if (!gpio_get(GPIOC, GPIO8)) {
      sh1106_write('c');
    } else {
      sh1106_write(' ');
    }
    if (!gpio_get(GPIOC, GPIO9)) {
      sh1106_write('d');
    } else {
      sh1106_write(' ');
    }
    gpio_toggle(GPIOC, GPIO14);
    for (int i = 0; i < 200000; i++) {
      __asm__("nop");
    }
  }
}
