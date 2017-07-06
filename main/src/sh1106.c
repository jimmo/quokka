#include "sh1106.h"

#include <memory.h>

#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/spi.h>

// When DC is '1' the LCD expects data, when it is '0' it expects a command.
#define SH1106_COMMAND		0
#define SH1106_DATA		1

// You may find a different size screen, but this one is 128 by 64 pixels
#define SH1106_X_PIXELS		128
#define SH1106_Y_PIXELS		64
#define SH1106_ROWS			8

// Functions gotoXY, writeBitmap, renderString, writeLine and writeRect
// will return SH1106_SUCCESS if they succeed and SH1106_ERROR if they fail.
#define SH1106_SUCCESS		1
#define SH1106_ERROR		0

uint8_t sh1106_m_Column = 0;
uint8_t sh1106_m_Line = 0;


//This table contains the hex values that represent pixels
//for a font that is 5 pixels wide and 8 pixels high
static const uint8_t ASCII[][5] = {
  { 0x00, 0x00, 0x00, 0x00, 0x00 } // 20   (space)
  ,{ 0x00, 0x00, 0x5f, 0x00, 0x00 } // 21 !
  ,{ 0x00, 0x07, 0x00, 0x07, 0x00 } // 22 "
  ,{ 0x14, 0x7f, 0x14, 0x7f, 0x14 } // 23 #
  ,{ 0x24, 0x2a, 0x7f, 0x2a, 0x12 } // 24 $
  ,{ 0x23, 0x13, 0x08, 0x64, 0x62 } // 25 %
  ,{ 0x36, 0x49, 0x55, 0x22, 0x50 } // 26 &
  ,{ 0x00, 0x05, 0x03, 0x00, 0x00 } // 27 '
  ,{ 0x00, 0x1c, 0x22, 0x41, 0x00 } // 28 (
  ,{ 0x00, 0x41, 0x22, 0x1c, 0x00 } // 29 )
  ,{ 0x14, 0x08, 0x3e, 0x08, 0x14 } // 2a *
  ,{ 0x08, 0x08, 0x3e, 0x08, 0x08 } // 2b +
  ,{ 0x00, 0x50, 0x30, 0x00, 0x00 } // 2c ,
  ,{ 0x08, 0x08, 0x08, 0x08, 0x08 } // 2d -
  ,{ 0x00, 0x60, 0x60, 0x00, 0x00 } // 2e .
  ,{ 0x20, 0x10, 0x08, 0x04, 0x02 } // 2f /
  ,{ 0x3e, 0x51, 0x49, 0x45, 0x3e } // 30 0
  ,{ 0x00, 0x42, 0x7f, 0x40, 0x00 } // 31 1
  ,{ 0x42, 0x61, 0x51, 0x49, 0x46 } // 32 2
  ,{ 0x21, 0x41, 0x45, 0x4b, 0x31 } // 33 3
  ,{ 0x18, 0x14, 0x12, 0x7f, 0x10 } // 34 4
  ,{ 0x27, 0x45, 0x45, 0x45, 0x39 } // 35 5
  ,{ 0x3c, 0x4a, 0x49, 0x49, 0x30 } // 36 6
  ,{ 0x01, 0x71, 0x09, 0x05, 0x03 } // 37 7
  ,{ 0x36, 0x49, 0x49, 0x49, 0x36 } // 38 8
  ,{ 0x06, 0x49, 0x49, 0x29, 0x1e } // 39 9
  ,{ 0x00, 0x36, 0x36, 0x00, 0x00 } // 3a :
  ,{ 0x00, 0x56, 0x36, 0x00, 0x00 } // 3b ;
  ,{ 0x08, 0x14, 0x22, 0x41, 0x00 } // 3c <
  ,{ 0x14, 0x14, 0x14, 0x14, 0x14 } // 3d =
  ,{ 0x00, 0x41, 0x22, 0x14, 0x08 } // 3e >
  ,{ 0x02, 0x01, 0x51, 0x09, 0x06 } // 3f ?
  ,{ 0x32, 0x49, 0x79, 0x41, 0x3e } // 40 @
  ,{ 0x7e, 0x11, 0x11, 0x11, 0x7e } // 41 A
  ,{ 0x7f, 0x49, 0x49, 0x49, 0x36 } // 42 B
  ,{ 0x3e, 0x41, 0x41, 0x41, 0x22 } // 43 C
  ,{ 0x7f, 0x41, 0x41, 0x22, 0x1c } // 44 D
  ,{ 0x7f, 0x49, 0x49, 0x49, 0x41 } // 45 E
  ,{ 0x7f, 0x09, 0x09, 0x09, 0x01 } // 46 F
  ,{ 0x3e, 0x41, 0x49, 0x49, 0x7a } // 47 G
  ,{ 0x7f, 0x08, 0x08, 0x08, 0x7f } // 48 H
  ,{ 0x00, 0x41, 0x7f, 0x41, 0x00 } // 49 I
  ,{ 0x20, 0x40, 0x41, 0x3f, 0x01 } // 4a J
  ,{ 0x7f, 0x08, 0x14, 0x22, 0x41 } // 4b K
  ,{ 0x7f, 0x40, 0x40, 0x40, 0x40 } // 4c L
  ,{ 0x7f, 0x02, 0x0c, 0x02, 0x7f } // 4d M
  ,{ 0x7f, 0x04, 0x08, 0x10, 0x7f } // 4e N
  ,{ 0x3e, 0x41, 0x41, 0x41, 0x3e } // 4f O
  ,{ 0x7f, 0x09, 0x09, 0x09, 0x06 } // 50 P
  ,{ 0x3e, 0x41, 0x51, 0x21, 0x5e } // 51 Q
  ,{ 0x7f, 0x09, 0x19, 0x29, 0x46 } // 52 R
  ,{ 0x46, 0x49, 0x49, 0x49, 0x31 } // 53 S
  ,{ 0x01, 0x01, 0x7f, 0x01, 0x01 } // 54 T
  ,{ 0x3f, 0x40, 0x40, 0x40, 0x3f } // 55 U
  ,{ 0x1f, 0x20, 0x40, 0x20, 0x1f } // 56 V
  ,{ 0x3f, 0x40, 0x38, 0x40, 0x3f } // 57 W
  ,{ 0x63, 0x14, 0x08, 0x14, 0x63 } // 58 X
  ,{ 0x07, 0x08, 0x70, 0x08, 0x07 } // 59 Y
  ,{ 0x61, 0x51, 0x49, 0x45, 0x43 } // 5a Z
  ,{ 0x00, 0x7f, 0x41, 0x41, 0x00 } // 5b [
  ,{ 0x02, 0x04, 0x08, 0x10, 0x20 } // 5c backslash
  ,{ 0x00, 0x41, 0x41, 0x7f, 0x00 } // 5d ]
  ,{ 0x04, 0x02, 0x01, 0x02, 0x04 } // 5e ^
  ,{ 0x40, 0x40, 0x40, 0x40, 0x40 } // 5f _
  ,{ 0x00, 0x01, 0x02, 0x04, 0x00 } // 60 `
  ,{ 0x20, 0x54, 0x54, 0x54, 0x78 } // 61 a
  ,{ 0x7f, 0x48, 0x44, 0x44, 0x38 } // 62 b
  ,{ 0x38, 0x44, 0x44, 0x44, 0x20 } // 63 c
  ,{ 0x38, 0x44, 0x44, 0x48, 0x7f } // 64 d
  ,{ 0x38, 0x54, 0x54, 0x54, 0x18 } // 65 e
  ,{ 0x08, 0x7e, 0x09, 0x01, 0x02 } // 66 f
  ,{ 0x0c, 0x52, 0x52, 0x52, 0x3e } // 67 g
  ,{ 0x7f, 0x08, 0x04, 0x04, 0x78 } // 68 h
  ,{ 0x00, 0x44, 0x7d, 0x40, 0x00 } // 69 i
  ,{ 0x20, 0x40, 0x44, 0x3d, 0x00 } // 6a j
  ,{ 0x7f, 0x10, 0x28, 0x44, 0x00 } // 6b k
  ,{ 0x00, 0x41, 0x7f, 0x40, 0x00 } // 6c l
  ,{ 0x7c, 0x04, 0x18, 0x04, 0x78 } // 6d m
  ,{ 0x7c, 0x08, 0x04, 0x04, 0x78 } // 6e n
  ,{ 0x38, 0x44, 0x44, 0x44, 0x38 } // 6f o
  ,{ 0x7c, 0x14, 0x14, 0x14, 0x08 } // 70 p
  ,{ 0x08, 0x14, 0x14, 0x18, 0x7c } // 71 q
  ,{ 0x7c, 0x08, 0x04, 0x04, 0x08 } // 72 r
  ,{ 0x48, 0x54, 0x54, 0x54, 0x20 } // 73 s
  ,{ 0x04, 0x3f, 0x44, 0x40, 0x20 } // 74 t
  ,{ 0x3c, 0x40, 0x40, 0x20, 0x7c } // 75 u
  ,{ 0x1c, 0x20, 0x40, 0x20, 0x1c } // 76 v
  ,{ 0x3c, 0x40, 0x30, 0x40, 0x3c } // 77 w
  ,{ 0x44, 0x28, 0x10, 0x28, 0x44 } // 78 x
  ,{ 0x0c, 0x50, 0x50, 0x50, 0x3c } // 79 y
  ,{ 0x44, 0x64, 0x54, 0x4c, 0x44 } // 7a z
  ,{ 0x00, 0x08, 0x36, 0x41, 0x00 } // 7b {
  ,{ 0x00, 0x00, 0x7f, 0x00, 0x00 } // 7c |
  ,{ 0x00, 0x41, 0x36, 0x08, 0x00 } // 7d }
  ,{ 0x10, 0x08, 0x08, 0x10, 0x08 } // 7e ~
  ,{ 0x78, 0x46, 0x41, 0x46, 0x78 } // 7f DEL
};

