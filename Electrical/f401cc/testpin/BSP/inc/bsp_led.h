#ifndef _BSP_LED_H
#define _BSP_LED_H
#include "main.h"
#define LED0_ON() HAL_GPIO_WritePin(EN_PW_GPIO_Port, LED0_Pin, GPIO_PIN_SET)
#define LED0_OFF() HAL_GPIO_WritePin(EN_PW_GPIO_Port, LED0_Pin, GPIO_PIN_RESET)

#endif