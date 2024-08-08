#include "bsp_adc.h"
#include "adc.h"
#include "bsp_adc.h"
uint16_t adc_buf[5];

void adc_init()
{
	
}

void adcDMAstart()
{
	HAL_ADC_Start_DMA(&hadc1,(uint32_t*)adc_buf,5);
}
