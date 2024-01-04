#include "bsp_led.h"
#include "stdbool.h"
uint8_t LED_MODE = LED0blinkONE;
void led_sta_update_20ms()
{
	static uint8_t led_cnt=0;
	static bool led_sta;//1: on 0:off
	switch(LED_MODE)
	{
		case LED0constOFF:
			LED0_OFF();
			break;
		case LED0constON:
			LED0_ON();
			break;
		case LED0blinkONE:
			led_cnt++;
			if(led_cnt > 25)
			{
				led_cnt = 0;
				led_sta = !led_sta;
			}
			if(led_sta)
				LED0_ON();
			else
				LED0_OFF();
			break;
		case LED0blinkWithCycle:
			led_sta = !led_sta;
			if(led_sta)
				LED0_ON();
			else
				LED0_OFF();			
			break;
	}
}
