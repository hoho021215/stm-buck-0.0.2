/* USER CODE BEGIN Header */
/* [0.0.2 수동 재구성 HAL 설정] CubeMX 재생성 시 해당 버전의 생성 설정으로 비교합니다.
 * tests/hal_config의 호스트 전용 헤더를 펌웨어에 복사하지 마세요. */
/* USER CODE END Header */
#ifndef STM32F3xx_HAL_CONF_H
#define STM32F3xx_HAL_CONF_H
#ifdef __cplusplus
extern "C" {
#endif
#define HAL_MODULE_ENABLED
#define HAL_ADC_MODULE_ENABLED
#define HAL_DMA_MODULE_ENABLED
#define HAL_RCC_MODULE_ENABLED
#define HAL_FLASH_MODULE_ENABLED
#define HAL_GPIO_MODULE_ENABLED
#define HAL_CORTEX_MODULE_ENABLED
#define HAL_PWR_MODULE_ENABLED
#define HAL_TIM_MODULE_ENABLED
#define HAL_DAC_MODULE_ENABLED
#define HAL_RTC_MODULE_ENABLED
#define HAL_UART_MODULE_ENABLED
#define HAL_PCD_MODULE_ENABLED
#define HSE_VALUE 8000000U
#define HSE_STARTUP_TIMEOUT 100U
#define HSI_VALUE 8000000U
#define LSI_VALUE 40000U
#define LSE_VALUE 32768U
#define LSE_STARTUP_TIMEOUT 5000U
#define EXTERNAL_CLOCK_VALUE 8000000U
#define VDD_VALUE 3300U
#define TICK_INT_PRIORITY 3U
#define USE_RTOS 0U
#define PREFETCH_ENABLE 1U
#define INSTRUCTION_CACHE_ENABLE 0U
#define DATA_CACHE_ENABLE 0U
#define USE_SPI_CRC 1U
#define USE_HAL_ADC_REGISTER_CALLBACKS 0U
#define USE_HAL_DAC_REGISTER_CALLBACKS 0U
#define USE_HAL_RTC_REGISTER_CALLBACKS 0U
#define USE_HAL_TIM_REGISTER_CALLBACKS 0U
#define USE_HAL_UART_REGISTER_CALLBACKS 0U
#define USE_HAL_PCD_REGISTER_CALLBACKS 0U
#include "stm32f3xx_hal_dma.h"
#include "stm32f3xx_hal_rcc.h"
#include "stm32f3xx_hal_flash.h"
#include "stm32f3xx_hal_gpio.h"
#include "stm32f3xx_hal_cortex.h"
#include "stm32f3xx_hal_adc.h"
#include "stm32f3xx_hal_pwr.h"
#include "stm32f3xx_hal_tim.h"
#include "stm32f3xx_hal_dac.h"
#include "stm32f3xx_hal_rtc.h"
#include "stm32f3xx_hal_uart.h"
#include "stm32f3xx_hal_pcd.h"
/* USER CODE BEGIN Includes */
/* USER CODE END Includes */
#ifdef USE_FULL_ASSERT
void assert_failed(uint8_t *file, uint32_t line);
#define assert_param(expr) ((expr) ? (void)0U : assert_failed((uint8_t *)__FILE__, __LINE__))
#else
#define assert_param(expr) ((void)0U)
#endif
#ifdef __cplusplus
}
#endif
#endif /* STM32F3xx_HAL_CONF_H */