void nop_delay(void);
void sh1106_advanceXY(uint8_t columns);
void sh1106_writeLcdBuf(uint8_t dataOrCommand, const uint8_t *data, uint16_t count);
void sh1106_writeLcd(uint8_t dataOrCommand, uint8_t data);

void nop_delay(void) {
  for (int i = 0; i < 2; i++) {
    __asm__("nop");
  }
}

void sh1106_spi_init2(void);
void sh1106_spi_init(void);

void sh1106_spi_init2(void) {
  rcc_periph_clock_enable(RCC_SPI2);

  gpio_mode_setup(GPIOB, GPIO_MODE_AF, GPIO_PUPD_NONE, GPIO13 | GPIO15);
  gpio_set_output_options(GPIOB, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, GPIO13 | GPIO15);
  gpio_set_af(GPIOA, 0, GPIO13 | GPIO15);

  gpio_mode_setup(GPIOB, GPIO_MODE_AF, GPIO_PUPD_NONE, GPIO14);
  gpio_set_af(GPIOB, 0, GPIO14);

  spi_reset(SPI2);

  /* Set up SPI in Master mode with:
   * Clock baud rate: 1/64 of peripheral clock frequency
   * Clock polarity: Idle High
   * Clock phase: Data valid on 2nd clock pulse
   * Data frame format: 8-bit
   * Frame format: MSB First
   */
  spi_init_master(SPI2, SPI_CR1_BAUDRATE_FPCLK_DIV_64, SPI_CR1_CPOL_CLK_TO_1_WHEN_IDLE, SPI_CR1_CPHA_CLK_TRANSITION_1, SPI_CR1_CRCL_8BIT, SPI_CR1_MSBFIRST);

  /*
   * Set NSS management to software.
   *
   * Note:
   * Setting nss high is very important, even if we are controlling the GPIO
   * ourselves this bit needs to be at least set to 1, otherwise the spi
   * peripheral will not send any data out.
   */
  spi_enable_software_slave_management(SPI2);
  spi_set_nss_high(SPI2);

  /* Enable SPI1 periph. */
  spi_enable(SPI2);
}

