#include "XdriveCom.h"
#include "bsp_uart.h"
#include "usart.h"
#include "string.h"
#include "crc16modbus.h"

#include "cubeMotion.h"
#include "stdbool.h"

/**
 * 电机位置速度控制
*/
void motorPosControl(uint8_t id, int32_t pos, int32_t speed)
{
  memset(uart2TxBuf, 0, 32);
  uart2TxBuf[0] = id;   // id
  uart2TxBuf[1] = 0x20; // mod
  memcpy(&uart2TxBuf[2], (uint8_t *)&pos, 4);
  memcpy(&uart2TxBuf[6], (uint8_t *)&speed, 4);
  uint16_t crc = crc16Cal((uint8_t *)&uart2TxBuf[0], 10);
  uart2TxBuf[10] = BYTE1(crc);
  uart2TxBuf[11] = BYTE0(crc);
  HAL_UART_Transmit_DMA(&huart2,(uint8_t *)&uart2TxBuf[0], 12);
}

void motorSpeedControl(uint8_t id, int32_t speed)
{
  uart2TxBuf[0] = id;
  uart2TxBuf[1] = 0x21;
  uart2TxBuf[2] = BYTE0(speed);
  uart2TxBuf[3] = BYTE1(speed);
  uart2TxBuf[4] = BYTE2(speed);
  uart2TxBuf[5] = BYTE3(speed);
  int16_t crc = crc16Cal((uint8_t *)&uart2TxBuf[0], 6);
  uart2TxBuf[6] = BYTE1(crc);
  uart2TxBuf[7] = BYTE0(crc);
  HAL_UART_Transmit_DMA(&huart2,(uint8_t *)&uart2TxBuf[0], 8);
}

void motorCurrControl(uint8_t id, int16_t Curr)
{
  uart2TxBuf[0] = id;
  uart2TxBuf[1] = 0x22;
  uart2TxBuf[2] = BYTE0(Curr);
  uart2TxBuf[3] = BYTE1(Curr);
  int16_t crc = crc16Cal((uint8_t *)&uart2TxBuf[0], 4);
  uart2TxBuf[4] = BYTE1(crc);
  uart2TxBuf[5] = BYTE0(crc);
  HAL_UART_Transmit_DMA(&huart2,(uint8_t *)&uart2TxBuf[0], 6);
}

void motorStop(uint8_t id)
{
  uart2TxBuf[0] = id;
  uart2TxBuf[1] = 0x10;
  int16_t crc = crc16Cal((uint8_t *)&uart2TxBuf[0], 2);
  uart2TxBuf[2] = BYTE1(crc);
  uart2TxBuf[3] = BYTE0(crc);
  HAL_UART_Transmit_DMA(&huart2,(uint8_t *)&uart2TxBuf[0], 4);
}
void motorRcvStatusUpdate(uint8_t id)
{
  uart2TxBuf[0] = id;
  uart2TxBuf[1] = 0xFF;
  int16_t crc = crc16Cal((uint8_t *)&uart2TxBuf[0], 2);
  uart2TxBuf[2] = BYTE1(crc);
  uart2TxBuf[3] = BYTE0(crc);
  HAL_UART_Transmit_DMA(&huart2,(uint8_t *)&uart2TxBuf[0], 4);
}


int32_t XdPosRcv,XdSpeedRcv;

extern uint8_t originMod;
bool xdRcvFinsh_Falg = 0;

void XdriveRcvTask(void)
{
	uint8_t idRcv;
			if (originMod == 1)
			{
				originMod=0;
				HAL_UART_Transmit_DMA(&huart1,uart2RxBuf,uart2RxLen);
			}
			else
			{
				int16_t crcCal = crc16Cal(uart2RxBuf,10);
				int16_t crcRcv = (uart2RxBuf[10]<<8) + uart2RxBuf[11];
				if(crcCal == crcRcv)
				{
					xdRcvFinsh_Falg = 1;
					idRcv = uart2RxBuf[0];
					memcpy(&XdPosRcv,&uart2RxBuf[2],4);
					memcpy(&XdSpeedRcv,&uart2RxBuf[6],4);
					if(idRcv == roboGripper[0].motorid)
					{
						roboGripper[0].posNow = XdPosRcv;
						roboGripper[0].speedNow = XdSpeedRcv;
					}
					else if(idRcv == roboGripper[1].motorid)
					{
						roboGripper[1].posNow = XdPosRcv;
						roboGripper[1].speedNow = XdSpeedRcv;
					}					
					#if(wrist_motor_type == xdrive_motor)
					else if(idRcv == roboWrist[0].motorid)
					{
						__nop();
						roboWrist[0].posNow = XdPosRcv;
						roboWrist[0].speedNow = XdSpeedRcv;
					}
					else if(idRcv == roboWrist[1].motorid)
					{
						roboWrist[1].posNow = XdPosRcv;
						roboWrist[1].speedNow = XdSpeedRcv;
					}
					#endif
				}
			}
		
}

























