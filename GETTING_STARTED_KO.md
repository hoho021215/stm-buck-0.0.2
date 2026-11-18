# 처음부터 설정하기: STM32CubeMX → STM32CubeIDE

대상은 **NUCLEO-F303ZE / STM32F303ZET6**, 이 저장소의 **0.0.2 개발 프로필**입니다. Windows 경로를 예시로 들며 다른 OS에서도 메뉴 흐름은 같습니다. 이 문서는 설치·프로젝트 생성·코드 연결·첫 빌드를 위한 안내입니다. 실제 CubeMX 재생성과 보드 구동을 검증한 결과는 아니며, 수행한 검사는 [VALIDATION.md](VALIDATION.md)에 있습니다.

읽는 순서: **이 문서 → [주변장치 설정표](CUBEMX_SETUP.md) → [USER CODE 삽입 안내](CUBEMX_USER_CODE.md)**.

## 1. 설치할 프로그램

| 프로그램 | 역할 | 설치 링크 |
|---|---|---|
| STM32CubeMX 6.x | `.ioc` 열기, 핀·ADC·TIM 설정, 초기화 코드 생성 | [ST 공식 CubeMX](https://www.st.com/content/st_com/en/stm32cubemx.html) |
| STM32CubeIDE for Eclipse | 생성 프로젝트 가져오기, C 편집·빌드·디버깅 | [ST 공식 CubeIDE](https://www.st.com/content/st_com/en/stm32cubeide.html) |
| STM32CubeF3 MCU Package | F3용 HAL·CMSIS·템플릿 | 다음 단계에서 CubeMX로 설치 |

이 저장소는 **CubeMX 6.x의 `.ioc`와 `USER CODE` 형식**을 사용합니다. CubeMX2나 VS Code용 새 프로젝트 흐름을 이 안내와 혼용하지 않습니다. `.ioc`에 기록된 버전은 CubeMX **6.18.1**, firmware pack **STM32Cube FW_F3 V1.11.6**입니다. 같은 버전을 사용할 수 있으면 우선 맞추고, 다른 버전으로 열 때는 복사본을 마이그레이션하고 실제 사용 버전을 기록합니다.

CubeIDE **2.0부터 CubeMX가 분리**되어 별도 설치·실행이 필요합니다. IDE 안에 `.ioc` 설정 화면이나 예전 프로젝트 생성 메뉴가 없다고 설치 실패로 판단하지 않습니다. 이 가이드는 별도 CubeMX에서 생성한 뒤 IDE로 가져오는 흐름을 사용합니다. [ST의 2.0 변경 안내](https://community.st.com/stm32cubeide-mcus-28/stm32cubeide-2-0-0-released-159542)

설치 파일은 OS에 맞게 받고 설치기를 실행합니다. ST 계정·약관 확인이 나타나면 설치기의 안내를 따릅니다. Windows에서 IDE 설치기가 ST-LINK 드라이버 설치를 제안하면 함께 설치합니다. CubeIDE가 제공하는 Arm 도구체인을 사용하면 펌웨어 빌드를 위해 PC의 별도 GCC를 설치할 필요는 없습니다. Git·Python·호스트 GCC는 저장소의 Linux/WSL 시험을 실행할 때 별도로 필요합니다.

## 2. F3 firmware pack 준비

1. CubeMX를 실행합니다.
2. **Help → Manage embedded software packages** 또는 홈의 **INSTALL/REMOVE**를 엽니다.
3. **STM32Cube MCU Packages → STM32F3**에서 프로젝트의 F3 패키지를 설치합니다. 요청 버전이 없으면 사용 가능한 호환 버전을 선택하고 변경 사항을 기록합니다.
4. 다운로드가 안 되면 CubeMX의 로그인·연결 설정을 확인합니다. 공식 패키지 ZIP을 미리 받았다면 패키지 관리자의 **From Local…**로 설치할 수도 있습니다.

설치 방법과 패키지 관리 메뉴는 [ST CubeMX 설치 설명](https://dev.st.com/stm32cube-docs/stm32cubemx/6.18.1/en/docs/markup/CubeMX_UserManual/chapters/03_3_installing_and_running_stm32cubemx.html)을 기준으로 합니다. 라이브러리가 없는 상태에서 Generate Code가 실패하면 소스에 임의의 HAL 헤더를 복사해 해결하지 않습니다.

## 3. 원본과 생성 폴더를 분리

GitHub에서 **Code → Download ZIP**으로 저장소를 받아 압축을 풀거나 Git으로 내려받습니다. 아래는 경로 예시입니다.

```text
C:/STM32/source/stm-buck-0.0.2/      ← 내려받은 저장소, 참고 자료
C:/STM32/projects/buck_f303ze/      ← 새로 생성할 펌웨어 프로젝트
C:/STM32/workspace/                ← CubeIDE workspace
```

새 프로젝트 폴더에는 저장소 루트의 **[buck_f303ze.ioc](buck_f303ze.ioc) 하나만** 복사해 시작합니다. 파일명과 프로젝트명을 `buck_f303ze`로 맞춥니다.

**[reference/uploaded/ex1.ioc](reference/uploaded/ex1.ioc)는 약 10kHz·단일 ADC 원본**입니다. 이전 보존본과 동일하며 50kHz 벅용 개발 목표가 아닙니다. 현재 코드와 연결할 때는 루트의 `buck_f303ze.ioc`를 사용합니다.

`reference/`, `tests/`, `integration/`을 생성 프로젝트에 통째로 복사하면 중복 main·콜백이나 호스트 시험 소스가 빌드에 들어갈 수 있습니다. 아래 단계에서 필요한 제품 모듈만 복사합니다.

## 4. CubeMX에서 .ioc 열기와 Project Manager 설정

CubeMX의 **File → Load Project…** 또는 홈의 프로젝트 열기에서 새 폴더의 `buck_f303ze.ioc`를 선택합니다. 새 Board Selector 프로젝트를 다시 만들어 기본 핀을 덮어쓸 필요는 없습니다. MCU가 **STM32F303ZETx / LQFP144**, 보드가 **NUCLEO-F303ZE**인지 확인합니다.

마이그레이션 창이 뜨면 파일 복사본을 보존하고, 변경 후 [설정표](CUBEMX_SETUP.md)와 비교합니다. 프로젝트를 열었다는 사실만으로 수작업 `.ioc`의 모든 속성이 받아들여졌다고 판단하지 않습니다.

**Project Manager → Project**에서 확인합니다.

| 항목 | 선택·확인값 |
|---|---|
| Project Name | `buck_f303ze` |
| Project Location | 프로젝트 폴더의 상위 위치. 예: `C:/STM32/projects` |
| 최종 생성 경로 | `C:/STM32/projects/buck_f303ze`인지 확인 |
| Toolchain / IDE | **STM32CubeIDE** |
| Generate under root | 켬: `.project`·`.cproject`를 `.ioc`와 같은 프로젝트 루트에 생성 |
| Firmware Package | 설치한 STM32CubeF3 버전. `.ioc` 기록은 V1.11.6 |

**Project Manager → Code Generator**에서 `Keep User Code when re-generating`을 켜고 필요한 라이브러리를 프로젝트에 복사하도록 선택합니다. 초기화 함수를 `main.c`에 모으려면 **Generate peripheral initialization as a pair of .c/.h files per peripheral**은 끕니다. 주변장치를 파일별로 나눴다면 실제 생성된 include·핸들 위치를 기준으로 연결해야 합니다.

**Advanced Settings → Generated Function Calls**에서 GPIO 초기화와 **MX_DMA_Init이 MX_ADC1_Init보다 먼저** 호출되는지 확인합니다. ADC/TIM 등은 HAL로 생성하고 별도 HAL callback 등록 옵션은 기본 비활성 상태를 유지합니다. 이 프로젝트의 ADC callback은 `buck_app.c`에서 구현합니다.

프로젝트 위치·코드 생성 옵션은 [ST CubeMX Project Manager 설명](https://dev.st.com/stm32cube-docs/stm32cubemx/6.18.1/en/docs/markup/CubeMX_UserManual/chapters/04_4_stm32cubemx_user_interface.html)을 참고합니다.

## 5. 핀·클럭·ADC·TIM 확인 후 Generate Code

상세 값은 [CUBEMX_SETUP.md](CUBEMX_SETUP.md)에 있습니다. 우선 아래 항목이 보이는지 확인합니다.

| 화면 | 핵심 확인 |
|---|---|
| RCC / Clock Configuration | HSE bypass 8MHz, PLL×9, HCLK·TIM1 72MHz, ADC12 PLL/1, USB 48MHz |
| TIM1 | Up, PSC0, ARR1439, PC0 CH1/PA7 CH1N, 내부 CH4 PWM2·CCR360·OC4REF TRGO |
| Deadtime / 출력 상태 | DTG22 후보, OSSI·OSSR enable, AOE disable. 실제 파형 검증 필요 |
| ADC1 | PA0 IL / PA1 Vout / PA2 Vin 순서, 3 ranks, async DIV1·19.5cycles, TRGO rising |
| ADC DMA | DMA1 Channel1, circular, halfword/halfword, memory increment |
| GPIO | PC6 EN output 초기 LOW. 실제 전용 배선과 외부 풀다운 필요 |
| NVIC / SYS | DMA·ADC·EXTI priority0, USB2, SysTick3, SWD 디버그 유지 |

오류가 표시되면 해당 설정을 먼저 해결하고 **GENERATE CODE**를 누릅니다. 펌웨어 다운로드 요청이 있으면 패키지 설치를 완료합니다. 생성된 폴더에서 다음 파일·폴더를 확인합니다.

```text
buck_f303ze.ioc
.project / .cproject
Core/Inc/ 및 Core/Src/
Drivers/
startup 파일 및 STM32F303ZE용 linker script
```

IDE 설정 파일이 도구체인 하위 폴더에 생겼다면 실제 `.project`가 있는 위치를 가져옵니다. 저장소의 첨부 `.project`·`.mxproject`를 빈 폴더에 복사하는 것으로 이 단계를 대신하지 않습니다.

## 6. CubeIDE로 가져오기

CubeIDE를 실행하고 workspace 예시 `C:/STM32/workspace`를 선택합니다. 생성된 프로젝트 폴더와 workspace는 별개의 개념입니다.

IDE 버전에 따라 메뉴 이름이 다릅니다.

- `File → STM32 Project Create/Import` 또는 `File → Import STM32 Project`에서 **STM32CubeMX/STM32CubeIDE Project**를 선택합니다.
- 해당 메뉴가 없으면 `File → Import… → General → Existing Projects into Workspace`에서 생성된 `.project`가 있는 폴더를 선택합니다.

여러 후보가 나오면 `buck_f303ze` 프로젝트만 선택합니다. **Copy projects into workspace는 끄는 방법을 권장**합니다. CubeMX와 IDE가 같은 폴더를 계속 사용해야 하기 때문입니다. 복사 옵션을 사용하면 이후 CubeMX도 IDE가 실제 사용하는 복사본의 `.ioc`를 열어야 합니다.

Project Explorer에서 `Core`, `Drivers`, startup·linker 항목이 보이는지 확인하고 프로젝트를 우클릭해 **Refresh**합니다. import 메뉴 예시는 [ST AN5361의 프로젝트 가져오기 절차](https://www.st.com/resource/en/application_note/dm00629855-getting-started-with-projects-based-on-dual-core-stm32h7-microcontrollers-in-stm32cubeide-stmicroelectronics.pdf)를 참고할 수 있습니다. 해당 문서의 H7 전용 설정은 F303에 적용하지 않습니다.

## 7. 벅 모듈과 USER CODE 추가

저장소에서 생성 프로젝트로 **아래 8개 파일만** 먼저 복사합니다.

| 복사할 원본 | 생성 프로젝트의 위치 |
|---|---|
| `Core/Src/buck_app.c` | `Core/Src/` |
| `Core/Src/buck_hw.c` | `Core/Src/` |
| `Core/Src/buck_supervisor.c` | `Core/Src/` |
| `Core/Inc/buck_app.h` | `Core/Inc/` |
| `Core/Inc/buck_board.h` | `Core/Inc/` |
| `Core/Inc/buck_hw.h` | `Core/Inc/` |
| `Core/Inc/buck_platform.h` | `Core/Inc/` |
| `Core/Inc/buck_supervisor.h` | `Core/Inc/` |

복사 후 IDE에서 프로젝트를 선택하고 **Refresh(F5)**하여 소스 3개·헤더 5개가 Project Explorer에 보이는지 확인합니다.

`buck_board.h`의 **BUCK_BOARD_VERIFIED=0**을 유지합니다. 이어 [USER CODE 안내](CUBEMX_USER_CODE.md)를 따라 다음을 넣습니다.

- `main.c`의 `Includes`: `#include "buck_app.h"`.
- `main.c`의 `USER CODE 2`: 초기화 함수 호출 뒤 `Buck_Init();`.
- `main.c`의 `USER CODE 3`: 반복문 안 `Buck_Poll();`.
- `USER CODE 4`: 참고 main의 PC13 정지 callback 내용. 이미 `HAL_GPIO_EXTI_Callback`이 있으면 한 함수로 병합.
- `Error_Handler_Debug`: IRQ 차단 후 `Buck_EmergencyOff();`, 기존 무한 루프 유지.
- IRQ 파일의 `Includes`와 NMI·HardFault·MemManage·BusFault·UsageFault 사용자 구역: 참고 코드의 비상 차단 처리.

생성된 main/MSP/IRQ/헤더 전체를 저장소의 수작업 참고본으로 덮어쓰지 않습니다. 생성된 DMA·ADC IRQ의 HAL 호출을 유지하고 **HAL_ADC_*Callback은 buck_app.c 한 곳에만** 둡니다. HAL PWM/ADC 시작 함수를 따로 추가하지 않습니다. 시스템 소스도 한 개만 빌드합니다.

## 8. 첫 빌드

프로젝트를 선택한 뒤 `Properties → C/C++ Build → Settings` 등 해당 버전의 설정 화면에서 확인합니다.

| 항목 | 확인값 |
|---|---|
| MCU / CPU | STM32F303ZE / Cortex-M4 |
| FPU / ABI | fpv4-sp-d16 / hard-float. 프로젝트·라이브러리 ABI 일치 |
| 전처리 정의 | `STM32F303xE`, `USE_HAL_DRIVER` |
| include 경로 | 생성된 `Core/Inc` 및 HAL/CMSIS 경로 |
| 최적화 | 검증할 Debug/Release 구성 모두 `-O2`; `-ffast-math` 사용하지 않음 |
| 빌드 소스 | 벅 3개 소스 포함, reference·tests·example 제외 |

**Project → Clean… → Build Project**를 실행하고 Console의 첫 오류부터 해결합니다. 정상 완료 후 `Debug/` 또는 선택한 구성 폴더의 `.elf`가 만들어지는지 확인합니다. 저장소에서 수행한 ARM 검사는 `.o` 컴파일까지이며, 사용자의 생성 프로젝트 전체 링크 성공을 미리 보장한 것은 아닙니다.

| 증상 | 먼저 확인할 것 |
|---|---|
| 프로젝트를 찾지 못함 | Generate Code 완료 여부, `.project`가 있는 실제 폴더 선택 |
| HAL/CMSIS 헤더 없음 | F3 pack 설치·라이브러리 복사 옵션·생성 완료 여부 |
| `buck_app.h` 없음 | 헤더 복사와 `Core/Inc` include 경로 |
| `Buck_*` undefined reference | 벅 `.c` 3개가 프로젝트에 포함·빌드되는지 |
| ADC callback/main 중복 정의 | LAB 코드·reference·tests가 섞였는지, callback이 한 곳인지 |
| FPU ABI 링크 오류 | 모든 대상의 hard/soft-float ABI·선택 라이브러리 일치 |
| ADC/TIM 필드·매크로 오류 | 선택 MCU와 실제 F3 pack/HAL 버전, 마이그레이션 차이 |

## 9. 초기 관찰과 재생성

이 단계까지의 목표는 **프로젝트 생성·코드 연결·빌드**입니다. 전력단 기동 허용은 배선·보호·센싱·게이트 파형 검증 뒤 별도 판단합니다. MCU만 USB로 확인할 때도 `BUCK_BOARD_VERIFIED=0`을 유지하며 시작 명령을 넣지 않습니다. 센서가 무전원·미연결이면 ADC 또는 영점 오류가 날 수 있으므로 성공 상태를 만들기 위해 검사를 우회하지 않습니다.

디버거의 `buck_debug`, `buck_fault_snapshot`, `buck_arm_request`를 관찰할 수 있습니다. `BUCK_FAULT_SETUP=512`이면 ADC clock/rank, DMA Parent, CH4/TRGO, GPIO와 deadtime·OSSI/OSSR를 [설정표](CUBEMX_SETUP.md)와 비교합니다. 검증 플래그를 1로 바꿔 설정 오류를 숨기지 않습니다.

ADC 제어 ISR은 20µs 주기와 DWT 실행시간을 검사합니다. ISR breakpoint·단계실행·printf는 F_TIMING/F_ADC를 만들 수 있습니다. 초기 breakpoint는 ADC 수집이 시작되기 전인 `Buck_Init` 호출 전에 둡니다. 수집 시작 뒤에는 실행을 유지하는 Live Expressions 등의 관찰 방법을 사용합니다. halt로 수집을 중단했다면 다시 확인할 때 reset부터 시작하는 방법이 좋습니다.

다시 설정을 바꿀 때는 **IDE가 사용하는 프로젝트 폴더의 같은 `.ioc`**를 CubeMX에서 엽니다. 저장·Generate Code 후 IDE Refresh, USER CODE diff 확인, Clean/Build를 반복합니다. 현재 저장소의 `.ioc` 왕복 생성·실물 검증은 미수행이므로 설정이 자동 보정됐다면 그 차이를 기록해야 합니다.