void sh1106_spi_init(void) {

  gpio_mode_setup(GPIOB, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO13 | GPIO15);
  gpio_set_output_options(GPIOB, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, GPIO13 | GPIO15);

  gpio_set(GPIOB, GPIO13);}


void spi_bit(int n);

void spi_bit(int n) {
  gpio_clear(GPIOB, GPIO13);
  if (n) {
    gpio_set(GPIOB, GPIO15);
  } else {
    gpio_clear(GPIOB, GPIO15);
  }
  //nop_delay();
  gpio_set(GPIOB, GPIO13);
  //nop_delay();
}

void sh1106_begin(int invert, uint8_t contrast, uint8_t Vpp) {
  sh1106_spi_init();

  for (int i = 0; i < 1000; ++i) {
    nop_delay();
  }

  // CS
  gpio_mode_setup(GPIOB, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO1);
  gpio_set(GPIOB, GPIO1); // CS

  //SPI.begin();
  //if (fastSpi)
  //  SPI.setClockDivider(SPI_CLOCK_DIV2);
  // LCD init section:

  uint8_t invertSetting = invert ? 0xA7 : 0xA6;
  Vpp &= 0x03;

  // Must reset LCD first!
  //SH1106_PORT &= ~PIN_RESET;
  //delay(1);
  //SH1106_PORT |= PIN_RESET;


  sh1106_writeLcd(SH1106_COMMAND, 0xAE);    /*display off*/
  sh1106_writeLcd(SH1106_COMMAND, 0x02);    /*set lower column address*/
  sh1106_writeLcd(SH1106_COMMAND, 0x10);    /*set higher column address*/
  sh1106_writeLcd(SH1106_COMMAND, 0x40);    /*set display start line*/
  sh1106_writeLcd(SH1106_COMMAND, 0xB0);    /*set page address*/
  sh1106_writeLcd(SH1106_COMMAND, 0x81);    /*contract control*/
  sh1106_writeLcd(SH1106_COMMAND, contrast);    /*128*/
  sh1106_writeLcd(SH1106_COMMAND, 0xA1);    /*set segment remap*/
  sh1106_writeLcd(SH1106_COMMAND, invertSetting);    /*normal / reverse*/
  sh1106_writeLcd(SH1106_COMMAND, 0xA8);    /*multiplex ratio*/
  sh1106_writeLcd(SH1106_COMMAND, 0x3F);    /*duty = 1/32*/
  sh1106_writeLcd(SH1106_COMMAND, 0xAD);    /*set charge pump enable*/
  sh1106_writeLcd(SH1106_COMMAND, 0x8B);     /*external VCC   */
  sh1106_writeLcd(SH1106_COMMAND, 0x30 | Vpp);    /*0X30---0X33  set VPP   9V liangdu!!!!*/
  sh1106_writeLcd(SH1106_COMMAND, 0xC8);    /*Com scan direction*/
  sh1106_writeLcd(SH1106_COMMAND, 0xD3);    /*set display offset*/
  sh1106_writeLcd(SH1106_COMMAND, 0x00);   /*   0x20  */
  sh1106_writeLcd(SH1106_COMMAND, 0xD5);    /*set osc division*/
  sh1106_writeLcd(SH1106_COMMAND, 0x80);
  sh1106_writeLcd(SH1106_COMMAND, 0xD9);    /*set pre-charge period*/
  sh1106_writeLcd(SH1106_COMMAND, 0x1F);    /*0x22*/
  sh1106_writeLcd(SH1106_COMMAND, 0xDA);    /*set COM pins*/
  sh1106_writeLcd(SH1106_COMMAND, 0x12);
  sh1106_writeLcd(SH1106_COMMAND, 0xDB);    /*set vcomh*/
  sh1106_writeLcd(SH1106_COMMAND, 0x40);
  sh1106_writeLcd(SH1106_COMMAND, 0xAF);    /*display ON*/

  sh1106_clear();
}

