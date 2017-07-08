#ifndef __SH1106_H__
#define __SH1106_H__

#include <stdint.h>

///***************************************************************************************************************
// invert - True for inverted display and False for normal.
// contrast - Sets the contrast of the display, valid values are in the range of 0 - 255 (default 128).
// Vpp - Sets the charge pump voltage for the display, 0 = 6.4V (default), 1 = 7.4V, 2 = 8.0V (controller default), 3 = 9.0V
///***************************************************************************************************************
void sh1106_begin(int invert, uint8_t contrast, uint8_t Vpp);
void sh1106_clear(void);
uint8_t sh1106_goto(uint8_t x, uint8_t y);
void sh1106_write_str(char* str);
uint32_t sh1106_write(uint8_t uint8_t);
uint8_t sh1106_write_bitmap(const uint8_t *bitmap, uint8_t x, uint8_t y, uint8_t width, uint8_t height);

#endif
