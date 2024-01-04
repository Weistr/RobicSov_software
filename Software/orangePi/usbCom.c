#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termios.h>
#include <errno.h>
#include <string.h>
#include <sys/select.h>

#include "usbCom.h"


/**
 * 初始化串口
*/
int ttyUSBfd;
int usbComInit()
{
    
    struct termios options;
    //开启串口
    ttyUSBfd = open("/dev/ttyACM0",O_RDWR|O_NOCTTY|O_NDELAY);

    if(ttyUSBfd < 0)
    {
        printf("open ttyUSB failed:%s\n",strerror(errno));
        goto ttyFaild;
    }

    printf("open ttyUSB successful!\n");

    //获取串口信息
    memset(&options, 0, sizeof(options)) ;

    int16_t rv = tcgetattr(ttyUSBfd, &options); //获取原有的串口属性的配置    

    if(rv != 0)
    {
        printf("tcgetattr() failed:%s\n",strerror(errno)) ;
        goto ttyFaild ;
 
    }

    options.c_cflag|=(CLOCAL|CREAD ); // CREAD 开启串行数据接收，CLOCAL并打开本地连接模式
 
    options.c_cflag &=~CSIZE;// 先使用CSIZE做位屏蔽  
 
    options.c_cflag |= CS8; //设置8位数据位
 
    options.c_cflag &= ~PARENB; //无校验位
    /* 设置115200波特率  */
 
    cfsetispeed(&options, B115200);
 
    cfsetospeed(&options, B115200);
 
 
 
    options.c_cflag &= ~CSTOPB;/* 设置一位停止位; */
 
    options.c_cc[VTIME] = 0;/* 非规范模式读取时的超时时间；*/
 
    options.c_cc[VMIN]  = 0; /* 非规范模式读取时的最小字符数*/
 
    tcflush(ttyUSBfd ,TCIFLUSH);/* tcflush清空终端未完成的输入/输出请求及数据；TCIFLUSH表示清空正收到的数据，且不读取出来 */

 
    if((tcsetattr(ttyUSBfd, TCSANOW,&options))!=0)
 
    {
 
        printf("tcsetattr failed:%s\n", strerror(errno));
 
        goto ttyFaild ;
 
    }
    return ttyUSBfd;


    ttyFaild: close(ttyUSBfd);
    return 0;
}

void usbComSend(u_int8_t* buf, int len)
{

    int rv = write(ttyUSBfd,buf,len);
    if(rv < 0)
    {
        printf("write() error:%s\n",strerror(errno));
    }
}
fd_set rset;
void usbComRead(u_int8_t* buf, int len)
{
    int rv;
    FD_ZERO(&rset);
    FD_SET(ttyUSBfd, &rset);
    rv = select(ttyUSBfd+1, &rset, NULL, NULL, NULL) ;     
    if(rv < 0) 
    {
        printf("select() failed: %s\n", strerror(errno)); 
    }
    else if(rv == 0)
    {
        printf("select() time out!\n") ; 
    }
    else 
    {
        printf("selss\n");
    }
    rv = select(ttyUSBfd+1, &rset, NULL, NULL, NULL) ;
    memset(buf, 0, len) ;
    rv = read(ttyUSBfd,buf,len);
    if(rv < 0)
    {
        printf("read() error:%s\n",strerror(errno)) ;
    }
    
}
