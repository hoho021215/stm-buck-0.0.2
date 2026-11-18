# CubeMX / CubeIDE USER CODE 연결 — 0.0.2

이 저장소는 첨부와 같은 `/* USER CODE BEGIN ... */` 형식을 사용합니다. `main.c`, MSP, IRQ와 헤더는 첨부를 근거로 **수작업 수정한 통합 참고본**이며, 새 `.ioc`로 실제 생성한 파일이라는 뜻은 아닙니다. [설정표](CUBEMX_SETUP.md)를 확인하고 CubeMX로 프로젝트를 생성한 뒤 아래 사용자 구역을 연결합니다.

권장 적용 방법은 빈 폴더에 `.ioc`만 복사해 생성한 뒤 아래 `buck_*` 모듈과 USER CODE 내용만 추가하는 것입니다. 생성된 main/MSP/IRQ/헤더 전체를 참고본으로 덮어쓰지 않습니다.

`reference/uploaded/`는 원본 자료 보관이며 제품 빌드 소스가 아닙니다. `integration/*.example`도 위치 설명용 부분 파일이므로 빌드에 추가하지 않습니다.

## 생성 파일과 직접 관리 파일

| 파일 | 관리 방법 |
|---|---|
| `main.c`, `main.h`, MSP, IRQ, HAL config, system | CubeMX 생성 결과를 기준으로 관리. 주변장치·핀·IRQ 변경은 MX에서 반영 |
| `buck_app.c/.h` | 사용자가 별도로 추가하는 제어·상태 전이 |
| `buck_board.h` | 사용자가 확인하는 클럭·핀·센싱·검증 플래그 |
| `buck_hw.c/.h` | 실제 레지스터·핸들 설정 검사 |
| `buck_supervisor.c/.h` | 출력 UV·PGOOD 감시 |
| `buck_platform.h` | IRQ 저장/복구 내부 헤더. 제품에 BUCK_HOST_TEST를 정의하지 않음 |

`Core/Src`의 세 `buck_*.c`와 `Core/Inc`의 모든 `buck_*.h`를 프로젝트에 추가합니다. `.c` 자체를 include하거나 `hadc1`, `htim1`, `hdma_adc1`을 다른 파일에서 중복 정의하지 않습니다.

Project Manager → Code Generator의 **Keep User Code when re-generating**을 켭니다. 기존 USER CODE 표식 이름과 위치를 그대로 유지합니다. 재생성 뒤 diff와 Clean/Build로 사용자 구역 보존을 확인해야 하며, 이번 작업이 그 실물 재생성을 시험한 것으로 해석하지 않습니다.

## main.c

생성된 `Includes` 구역:

```c
/* USER CODE BEGIN Includes */
#include "buck_app.h" /* [직접 추가] 벅 앱의 공개 인터페이스 */
/* USER CODE END Includes */
```

생성된 초기화 호출은 한 번씩 유지하며 `MX_DMA_Init()`가 `MX_ADC1_Init()`보다 앞인지 확인합니다. 첨부에 있던 LAB_COPY/LAB_SPWM 실험 코드, ADC trigger 덮어쓰기, ADC polling, DAC 복사, 듀티 50% 자동 시작을 함께 남기지 않습니다.

```c
/* USER CODE BEGIN 2 */
/* [직접 추가] 생성된 GPIO/DMA/ADC1/TIM1 초기화가 모두 끝난 뒤 한 번 실행.
 * BUCK_BOARD_VERIFIED=0에서는 전력단 시작이 허용되지 않습니다. */
Buck_Init();
/* USER CODE END 2 */
```

```c
/* USER CODE BEGIN WHILE */
while (1)
{
  /* USER CODE END WHILE */

  /* USER CODE BEGIN 3 */
  /* [직접 추가] ADC 갱신 정지 감시. 이 반복문을 긴 blocking 함수로 막지 않습니다. */
  Buck_Poll();
}
/* USER CODE END 3 */
```

CubeMX 버전에 따라 닫는 중괄호 위치가 달라질 수 있으므로 구역 전체나 중괄호를 중복 복사하지 않습니다.

`HAL_TIM_PWM_Start()`, `HAL_TIMEx_PWMN_Start()`, `HAL_ADC_Start_IT()`를 사용자 기동 코드로 추가하지 않습니다. `Buck_Init()`와 앱의 DMA callback이 타이머·게이트 순서를 관리합니다. `HAL_ADC_ConvHalfCpltCallback`, `HAL_ADC_ConvCpltCallback`, `HAL_ADC_ErrorCallback`의 정의는 `buck_app.c` 한 곳에만 둡니다.

## 버튼 정지

`main.c`의 기존 `USER CODE 4`에 둔 `HAL_GPIO_EXTI_Callback()`는 PC13 이벤트에서 게이트를 차단하고 앱에 정지 명령을 전달합니다. ADC callback과 상태 전이가 진행 중에도 정지 요청이 유실되거나 다시 기동하지 않도록 통합 코드의 처리를 유지합니다.

PC13은 정지 입력이며 시작·고장 해제 버튼으로 쓰지 않습니다. HAL EXTI IRQ handler 호출도 유지합니다. 실제 버튼·EN·게이트 배선을 확인하기 전 실물 보호 장치로 간주하지 않습니다.

## Error_Handler와 fault

`main.c`의 기존 구역에서 인터럽트를 먼저 끈 뒤 차단하고 무한 루프에 머뭅니다.

```c
/* USER CODE BEGIN Error_Handler_Debug */
__disable_irq();
Buck_EmergencyOff(); /* [직접 추가] 주변장치 초기화 실패를 포함해 게이트 차단 */
while (1)
{
}
/* USER CODE END Error_Handler_Debug */
```

IRQ 파일의 기존 `Includes` 구역에도 `#include "buck_app.h"`를 넣습니다. HardFault와 사용 중인 MemManage/BusFault/UsageFault 핸들러의 첫 사용자 구역에서 인터럽트를 끄고 `Buck_EmergencyOff()`를 호출한 뒤 기존 무한 루프를 유지합니다. 원본에 없는 USER CODE 이름을 임의로 만들어 보존을 기대하지 않습니다.

NMI로 clock security failure를 처리하는 경우에도 차단 후 계속 운전하지 않도록 합니다. 비상 차단 함수는 리셋 중 외부 EN 풀다운과 독립 하드웨어 보호를 대신하지 않습니다.

## 생성 코드에서 확인할 연결

- `MX_DMA_Init()`에서 DMA1 clock와 Channel1 IRQ 설정.
- ADC MSP에서 PA0/PA1/PA2 analog, DMA1 Channel1 circular·halfword 및 `__HAL_LINKDMA`.
- TIM MSP/PostInit에서 PC0 AF2 CH1, PA7 AF6 CH1N.
- GPIO에서 PC6 LOW를 먼저 기록하고 출력으로 설정. 외부 풀다운도 필요.
- DMA IRQ의 `HAL_DMA_IRQHandler(&hdma_adc1)`, ADC IRQ의 `HAL_ADC_IRQHandler(&hadc1)`.
- SysTick의 `HAL_IncTick()`, PC13 EXTI의 `HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_13)`.
- system source는 한 개만 빌드. Core와 Drivers 경로의 같은 파일을 동시에 추가하지 않음.

설정이 달라지면 `buck_board.h`와 preflight 조건도 근거 있게 함께 갱신합니다. F_SETUP을 숨기거나 `BUCK_BOARD_VERIFIED`를 먼저 1로 바꾸는 방법으로 설정 차이를 해결하지 않습니다. 실제 검증·실행 방법은 [VALIDATION.md](VALIDATION.md)를 확인합니다.