uint32_t sh1106_write(uint8_t data)
{
  // Non-ASCII characters are not supported.
  if (data < 0x20 || data > 0x7F) return 0;
  if (sh1106_m_Column >= 123)
    sh1106_advanceXY(SH1106_X_PIXELS - sh1106_m_Column);

  uint8_t buf[6];
  memcpy(buf, ASCII[data - 0x20], 5);
  buf[5] = 0x00;
  sh1106_writeLcdBuf(SH1106_DATA, buf, 6);
  sh1106_advanceXY(6);
  return 1;
}

void sh1106_clear(void)
{
  for (uint8_t j = SH1106_ROWS; j > 0; j--)
    {
      sh1106_gotoXY(0, j-1);
      for (uint8_t i = SH1106_X_PIXELS; i > 0; i--)
        sh1106_writeLcd(SH1106_DATA, 0x00);
    }
  sh1106_gotoXY(0, 0);
}

uint8_t sh1106_gotoXY(uint8_t x, uint8_t y)
{
  if (x >= SH1106_X_PIXELS || y >= SH1106_ROWS) return SH1106_ERROR;
  sh1106_m_Column = x;
  sh1106_m_Line = y;
  x = x + 2;										// Panel is 128 pixels wide, controller RAM has space for 132,
  // it's centered so add an offset to ram address.

  sh1106_writeLcd(SH1106_COMMAND, 0xB0 + y);		// Set row
  sh1106_writeLcd(SH1106_COMMAND, x & 0xF);		// Set lower column address
  sh1106_writeLcd(SH1106_COMMAND, 0x10 | (x >> 4));// Set higher column address
  return SH1106_SUCCESS;
}

