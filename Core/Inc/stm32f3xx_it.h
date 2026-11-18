/* USER CODE BEGIN Header */
/* [0.0.2 수동 재구성] 대응하는 stm32f3xx_it.c의 IRQ 선언입니다. */
/* USER CODE END Header */
#ifndef __STM32F3xx_IT_H
#define __STM32F3xx_IT_H
#ifdef __cplusplus
extern "C" {
#endif
/* USER CODE BEGIN Includes */
/* USER CODE END Includes */
void NMI_Handler(void);
void HardFault_Handler(void);
void MemManage_Handler(void);
void BusFault_Handler(void);
void UsageFault_Handler(void);
void SVC_Handler(void);
void DebugMon_Handler(void);
void PendSV_Handler(void);
void SysTick_Handler(void);
void DMA1_Channel1_IRQHandler(void);
void ADC1_2_IRQHandler(void);
void USB_LP_CAN_RX0_IRQHandler(void);
void TIM1_BRK_TIM15_IRQHandler(void);
void TIM1_UP_TIM16_IRQHandler(void);
void TIM1_TRG_COM_TIM17_IRQHandler(void);
void TIM1_CC_IRQHandler(void);
void EXTI15_10_IRQHandler(void);
/* USER CODE BEGIN EFP */
/* USER CODE END EFP */
#ifdef __cplusplus
}
#endif
#endif /* __STM32F3xx_IT_H */
