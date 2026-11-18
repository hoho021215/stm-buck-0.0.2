# 첨부 설정 검토와 새 .ioc의 차이 — 0.0.2

사용자가 제공한 `main.c`, `stm32f3xx_hal_msp.c`, `stm32f3xx_it.c`, `system_stm32f3xx.c`, `.project`, `.mxproject`를 확인했습니다. 최초 C 파일 첨부에는 `.ioc`가 없었습니다. 이후 추가 첨부한 `ex1.ioc`를 확인했으며, 기존 `reference/v0.0.1/ex1.ioc`와 바이트 단위로 동일합니다. 새 ADC/TIM 설정이 추가된 파일은 아닙니다. 새 [`buck_f303ze.ioc`](buck_f303ze.ioc)는 이 자료와 기존 제어 모듈의 조건을 조합한 수작업 개발 프로필입니다.

## 실제 첨부에서 확인한 내용

후속 `ex1.ioc`는 CubeMX 속성 파일 형식으로, 중복 없는 속성 261개, IP 9개·핀 23개 목록 및 ADC/TIM/RCC 속성 참조 정적 검사를 통과했습니다. MCU는 STM32F303ZET6, 보드는 NUCLEO-F303ZE입니다. 파일을 실제 CubeMX에서 열거나 재생성한 검사는 아닙니다. 원본은 [`reference/uploaded/ex1.ioc`](reference/uploaded/ex1.ioc)에 보존하며, 코드에 맞춘 `buck_f303ze.ioc`는 그대로 유지합니다.

| 항목 | 첨부의 실제 내용 | 벅에서 수정할 이유 |
|---|---|---|
| MCU/IDE | STM32F303xE, 프로젝트 ex1, CubeIDE 성격 | MCU 계열은 맞지만 .cproject·startup·linker·헤더·vendor 전체 없음 |
| Clock | HSE bypass / PLL×9, HCLK 72MHz, TIM1 HCLK | 유지. system의 초기 8MHz 변수는 reset 기준으로 정상 |
| TIM1 | PSC0, center-aligned1, ARR3599 | 약 10kHz이며 목표 50kHz와 다름 |
| TRGO | UPDATE, RCR0 | center 정렬에서 주기당 두 update event가 생길 수 있음. PWM과 ADC trigger 주파수를 구분해야 함 |
| CH1/CH1N | PC0 AF2 / PA7 AF6 | 기존 연결 유지 |
| Deadtime | 0, OSSI/OSSR disable | 동기식 전력단의 게이트 중첩·정지 상태 검토 필요 |
| ADC1 | PA0 한 채널, sync PCLK/4, 1.5cycle | 18MHz·단일 채널이며 현재 3채널 제어 모듈과 다름 |
| ADC trigger | 초기화는 TIM1_TRGO지만 USER CODE2가 LAB_COPY에서 software로 덮어씀 | 생성 설정만 보고 실제 ADC 동작을 판단할 수 없음 |
| DMA | ADC DMA 없음 | 3채널 프레임 수집과 갱신 감시에 필요 |
| USER CODE | PA0→PA4 DAC 복사, 듀티50% CH1/CH1N 자동 시작 | 벅의 보정·bootstrap·조건부 기동 경로로 교체 |
| 전용 EN | 없음 | PC6 LOW 출력 개발 프로필 추가. 실제 PCB 연결 확인 필요 |
| 버튼 | PC13 EXTI 정지 | 벅 앱 정지 경로와 연결 |
| UART/DAC | USART3 38400 / PA4 DAC | 주변장치 유지, LAB 실험 출력 제거 |

`.project`는 IDE 프로젝트 식별자이고 `.mxproject`의 Previous* 항목은 이전 생성 파일 목록입니다. ADC rank·핀·클럭의 신뢰할 원천으로 쓰거나 새 프로젝트의 빌드 설정을 대신할 수 없습니다.

## 새 개발 프로필에 반영한 목표

- TIM1 Up, ARR1439, PSC0, 72MHz의 50kHz. PWM1 CH1/CH1N은 pulse0으로 초기화.
- CH4는 내부 PWM2·CCR360, TRGO=OC4REF로 약 5µs에 ADC trigger.
- DTG22, OSSI/OSSR enable, AOE disable. 실제 deadtime은 파형 검증 전 후보.
- ADC1 asynchronous 72MHz /1, PA0/PA1/PA2 rank1/2/3, 19.5cycle, 외부 rising trigger, circular DMA1 Channel1 halfword.
- PC6를 전용 EN 초기 LOW로 채택하고 앱의 기본 검증 플래그 0 유지.
- RTC·USB·UART·DAC 주변장치와 기존 CubeMX USER CODE 형식 유지.

계산상 목표가 일치해도 CubeMX가 인식·생성했다는 증거가 되지 않습니다. 특히 설치된 버전에서 내부 CH4·DMA·ADC RCC 설정이 유지되는지 생성 결과와 실제 레지스터를 확인해야 합니다. 자세한 표는 [CUBEMX_SETUP.md](CUBEMX_SETUP.md)에 있습니다.

## 미확정 조건

L1 인덕턴스·포화전류, 출력 총 C·ESR, MOSFET 품번, 전용 EN 배선과 FAULT 분리, 실제 gate delay, ADC 입력 연결·VDDA·전류 방향이 미확정입니다. 전류·전압 이중 루프의 최종 이득이나 실제 안정성을 임의로 정하지 않습니다.

참고 원본은 [reference/uploaded/](reference/uploaded/), 변경 전 `.ioc`는 [reference/v0.0.1/ex1.ioc](reference/v0.0.1/ex1.ioc)에 보존합니다. 출처와 해시는 [ORIGIN.md](ORIGIN.md), 실제 실행한 검사는 [VALIDATION.md](VALIDATION.md)에 기록합니다.
