#ifndef _BSP_LED_H
#define _BSP_LED_H
#include "main.h"
#define LED0_ON() HAL_GPIO_WritePin(LED0_GPIO_Port, LED0_Pin, GPIO_PIN_SET)
#define LED0_OFF() HAL_GPIO_WritePin(LED0_GPIO_Port, LED0_Pin, GPIO_PIN_RESET)
#define LED0constOFF 0
#define LED0constON 1
#define LED0blinkONE 2
#define LED0blinkWithCycle 3
void led_sta_update_20ms(void);
extern uint8_t LED_MODE;

#endif
