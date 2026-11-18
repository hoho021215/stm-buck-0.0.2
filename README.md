# STM32F303ZE 동기식 벅 컨버터 0.0.2

[GitHub 저장소 바로가기](https://github.com/hoho021215/stm-buck-0.0.2)

**처음 설정한다면: [설치부터 CubeMX 생성·CubeIDE 첫 빌드까지](GETTING_STARTED_KO.md)**

NUCLEO-F303ZE / STM32F303ZET6, 입력 30V → 출력 15V·1A·15W, 목표 스위칭 50kHz의 개발용 코드와 CubeMX 설정입니다. 0.0.1의 제어·보호 모듈을 유지하고, 사용자가 제공한 CubeIDE C 파일의 `USER CODE` 형식에 맞춘 초기화·IRQ·통합 파일과 [`buck_f303ze.ioc`](buck_f303ze.ioc)를 추가합니다.

**이 `.ioc`와 생성 형식의 C 파일은 첨부 자료를 근거로 수작업 재구성한 개발 프로필입니다. CubeMX에서 실제 Generate Code한 결과라고 주장하지 않습니다.** CubeMX로 열어 설정을 확인하고 새 CubeIDE 프로젝트를 생성해야 합니다. `.cproject`, startup, linker script, HAL/CMSIS vendor 전체가 포함된 즉시 Import/Flash 프로젝트는 아닙니다. 실제 수행한 검사는 [VALIDATION.md](VALIDATION.md)에 구분해 기록합니다.

기본값 `BUCK_BOARD_VERIFIED=0`은 전력단 기동을 차단합니다. 설정 검사에 통과해도 실물 배선·게이트 파형·보호·센싱 검증 전에는 1로 변경하지 않습니다.

## 이번 버전의 변경

후속 첨부 [`ex1.ioc`](reference/uploaded/ex1.ioc)도 CubeMX 설정 형식으로 확인했습니다. 기존 `reference/v0.0.1/ex1.ioc`와 9535 bytes 전체가 동일하며, 약 10kHz·ADC 단일 채널의 실험 프로필입니다. 실제 생성에 사용할 개발 목표는 루트의 `buck_f303ze.ioc`이며, 첨부 원본으로 교체하지 않았습니다.

첨부 `main.c`는 기본 `LAB_COPY` 모드에서 PA0 ADC를 software trigger로 읽어 PA4 DAC로 복사하고, TIM1을 듀티 50%로 자동 시작했습니다. TIM1은 약 10kHz center-aligned, deadtime 0이며 ADC는 한 채널·DMA 미사용이었습니다. 이 실험 동작을 벅 기동에 그대로 사용하지 않습니다.

0.0.2에는 다음 개발 목표를 반영합니다.

- TIM1 72MHz, Up / PSC=0 / ARR=1439의 50kHz 상보 PWM. CH1·CH1N 초기 듀티 0, DTG=22 약 305.6ns.
- 내부 CH4 PWM2 / CCR4=360 / OC4REF TRGO를 이용한 주기 시작 약 5µs 후 ADC 트리거.
- PA0=인덕터 전류, PA1=출력 전압, PA2=입력 전압의 3채널 순서와 circular DMA.
- PC6의 전용 드라이버 EN 초기 LOW. PC0 CH1 / PA7 CH1N은 기존 핀 유지.
- `Buck_Init()` / `Buck_Poll()`, 오류·fault 차단, PC13 정지와 생성 IRQ의 HAL 처리 연결.
- ADC callback은 `buck_app.c` 한 곳에서 정의하며, 첨부의 LAB callback과 중복하지 않음.
- RTC·USB·USART3 38400baud와 PA4 DAC 주변장치 구성을 참고용으로 유지. 벅 앱은 DAC에 실험 기준파를 쓰지 않음.

DTG=22, ADC 트리거 시점과 제어 계수는 검증 전 초깃값입니다. 고정 5µs 전류 표본은 듀티·리플·센서 지연에 따라 평균 또는 피크 전류와 다를 수 있습니다.

## 파일과 적용 순서

1. [IOC_REVIEW.md](IOC_REVIEW.md)에서 첨부 설정과 수정 이유를 확인합니다.
2. [CUBEMX_SETUP.md](CUBEMX_SETUP.md)의 표와 `buck_f303ze.ioc`를 비교하고, 새 빈 폴더에 `.ioc`만 복사해 STM32CubeIDE 프로젝트를 생성합니다.
3. [CUBEMX_USER_CODE.md](CUBEMX_USER_CODE.md)에 따라 생성 파일의 기존 사용자 구역과 별도 제어 모듈을 연결합니다.
4. 기본 기동 차단 상태에서 설정 검사·센싱·타이밍을 확인한 뒤 보드별 검증을 진행합니다.

| 위치 | 용도 |
|---|---|
| `buck_f303ze.ioc` | 새 버전의 재구성 CubeMX 개발 프로필 |
| `Core/Src/main.c`, MSP, IRQ 및 관련 헤더 | 첨부 스타일을 따른 수작업 통합 참고본. 실제 재생성 결과와 비교 |
| `Core/Src/buck_*.c`, `Core/Inc/buck_*.h` | 사용자가 별도로 관리하는 제어·설정 검사·출력 감시 모듈 |
| `reference/uploaded/` | C·metadata 6개와 후속 `ex1.ioc` 원본 보관. 빌드 소스에 추가하지 않음 |
| `reference/v0.0.1/ex1.ioc` | 변경 전 설정 원본 보관 |
| `integration/*.example` | 사용자 코드 위치를 보여 주는 부분 예제. 빌드 제외 |
| `tests/` | 호스트 검사용. 펌웨어에 시험 헤더·`BUCK_HOST_TEST`를 넣지 않음 |

## 제어·감시 기능

0.0.1의 입력전압 피드포워드, 300ms 기준전압 램프, 듀티 상승 제한 1.0/s, 10kHz 전압 보상·50kHz 센싱, 전류 duty-cap과 최종 듀티 기준 anti-windup을 유지합니다. 약 500ms보다 빨리 듀티 0.5에 도달하지 않으므로 기준전압 램프 시간은 출력 정착 시간을 보장하지 않습니다.

게이트 OFF 상태에서 2048표본 영점 보정, 약 1ms 저측 bootstrap 충전, 기충전 출력 기동 거부, DWT 처리 시점·실행시간 및 ADC 갱신 감시를 사용합니다. 정상 기동 검사를 통과한 뒤 출력이 기준의 80% 미만이면 UV 상태에 진입하고 85% 초과에서 해제합니다. 활성 상태가 50ms 연속 유지되면 차단합니다. PGOOD는 ±5% 범위 5ms 유지 시 설정하고 ±10% 이탈·정지·고장 시 해제합니다.

첫 고장 당시 raw ADC, 환산 전압·전류, 듀티·적분기·상태·타이밍은 `buck_fault_snapshot`에 보관합니다. 이후 고장으로 덮어쓰지 않으며 수동 clear 또는 리셋·초기화 시 사라집니다. RAM 기록이며 `sample_valid`는 표본 존재 표시입니다.

전류 duty-cap은 CC 루프가 아닙니다. 이 버전은 평균전류 이중 루프·CC/CV·MPC·Deadbeat·DOB·IWDG를 추가하지 않습니다. 인덕터 L·포화전류, 출력 총 C·ESR, MOSFET 품번과 지연 모델이 확보되면 내부 전류 루프부터 별도로 설계·검증할 수 있습니다.

## 센싱과 사용자 확인값

| 항목 | 기준 |
|---|---|
| 전류센서 | ACS71240LLCBTR-010B3, 인덕터 전류 |
| 명목 환산 | 3.3V 전원, 영점 1.65V, 감도 0.132V/A |
| 전압 검출 | 분압비 19, MCP6002 단위 이득 버퍼 |
| 클럭 | HSE bypass 8MHz, PLL×9, HCLK·TIM1 72MHz |
| PWM 핀 | PC0 AF2 CH1 → HI, PA7 AF6 CH1N → LI |
| EN 제안 | PC6 전용 출력 LOW + 외부 풀다운, 실제 PCB 연결 확인 필요 |

전압은 `ADC × VDDA / 4095 × 19`, 전류는 `(ADC × VDDA / 4095 − 보정 영점) / 0.132`로 환산합니다. `buck_board.h`의 VDDA·전류 방향은 실측으로 확인합니다.

**PC6는 실제 PCB 배선이 확인된 신호가 아니라 이 프로필에서 채택한 전용 EN 핀입니다.** 센서 open-drain FAULT와 드라이버 EN이 같은 PCB net이면 push-pull HIGH로 강제하지 않습니다. 신호 분리 또는 적절한 논리와 외부 약 10kΩ 풀다운을 먼저 구성합니다.

## 명령과 관찰

설정 검사·센싱을 확인한 뒤 디버거에서 `buck_arm_request`를 사용합니다.

| 값 | 동작 |
|---:|---|
| 1 | 보정·입력·초기 출력·검증 플래그 조건을 만족하면 시작 |
| 2 | 정지. 고장 유지 |
| 3 | 새 ADC/타이밍 오류가 없고 전원·전류가 유효할 때 고장 해제. 재시작하지 않음 |

상태는 `0=DISARMED, 1=PRECHARGE, 2=SOFTSTART, 3=RUN, 4=FAULT`입니다. `buck_debug`에서 측정값·고장·프레임·최대 처리 cycle·PGOOD를 관찰합니다. 설정 불일치는 `BUCK_FAULT_SETUP=512`로 차단할 수 있으므로 검사 우회를 통해 구동하지 않습니다. 고장 비트·스냅샷의 정확한 필드는 `buck_app.h`에 있습니다.

## 남은 하드웨어 조건

전압 보상 이득, 듀티 0.75 상한, 전류 제한 1.15A/복귀 1.05A, 차단 1.8A·역전류 −0.4A, OVP 17V, 입력 23~36V는 조정용 값입니다. L·C·ESR·MOSFET·부하·센서 지연이 미확정이므로 안정성과 부품 보호를 보장하지 않습니다.

UCC27714 구동 전원은 데이터시트 권장 범위로 공급하며 30V를 직접 연결하지 않습니다. CH1/CH1N 하드웨어 deadtime과 실제 게이트 파형을 확인합니다. 정지는 EN LOW와 MOE 해제를 함께 사용합니다. 듀티 0만 쓰면 저측 MOSFET이 계속 켜질 수 있습니다.

ACS71240-010B3 기본 FAULT 기준은 ±10A로 이 1A급 컨버터의 빠른 단락 차단을 대신하지 않습니다. 별도 비교기→TIM1 BKIN 등 독립 보호 경로가 필요합니다. 현재 개발 프로필의 BKIN/BKIN2는 미연결·비활성 상태입니다.

출처·첨부 해시는 [ORIGIN.md](ORIGIN.md), 변경 이력은 [CHANGELOG.md](CHANGELOG.md), 수행한 검사와 미수행 검증은 [VALIDATION.md](VALIDATION.md)를 확인합니다.
