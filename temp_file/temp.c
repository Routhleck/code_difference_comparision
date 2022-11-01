#include "reg51.h"
#include "intrins.h"
#define FOSC        11059200UL
#define BRT         (65536 - FOSC / 115200 / 4)
sfr     AUXR    =   0x8e;
sfr     P0M1    =   0x93;
sfr     P0M0    =   0x94;
sfr     P1M1    =   0x91;
sfr     P1M0    =   0x92;
sfr     P2M1    =   0x95;
sfr     P2M0    =   0x96;
sfr     P3M1    =   0xb1;
sfr     P3M0    =   0xb2;
sfr     P4M1    =   0xb3;
sfr     P4M0    =   0xb4;
sfr     P5M1    =   0xc9;
sfr     P5M0    =   0xca;
bit busy;
char xdata *ID;
void delay(unsigned int l)
{
    int i;
    int j;
    for(i = 0; i < l; i++)
    {
        for(j = 0; j < 1000; j++)
        {
            _nop_();
        }
    }
}
void UartIsr() interrupt 4
{
    if (TI)
    {
        TI = 0;
        busy = 0;
    }
    if (RI)
    {
        RI = 0;
    }
}
void UartInit()
{
    SCON = 0x50;
    TMOD = 0x00;
    TL1 = BRT;
    TH1 = BRT >> 8;
    TR1 = 1;
    AUXR = 0x40;
    busy = 0;
}
void UartSend(char dat)
{
    while (busy);
    busy = 1;
    SBUF = dat;
}
void main()
{
		int i;
    delay(2000);
    P0M0 = 0x00;
    P0M1 = 0x00;
    P1M0 = 0x00;
    P1M1 = 0x00;
    P2M0 = 0x00;
    P2M1 = 0x00;
    P3M0 = 0x00;
    P3M1 = 0x00;
    P4M0 = 0x00;
    P4M1 = 0x00;
    P5M0 = 0x00;
    P5M1 = 0x00;
    ID = 0x0000;
    UartInit();
    ES = 1;
    EA = 1;
    while(i<8192)
    {
      UartSend(ID[i]);
			i++;
    }
		while(1);
}
