/* Define memory regions. */
MEMORY
{
	rom (rx) : ORIGIN = 0x08000000, LENGTH = 128K
	ram (rwx) : ORIGIN = 0x20000000, LENGTH = 16K
}

/* Include the common ld script. */
INCLUDE libopencm3_stm32f0.ld
