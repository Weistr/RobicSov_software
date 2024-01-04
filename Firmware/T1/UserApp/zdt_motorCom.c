#include "zdt_motorCom.h"
#include "bsp_uart.h"
#include "usart.h"
#include "cubeMotion.h"
zdtMotorTypedef zdtMotor[2]={
//id    rstpos  EncoderVal  speed  pos   pose cmdstatus
	{3,   64163,      },
	{2,   3262,      }
};



uint8_t xorCal(uint8_t* in, uint8_t len)
{
    uint8_t rt = 0;
    for (uint8_t i = 0; i < len; i++)
    {
        rt ^= in[i];
    }
    return rt;
}
void zdt_motorEnanleCtl(uint8_t id,uint8_t choice)
{
	uart2TxBuf[0] = id;
	uart2TxBuf[1] = 0xF3;
	uart2TxBuf[2] = 0xAB;
    uart2TxBuf[3] = choice;
    uart2TxBuf[4] = 0;
    uart2TxBuf[5] = xorCal(uart2TxBuf,5);
    HAL_UART_Transmit_DMA(&huart2,(uint8_t *)&uart2TxBuf[0], 6);
}

void zdt_motorTrackCtl(uint8_t id, int32_t pos,int16_t acc_P,int16_t acc_N,int16_t spdpss)
{
	uart2TxBuf[0] = id;
	uart2TxBuf[1] = 0xFD;
    if(pos>0)
    {
        uart2TxBuf[2] = 0x01;
    }
	else 
    {
        uart2TxBuf[2] = 0x00;
        pos = -pos;
    }

    uart2TxBuf[3] = BYTE1(acc_P);
    uart2TxBuf[4] = BYTE0(acc_P);
    uart2TxBuf[5] = BYTE1(acc_N);
    uart2TxBuf[6] = BYTE0(acc_N);
    uart2TxBuf[7] = BYTE1(spdpss);
    uart2TxBuf[8] = BYTE0(spdpss);

    uart2TxBuf[9] = BYTE3(pos);
    uart2TxBuf[10] = BYTE2(pos);
    uart2TxBuf[11] = BYTE1(pos);
    uart2TxBuf[12] = BYTE0(pos);
    
    uart2TxBuf[13] = 1;
    uart2TxBuf[14] = 0;
		
    uart2TxBuf[15] = xorCal(uart2TxBuf,15);
    HAL_UART_Transmit_DMA(&huart2,(uint8_t *)&uart2TxBuf[0], 16);
}

void zdt_zeroPosTrig(uint8_t id)
{
		uart2TxBuf[0] = id;
		uart2TxBuf[1] = 0x9A;
		uart2TxBuf[2] = 0;
    uart2TxBuf[3] = 0;
    uart2TxBuf[4] = xorCal(uart2TxBuf,4);
    HAL_UART_Transmit_DMA(&huart2,(uint8_t *)&uart2TxBuf[0], 5);
}
void zdt_zeroPosSet(uint8_t id,uint8_t save)
{
		uart2TxBuf[0] = id;
		uart2TxBuf[1] = 0x93;
		uart2TxBuf[2] = 0x88;
    uart2TxBuf[3] = save;
    uart2TxBuf[4] = xorCal(uart2TxBuf,4);
    HAL_UART_Transmit_DMA(&huart2,(uint8_t *)&uart2TxBuf[0], 5);
}
void zdt_readSpeed(uint8_t id)
{
		uart2TxBuf[0] = id;
		uart2TxBuf[1] = 0x35;
    uart2TxBuf[2] = xorCal(uart2TxBuf,2);
    HAL_UART_Transmit_DMA(&huart2,(uint8_t *)&uart2TxBuf[0], 3);
}
void zdt_readPos(uint8_t id)
{
		uart2TxBuf[0] = id;
		uart2TxBuf[1] = 0x36;
    uart2TxBuf[2] = xorCal(uart2TxBuf,2);
    HAL_UART_Transmit_DMA(&huart2,(uint8_t *)&uart2TxBuf[0], 3);
}
void zdt_readPosError(uint8_t id)
{
		uart2TxBuf[0] = id;
		uart2TxBuf[1] = 0x37;
    uart2TxBuf[2] = xorCal(uart2TxBuf,2);
    HAL_UART_Transmit_DMA(&huart2,(uint8_t *)&uart2TxBuf[0], 3);
}

