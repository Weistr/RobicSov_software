#include "opiCom.h"
#include "bsp_uart.h"
#include "usart.h"
#include "crc16modbus.h"
#include "string.h"
#include "cubeMotion.h"
/**
 * OPi收发任务
*/
/**OPI选择模式*/
uint8_t originMod = 0;

int16_t crcCal,crcRcv;
uint8_t packTimeOutCnt = 0;
uint16_t packStrCnt = 0;
uint8_t OpiUartRcvFlag = 0;

void OpiUartTask()
{
	if(packStrCnt==0)memset(actionSerialStr,0,actionStrLenMax);
	packTimeOutCnt = 0;
	OpiUartRcvFlag = 1;
	if(packStrCnt > actionStrLenMax)packStrCnt=0;
	memcpy(&actionSerialStr[packStrCnt],uart1RxBuf,uart1RxLen);
	packStrCnt += uart1RxLen;
}

uint16_t packLen=0,packLenPrevious=0;

void OpiRcvTask()
{
	if(packTimeOutCnt < 5)
	{
		__nop();
		packTimeOutCnt++;
	}
	else if(OpiUartRcvFlag == 1)
	{
		OpiUartRcvFlag = 0;
		packLenPrevious = packLen;
		packLen = packStrCnt;
		packStrCnt = 0;
		/**如果首字符为0-4则为透传模式*/
		if(actionSerialStr[0] < 4)
		{
			__nop();
			__nop();
			HAL_UART_Transmit_DMA(&huart2,(uint8_t*)actionSerialStr,packLen);
			originMod = 1;
			goto ENDLINE;
		}	
		/*CRC校验*/
		crcCal = crc16Cal((uint8_t *)&actionSerialStr[0], packLen-2); // 校验CRC
		crcRcv = (actionSerialStr[packLen-2] << 8) + actionSerialStr[packLen-1];
		if (crcCal != crcRcv)
		{
			uartWiteDataToBuffer((uint8_t*)"\r\ncrcError!",11);
			uartTrigSendStr();
			goto ENDLINE;
		}
		else if(memcmp(actionSerialStr,"backRcv",7)==0)
		{
			uartWiteDataToBuffer((uint8_t*)"\r\nrcvLen:",9);
			char sbuf[3];
			sbuf[0] = packLenPrevious/100+'0';
			sbuf[1] = packLenPrevious%100/10+'0';
			sbuf[2] = packLenPrevious%100%10+'0';
			uartWiteDataToBuffer((uint8_t*)sbuf,3);			
			uartWiteDataToBuffer((uint8_t*)"\r\nactCnt:",9);
			sbuf[0] = cubeStrStepCord/100+'0';
			sbuf[1] = cubeStrStepCord%100/10+'0';
			sbuf[2] = cubeStrStepCord%100%10+'0';
			uartWiteDataToBuffer((uint8_t*)sbuf,3);	
			
			uartWiteDataToBuffer((uint8_t*)"\r\nraw:",6);	
		}
		/**动作串模式*/
		else if(
			((packLen >= 5) && ((packLen-2)%3 == 0)) &&
			((actionSerialStr[0]=='L')||(actionSerialStr[0]=='R')) &&
			((actionSerialStr[1]=='W')||(actionSerialStr[1]=='G'))
			)
		{
			uartWiteDataToBuffer((uint8_t*)"\r\nserialAction: ",16);
			if(serialActionStartFlag == 0)//
			{
				
				uint8_t serialTestResult = serialConfict_Test((char*)actionSerialStr,packLen-2,
				roboGripper[0].status,
				roboGripper[1].status,
				roboWrist[0].status,
				roboWrist[1].status);
				if(serialTestResult == serialAction_checkCode_OK || serialTestResult == serialAction_checkCode_warning_sameRcv)
				{	
					if(serialTestResult == serialAction_checkCode_OK)
						uartWiteDataToBuffer((uint8_t*)"ok",2);
					else if(serialTestResult == serialAction_checkCode_warning_sameRcv)
						uartWiteDataToBuffer((uint8_t*)"warning: have same action!",26);
							
					//memset(actionSerialStr,0,actionStrLenMax);
					//memcpy(actionSerialStr,uart1RxBuf,packLen-2);
					serialActionStart();
				}
				else if(serialTestResult == serialAction_checkCode_error_90degCof)
				{
					uartWiteDataToBuffer((uint8_t*)"error: wrist conflict!",22);
				}
				else if(serialTestResult == serialAction_checkCode_error_illgelChar)
				{
					uartWiteDataToBuffer((uint8_t*)"error: illgel char!",19);
				}
				else if(serialTestResult == serialAction_checkCode_error_enptyRotate)
				{
					uartWiteDataToBuffer((uint8_t*)"error: enpty rotate!",19);
				}
				else if(serialTestResult == serialAction_checkCode_error_open2Gri)
				{
					uartWiteDataToBuffer((uint8_t*)"error: 2 Gripper open!",19);
				}

				uartTrigSendStr();			
			}
			else 
			{
				uartWiteDataToBuffer((uint8_t*)"error: motor busy!",19);
				uartTrigSendStr();	
				goto ENDLINE;
			}
			
			
		}
		else 
		{
				uartWiteDataToBuffer((uint8_t*)"\r\nerror: illeagel mod!",22);
				uartTrigSendStr();				
		}

	}
	
	ENDLINE:
		__nop();
}
