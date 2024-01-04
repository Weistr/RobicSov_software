#ifndef _BSP_UART_H
#define _BSP_UART_H
#include "main.h"

extern uint8_t uart2RxBuf[];
extern uint8_t uart2TxBuf[];
extern uint8_t uart2RxLen;
extern uint16_t uart2TimoutCnt;
extern uint8_t uart1RxBuf[];
extern uint8_t uart1TxBuf[];
extern uint16_t uart1RxLen;
extern uint16_t uart1TimoutCnt;
void uart_init(void);
void uartPrintString(UART_HandleTypeDef *huart, char* str);
void uartWiteDataToBuffer(uint8_t* datain, uint8_t len);
void uartTrigSend(void);
void uartTrigSendStr(void);
#define uart1MaxLen 600
#define uart1TxMaxLen 128
#define uart2MaxLen 64
#endif
