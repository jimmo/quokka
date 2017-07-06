#include <libopencm3/cm3/cortex.h>
#include <libopencm3/stm32/flash.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/syscfg.h>
#include <libopencm3/stm32/timer.h>
#include <libopencm3/cm3/nvic.h>
#include <libopencm3/cm3/systick.h>

void sys_tick_handler(void) {
  gpio_toggle(GPIOA, GPIO9);
}

static void systick_setup(int hz) {
  cm_disable_interrupts();
  systick_set_frequency(hz, rcc_ahb_frequency);
  systick_interrupt_enable();
  systick_counter_enable();
  cm_enable_interrupts();
}

static void clock_setup(void) {
  rcc_clock_setup_in_hse_8mhz_out_48mhz();
  rcc_periph_clock_enable(RCC_GPIOA);
  rcc_periph_clock_enable(RCC_GPIOC);
}

static void gpio_setup(void) {
  gpio_mode_setup(GPIOA, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO9);
}

static void mco_setup(void) {
  // Set PA8 to "alternate function 0" (i.e. PA8=MCO).
  gpio_mode_setup(GPIOA, GPIO_MODE_AF, GPIO_PUPD_NONE, GPIO8);
  gpio_set_output_options(GPIOA, GPIO_OTYPE_PP, GPIO_OSPEED_100MHZ, GPIO8);
  gpio_set_af(GPIOA, 0, GPIO8);
  rcc_set_mco(RCC_CFGR_MCO_PLL);
}

int main(void) {
  clock_setup();
  gpio_setup();
  mco_setup();

  systick_setup(1);

  gpio_set(GPIOA, GPIO9);

  while (1) {
    //gpio_toggle(GPIOA, GPIO9);
    for (int i = 0; i < 200000; i++) {
      __asm__("nop");
    }
  }
}
