/* USER CODE BEGIN Header */
/* [0.0.2 수동 재구성 헤더] 첨부 main.c/MSP와 buck_f303ze.ioc 기준입니다.
 * CubeMX 재생성 시 생성된 main.h의 핀/선언을 우선 비교하세요. */
/* USER CODE END Header */
#ifndef __MAIN_H
#define __MAIN_H
#ifdef __cplusplus
extern "C" {
#endif
#include "stm32f3xx_hal.h"
/* USER CODE BEGIN Includes */
/* USER CODE END Includes */
void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);
void Error_Handler(void);
#define LD1_Pin GPIO_PIN_0
#define LD1_GPIO_Port GPIOB
#define LD3_Pin GPIO_PIN_14
#define LD3_GPIO_Port GPIOB
#define LD2_Pin GPIO_PIN_7
#define LD2_GPIO_Port GPIOB
#define STLK_RX_Pin GPIO_PIN_8
#define STLK_RX_GPIO_Port GPIOD
#define STLK_TX_Pin GPIO_PIN_9
#define STLK_TX_GPIO_Port GPIOD
#define USB_PowerSwitchOn_Pin GPIO_PIN_6
#define USB_PowerSwitchOn_GPIO_Port GPIOG
#define USB_OverCurrent_Pin GPIO_PIN_7
#define USB_OverCurrent_GPIO_Port GPIOG
#define BUCK_EN_Pin GPIO_PIN_6
#define BUCK_EN_GPIO_Port GPIOC
/* USER CODE BEGIN Private defines */
/* [배선 확인 필요] PC6은 전용 드라이버 EN이며 외부 풀다운이 필요합니다.
 * ACS71240 FAULT와 공유된 선에 push-pull HIGH를 연결하지 마세요. */
/* USER CODE END Private defines */
#ifdef __cplusplus
}
#endif
#endif /* __MAIN_H */