uint8_t sh1106_writeBitmap(const uint8_t *bitmap, uint8_t x, uint8_t y, uint8_t width, uint8_t height)
{
  if (sh1106_gotoXY(x, y) == SH1106_ERROR) return SH1106_ERROR;
  const uint8_t *maxY = bitmap + height * width;

  for (const uint8_t *by = bitmap; by < maxY; by += width)
    {
      sh1106_writeLcdBuf(SH1106_DATA, by , width);
      sh1106_gotoXY(sh1106_m_Column, sh1106_m_Line + 1);
    }

  sh1106_advanceXY(width);
  return SH1106_SUCCESS;
}

void sh1106_advanceXY(uint8_t columns)
{
  sh1106_m_Column += columns;
  if (sh1106_m_Column >= SH1106_X_PIXELS)
    {
      sh1106_m_Column %= SH1106_X_PIXELS;
      sh1106_m_Line++;
      sh1106_m_Line %= SH1106_ROWS;
      sh1106_gotoXY(sh1106_m_Column, sh1106_m_Line);
    }
}

void sh1106_writeLcdBuf(uint8_t dataOrCommand, const uint8_t *data, uint16_t count)
{
      gpio_clear(GPIOB, GPIO1); // ~CS

  for (uint16_t i = count; i > 0; i--)
    {
      spi_bit(dataOrCommand);
      for (uint8_t x = 0; x < 8; ++x) {
        spi_bit(data[count-i] & (1 << (7-x)));
      }
      //spi_send8(SPI2, dataOrCommand);
      //spi_send8(SPI2, data[count-i]);
    }
      gpio_set(GPIOB, GPIO1); // CS
      nop_delay();
}

void sh1106_writeLcd(uint8_t dataOrCommand, uint8_t data)
{
  gpio_clear(GPIOB, GPIO1); // ~CS
  //spi_send8(SPI2, dataOrCommand);
  //spi_send8(SPI2, data);
  spi_bit(dataOrCommand);
  for (uint8_t x = 0; x < 8; ++x) {
    spi_bit(data & (1 << (7-x)));
  }
  gpio_set(GPIOB, GPIO1); // CS
  nop_delay();
}
