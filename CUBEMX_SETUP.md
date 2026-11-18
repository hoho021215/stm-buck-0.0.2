# CubeMX 설정과 재생성 절차 — 0.0.2

프로그램 설치·F3 pack·workspace·프로젝트 가져오기는 [초기 설정 가이드](GETTING_STARTED_KO.md)를 먼저 읽습니다. 이 문서는 주변장치별 상세 설정표입니다.

[`buck_f303ze.ioc`](buck_f303ze.ioc)는 첨부 C 파일과 0.0.1의 설정 검사 조건을 근거로 재구성한 **개발 목표 프로필**입니다. 실제 CubeMX로 열기·Generate Code·재생성 보존을 시험한 파일로 표현하지 않습니다. 설치된 CubeMX가 경고·자동 보정한 항목을 확인하고 아래 표와 생성된 C 코드를 다시 비교합니다.

첨부 원본의 실험 설정과 차이는 [IOC_REVIEW.md](IOC_REVIEW.md), 사용자 구역은 [CUBEMX_USER_CODE.md](CUBEMX_USER_CODE.md)에 있습니다.

## CubeIDE 프로젝트 생성

1. 새 빈 작업 폴더에 `buck_f303ze.ioc`만 복사하고 STM32CubeMX에서 엽니다. 생성 프로젝트에 시험·참고 C 파일이 섞이지 않도록 저장소 전체를 생성 폴더에 복사하지 않는 방법을 권장합니다.
2. MCU가 STM32F303ZETx, 패키지가 LQFP144이고 NUCLEO-F303ZE에 맞는 클럭 입력인지 확인합니다.
3. Project Manager에서 프로젝트명 `buck_f303ze`, Toolchain/IDE **STM32CubeIDE**, **Keep User Code when re-generating**을 확인합니다. 주변장치 초기화는 현재 참고 C처럼 `main.c`에 모으는 설정을 사용합니다.
4. 설치된 CubeMX·F3 firmware pack 버전으로 마이그레이션되면 변경 내용을 저장 전 비교합니다. `.ioc`의 버전 표시는 실제 생성 성공 증거가 아닙니다.
5. Generate Code 후 startup·linker·HAL/CMSIS·`.project`·`.cproject`가 만들어진 프로젝트를 CubeIDE로 엽니다. 저장소의 `buck_*.c/.h`만 추가하고, 참고 C와 실제 생성 코드를 비교해 USER CODE 내용을 연결합니다. 생성된 main/MSP/IRQ/헤더 전체를 참고본으로 덮어쓰지 않습니다.
6. `BUCK_BOARD_VERIFIED=0`을 유지합니다. 저장소 전체를 프로젝트 폴더로 사용했다면 `reference/`와 `tests/`에 반드시 Exclude from Build를 적용합니다.

첨부 `.project`는 `ex1`의 IDE 식별 정보이며 `.mxproject`는 이전 생성 파일 목록입니다. 둘만으로 빌드 옵션이나 주변장치 설정 전체를 복구할 수 없으므로 새 프로젝트의 생성 metadata로 사용하지 않습니다.

## 클럭

| 항목 | 목표 |
|---|---|
| HSE | bypass, 명목 8MHz ST-LINK MCO |
| PLL | HSE /1 ×9 |
| SYSCLK / HCLK | 72MHz |
| APB1 / APB2 | 36MHz / 72MHz |
| TIM1 | HCLK 72MHz. PLL VCO×2 경로 사용하지 않음 |
| ADC12 PLL clock | PLL 72MHz /1 |
| ADC1 prescaler | asynchronous DIV1 |
| USB | PLL /1.5 = 48MHz |
| RTC / USART3 | LSI / PCLK1, UART 38400baud |

ADC를 `ADC_CLOCK_SYNC_PCLK_DIV4`로 유지하면 18MHz가 되어 현재 preflight와 일치하지 않습니다. RCC의 계산 주파수 표시와 실제 ADC clock mode를 함께 확인합니다.

## 핀과 외부 배선

| 핀 | 프로필 기능 | 사용자 확인 |
|---|---|---|
| PC0 AF2 | TIM1_CH1 | UCC27714 HI 연결 |
| PA7 AF6 | TIM1_CH1N | UCC27714 LI 연결 |
| PA0 | ADC1_IN1 / Rank1 | 인덕터 전류 I_sen |
| PA1 | ADC1_IN2 / Rank2 | 출력 전압 V_sen |
| PA2 | ADC1_IN3 / Rank3 | 입력 전압 Vin_sen |
| PC6 | 전용 EN, output push-pull, 초기 LOW, no-pull | PCB 실제 net과 분리 여부 확인 |
| PC13 | 상승 에지 EXTI 정지 버튼 | NUCLEO 보드 버튼 연결 확인 |
| PA4 | DAC1 OUT1 | 주변장치만 유지. 앱은 실험파형을 출력하지 않음 |

