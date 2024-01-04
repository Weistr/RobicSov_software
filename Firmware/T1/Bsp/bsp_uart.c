#include "usart.h"
#include "bsp_uart.h"
#include "user_main.h"

#include "bsp_uart.h"
#include "string.h"
#include "bsp_delay.h"
#include "bsp_led.h"
#include "motionPlanter.h"
#include "OpiCom.h"
#include "zdt_motorCom.h"
//========================================================================
// 函数: 
// 描述: 串口相关.
// 参数: None.
// 返回: None.
//========================================================================
uint8_t uart2RxBuf[uart2MaxLen];
uint8_t uart2TxBuf[uart2MaxLen];
uint8_t uart2RxLen;


uint8_t uart1RxBuf[uart1MaxLen];
uint8_t uart1TxBuf[uart1TxMaxLen];
uint16_t uart1RxLen;
void uart_init()
{
	HAL_UARTEx_ReceiveToIdle_DMA(&huart2,uart2RxBuf,uart2MaxLen);
	__HAL_UART_ENABLE_IT(&huart2,UART_IT_IDLE);
	HAL_UARTEx_ReceiveToIdle_DMA(&huart1,uart1RxBuf,uart1MaxLen);
	__HAL_UART_ENABLE_IT(&huart1,UART_IT_IDLE);
	
}

void XdriveRcvTask(void);

//串口接收完成中断回调函数
void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *huart, uint16_t Size)
{
	if (huart->Instance == USART1)
	{
		HAL_UARTEx_ReceiveToIdle_DMA(huart, uart1RxBuf, uart1MaxLen);
		uart1RxLen = Size;
		OpiUartTask();
	}	
	if (huart->Instance == USART2)
	{
		HAL_UARTEx_ReceiveToIdle_DMA(huart, uart2RxBuf, uart2MaxLen);
		uart2RxLen = Size;
		XdriveRcvTask();
		zdt_uartRcv();
	}	
}




uint8_t strCnt = 0;

void uartWiteDataToBuffer(uint8_t* datain, uint8_t len)
{
	if(strCnt == 0)memset(uart1TxBuf,0,uart1TxMaxLen);
	if((strCnt + len)>(uart1TxMaxLen-5))strCnt=0;
	memcpy(&uart1TxBuf[strCnt],datain,len);
	strCnt+=len;
}


void uartTrigSendStr()
{
	HAL_UART_Transmit_DMA(&huart1,(uint8_t *)&uart1TxBuf[0], strCnt);
	strCnt = 0;
}
void HAL_UART_ErrorCallback(UART_HandleTypeDef *huart)
{

		MX_USART1_UART_Init();
		MX_USART2_UART_Init();
		
		uart_init();
		//HAL_Delay(20);
	
}