void zdt_readEncoderVal(uint8_t id)
{
		uart2TxBuf[0] = id;
		uart2TxBuf[1] = 0x31;
    uart2TxBuf[2] = xorCal(uart2TxBuf,2);
    HAL_UART_Transmit_DMA(&huart2,(uint8_t *)&uart2TxBuf[0], 3);
}

uint8_t xorRcv,xorCalVal;

void zdt_uartRcv()
{
#if(wrist_motor_type == zdt_motor)
	
	
	//id
	uint8_t idrcv = uart2RxBuf[0];
	uint8_t cmdrcv = uart2RxBuf[1];
	uint8_t LR = 0;
	if(idrcv == roboWrist[0].motorid)LR = 0;
	else if(idrcv == roboWrist[1].motorid)LR = 1;
	else goto ENDLINE;
	//xor
	xorRcv = uart2RxBuf[uart2RxLen-2];
	xorCalVal = xorCal(uart2RxBuf,uart2RxLen-2);
	if(xorRcv != xorCalVal)goto ENDLINE;
	
	switch(cmdrcv)
	{
		case 0xF3://电机使能
			zdtMotor[LR].cmdstatus = uart2RxBuf[2];
			break;
			
		case 0xFD://梯形曲线位置
			zdtMotor[LR].cmdstatus = uart2RxBuf[2];
			break;	


		case 0x31://编码器数值
			if(uart2RxLen == 5)zdtMotor[LR].cmdstatus = 0xE2;
			else
			{
				zdtMotor[LR].cmdstatus = 0x02;
				BYTE1(zdtMotor[LR].EncoderVal) = uart2RxBuf[2];
				BYTE0(zdtMotor[LR].EncoderVal) = uart2RxBuf[3];
			}
			break;	
		
		case 0x35://电机转速
			if(uart2RxLen == 5)zdtMotor[LR].cmdstatus = 0xE2;
			else
			{
				zdtMotor[LR].spderr_rcvd_flag = 1;
				zdtMotor[LR].cmdstatus = 0x02;
				BYTE1(zdtMotor[LR].speed) = uart2RxBuf[3];
				BYTE0(zdtMotor[LR].speed) = uart2RxBuf[4];
				zdtMotor[LR].speedAbs = zdtMotor[LR].speed;
				if(uart2RxBuf[2] == 0)
				{
					if(zdtMotor[LR].speed > 0)zdtMotor[LR].speed = -zdtMotor[LR].speed ;
				}
			}
			break;		

		case 0x36://电机位置
			if(uart2RxLen == 5)zdtMotor[LR].cmdstatus = 0xE2;
			else
			{
				zdtMotor[LR].perr_rcvd_flag = 1;
				zdtMotor[LR].cmdstatus = 0x02;
				BYTE3(zdtMotor[LR].pos) = uart2RxBuf[3];
				BYTE2(zdtMotor[LR].pos) = uart2RxBuf[4];
				BYTE1(zdtMotor[LR].pos) = uart2RxBuf[5];
				BYTE0(zdtMotor[LR].pos) = uart2RxBuf[6];		
				if(uart2RxBuf[2] == 0)
				{
					if(zdtMotor[LR].pos > 0)zdtMotor[LR].pos = -zdtMotor[LR].pos ;
				}
			}		
			break;		
		case 0x37://电机位置误差
			if(uart2RxLen == 5)zdtMotor[LR].cmdstatus = 0xE2;
			else
			{
				zdtMotor[LR].perr_rcvd_flag = 1;
				zdtMotor[LR].cmdstatus = 0x02;
				BYTE3(zdtMotor[LR].posError) = uart2RxBuf[3];
				BYTE2(zdtMotor[LR].posError) = uart2RxBuf[4];
				BYTE1(zdtMotor[LR].posError) = uart2RxBuf[5];
				BYTE0(zdtMotor[LR].posError) = uart2RxBuf[6];	
				zdtMotor[LR].posErrorAbs = zdtMotor[LR].posError;
				if(uart2RxBuf[2] == 0)
				{
					if(zdtMotor[LR].pos > 0)zdtMotor[LR].pos = -zdtMotor[LR].pos ;
				}
			}		
			break;				
	}
	
	ENDLINE:
	__nop();
#endif
}