ADC 핀과 PC6는 no-pull이며 EN의 리셋 중 OFF는 외부 풀다운으로 보장합니다. ADC 핀은 analog입니다. EN에는 외부 약 10kΩ 풀다운을 둬 리셋·초기화 전에도 OFF를 유지합니다. FAULT와 EN을 공유한 PCB net에 PC6 push-pull을 바로 연결하지 않습니다. PC6는 배선 확인 전 가정입니다.

## TIM1

| 항목 | 목표 |
|---|---|
| Counter / PSC / ARR | Up / 0 / 1439 |
| CKD / RCR | DIV1 / 0 |
| Auto-reload preload | Enable |
| UDIS / OPM | 0 / 0: update event 허용, 반복 운전 |
| CH1 | PWM1, Pulse=0, CH1·CH1N 사용 |
| CH1·CH1N polarity / idle | HIGH / RESET |
| CH1·CH4 compare preload | Enable |
| CH4 | 내부 PWM2, Pulse=360 |
| TRGO / TRGO2 | OC4REF / RESET |
| Master-slave | Disable |
| DTG | 22, 약 305.6ns |
| OSSI / OSSR | Enable / Enable |
| AOE | Disable |
| Break / Break2 | Disable, 실제 비교기 연결 미정 |

`72MHz / (1439+1) = 50kHz`, 주기는 20µs입니다. CH4의 OC4REF 상승이 카운터 360, 약 5µs에서 한 번 발생합니다. CH4는 내부 ADC 트리거이며 별도 게이트나 보드 핀에 연결하지 않습니다.

DTG=22는 MOSFET·게이트 저항·driver 지연 검증 전의 후보입니다. CubeMX의 단위/DTG 인코딩과 실제 파형을 확인합니다. 값 변경 시 `buck_board.h`의 검사값도 함께 맞춥니다. PWM 시작은 앱이 관리하므로 생성된 main 사용자 구역에 HAL PWM 자동 시작을 추가하지 않습니다.

고정 5µs는 듀티 25% 부근에서 스위칭 에지와 겹칠 수 있습니다. 센서·RC 지연과 노이즈를 측정해 샘플 시점·최소 펄스 조건을 재검토합니다. 한 표본을 정확한 평균·피크 전류로 간주하지 않습니다.

## ADC1 / DMA / IRQ

| 항목 | 목표 |
|---|---|
| Resolution / alignment | 12bit / Right |
| Scan / NbrOfConversion | Enable / 3 |
| Rank1 / Rank2 / Rank3 | IN1 PA0 IL / IN2 PA1 Vout / IN3 PA2 Vin |
| Sampling | 전 채널 19.5cycles, single-ended |
| EOC selection | End of sequence |
| Continuous / discontinuous / AutoWait | Disable |
| External trigger / edge | TIM1_TRGO / Rising |
| DMA continuous requests | Enable |
| Overrun | Data preserved |
| DMA channel | DMA1 Channel1, peripheral→memory |
| DMA mode / increment | Circular / peripheral fixed, memory increment |
| Peripheral / memory alignment | Halfword / Halfword |
| DMA priority | High |
| DMA1 Channel1 / ADC1_2 IRQ | Enable, preemption priority 0 |
| SysTick / EXTI15_10 | HAL tick 유지 / 버튼 정지 |

`MX_DMA_Init()`의 DMA clock·NVIC 설정은 `MX_ADC1_Init()`보다 먼저 실행합니다. ADC MSP의 `HAL_DMA_Init()`와 `__HAL_LINKDMA(hadc,DMA_Handle,hdma_adc1)`가 필요합니다. `hdma_adc1.Parent`가 `&hadc1`로 연결되어야 합니다.

앱의 6 halfword 버퍼는 `[IL,Vout,Vin]` 두 프레임이며 half/full DMA callback이 각각 한 PWM 주기 표본을 처리합니다. 버퍼를 CCM RAM에 두지 않습니다. 생성 IRQ에서 `HAL_DMA_IRQHandler(&hdma_adc1)`, `HAL_ADC_IRQHandler(&hadc1)`, `HAL_IncTick()` 호출을 유지합니다.

## 생성 후 확인과 실물 검증

`Core/Inc` include path, STM32F303xE·USE_HAL_DRIVER 정의, Cortex-M4F 및 맞는 FPU/ABI를 확인합니다. `-O2`를 사용하고 `-ffast-math`를 사용하지 않습니다. ISR에 printf·UART blocking·HAL_Delay를 넣지 않습니다.

재생성 후 레지스터·핸들 조건을 `buck_hw.c` preflight가 다시 검사합니다. F_SETUP이면 검사 우회보다 생성된 clock·rank·GPIO·TIM·DMA 설정을 먼저 비교합니다. 이 검사는 CubeMX의 인식 여부나 실물 안정성을 증명하지 않습니다.

기본 기동 차단 상태에서 영점 보정·DMM 대비 환산·DMA 간격·ISR 시간을 확인합니다. 이어 별도 시험 절차로 gate overlap·deadtime·bootstrap·정지 경로를 검증하고, L·C/ESR·MOSFET 정격과 제어 이득·보호 임계값을 확정한 뒤에만 검증 플래그를 변경합니다. 실제 실행한 검사 범위는 [VALIDATION.md](VALIDATION.md)에 기록합니다.
