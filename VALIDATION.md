# 0.0.2 검증 기록

이번 버전의 실제 파일로 클라우드 Linux x86_64에서 실행했습니다. 호스트 GCC 14.2.0, ARM GCC 14.2.1을 사용했으며 공통 옵션은 C11, `-O2 -Wall -Wextra -Werror -Wpedantic`입니다. STM32 보드와 사용자 PC에는 접근하지 않았습니다.

## 실행 방법

Linux/WSL에 Python 3, Git, GCC를 준비하고 저장소 루트에서 실행합니다. 처음 실행하면 아래 고정 커밋의 공식 헤더를 무시되는 `tests/.deps/`에 받습니다.

```sh
sh tests/run_host_tests.sh --sanitize
```

Arm GNU toolchain과 newlib 헤더를 설치했다면 ARM 객체 컴파일도 수행할 수 있습니다.

```sh
ARM_CC=arm-none-eabi-gcc sh tests/run_host_tests.sh --sanitize --arm
```

이번 실행은 이미 받은 의존성의 HEAD·tracked 파일이 변경되지 않았음을 검사한 뒤 다음과 같이 offline 모드로 수행했습니다. `/path/to/`는 사용자의 실제 경로로 바꿉니다.

```sh
BUCK_HAL_DIR=/path/to/stm32f3xx-hal-driver \
BUCK_DEVICE_DIR=/path/to/cmsis-device-f3 \
BUCK_CMSIS_DIR=/path/to/CMSIS_5 \
ARM_CC=arm-none-eabi-gcc \
sh tests/run_host_tests.sh --offline --sanitize --arm
```

이 환경에서는 Debian ARM GCC·newlib 헤더 패키지를 작업 공간에만 추출했고 `ARM_CC`에 그 실행 파일 경로, `BUCK_ARM_INCLUDE`에 추출한 newlib include 경로를 지정했습니다. 정상 설치한 도구체인은 보통 추가 include 환경변수가 필요하지 않습니다. 도구체인·vendor 저장소·생성된 객체는 게시 파일에 포함하지 않습니다.

| 공식 의존성 | 사용 커밋 |
|---|---|
| ST stm32f3xx-hal-driver | `664a3bd898dc001d253a47c3e058d4f053cc4da5` |
| ST cmsis-device-f3 | `402c039a0a6d73c31303a05e6a1d6b8b59474fa1` |
| Arm CMSIS_5 | `55b19837f5703e418ca37894d5745b1dc05e4c91` |

이는 API·컴파일 검사용 고정 의존성입니다. `.ioc`에 기록된 Cube FW_F3 1.11.6 전체 생성 프로젝트를 링크한 결과와 구분합니다. 실제 소스는 `Core/Inc/stm32f3xx_hal_conf.h`를 사용합니다. `tests/generated_stubs`는 생략된 초기화 선언이 있는 `.example`의 호스트 문법 검사에만 사용하며 제품 소스의 대역이 아닙니다.

## 실제 결과

| 검사 | 결과 |
|---|---|
| 출력 감시 모듈 | PGOOD 유지 시간·히스테리시스, UV 50ms, 경계값·비유한 값·계수 포화 시험 통과 |
| 하드웨어 설정 검사 | 읽기 전용 MMIO **40건** 통과. Rank·클럭·DMA Parent·핀·TIM 오류 거부와 검사 자체의 무변경 확인 |
| 앱 동작 | 호스트 시나리오 **22건** 통과. 기동·정지·bootstrap·MOE 소실·센서/타이밍 오류·보호·수동 복구 검사 |
| 제품 기본 기동 차단 | `BUCK_BOARD_VERIFIED=0`을 유지한 별도 빌드에서 시작 명령으로 게이트가 켜지지 않음 |
| 소스 문법 | 실제 `Core/Src` 소스 7개 및 위치 예제 2개의 공식 HAL/CMSIS 헤더 문법 검사 통과 |
| sanitizer | supervisor ASan+UBSan, 앱·MMIO UBSan 통과. 고정 MMIO 주소와 ASan shadow 충돌 때문에 해당 두 시험의 ASan 통과는 주장하지 않음 |
| 프로젝트 계약 검사 | `.ioc`의 핀/IP 목록·50kHz/5µs 계산, C와 ADC Rank·DMA·타이머 설정 일치, 초기 EN LOW, USER CODE 쌍·연동 위치, ADC 콜백 단일 정의, 버전·기동 차단 확인 |
| 원본 보존 | 첨부 6개와 이전 `ex1.ioc` SHA-256 일치. system source는 첨부와 바이트 단위 동일 |
| ARM 대상 컴파일 | **Cortex-M4F용 production 소스 7개 `.o` 생성 성공**. `-mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard` 사용. `readelf`로 ARM ELF32 relocatable 확인 |

대표 실행 출력:

```text
buck_supervisor: all tests passed
hardware configuration: 40 read-only MMIO cases passed
buck_app: 22 host scenarios passed; production board flag remains 0
default-off profile: calibrated start request cannot enable gates
project contract: IOC/C timing, ranks, DMA, USER CODE, callback ownership and reference hashes passed
NOT PROVEN: CubeMX schema acceptance or regenerated output equivalence
PASS: 7 Cortex-M4F production objects compiled (not linked)
PASS: host suites, production source syntax, IOC/C contract and default-off profile
NOT TESTED: ARM link, real CubeMX regeneration, ISR WCET, power-stage behavior
```

호스트 시험은 HAL·시간·MMIO를 모의한 검사입니다. 제어 입력의 시험 궤적은 LC 전력단 시뮬레이션이 아닙니다.

## 수행하지 않은 검사와 남은 조건

- ARM 최종 링크, startup·linker·vendor 전체 빌드 및 플래시용 ELF/HEX/BIN 생성: 미수행.
- CubeMX에서 `.ioc` 열기, 스키마 수용·마이그레이션, Generate Code 및 USER CODE 왕복 보존: 미수행.
- 실제 ADC/DMA 동기·최악 실행시간·게이트 중첩·deadtime·bootstrap·LC 안정성·부하 과도·단락 시험: 미수행.

새 `.ioc`는 첨부 C와 이전 설정에서 재구성한 개발 목표입니다. 정적 계약 검사는 CubeMX 앱의 인식·재생성 성공을 입증하지 않습니다. 사용자 CubeMX로 빈 폴더에 생성하고 [설정표](CUBEMX_SETUP.md)와 생성된 코드를 비교해야 합니다.

L·C/ESR·MOSFET 정격, PC6 전용 EN 배선과 외부 풀다운, FAULT 분리, VDDA·전류 방향·센서 지연 및 보호 임계값을 확정하기 전에는 `BUCK_BOARD_VERIFIED=0`을 유지합니다.

## 후속 ex1.ioc 첨부 확인

추가 작업에서는 제품 소스·개발 목표 `.ioc`를 변경하지 않았습니다. 첨부한 `ex1.ioc`는 9535 bytes이며 이전 원본과 바이트 단위로 동일합니다. CubeMX 형식의 속성 261개에 중복 키가 없고, IP 9개·핀 23개 목록과 ADC/TIM/RCC 속성 참조의 정적 일치를 확인했습니다.

`python3 tests/test_project_contract.py`를 재실행하여 새 첨부를 포함한 7개 원본의 해시와 기존 IOC/C 계약 검사가 통과함을 확인했습니다. 위의 호스트·ARM 객체 검사 결과는 제품 소스가 동일한 직전 게시에서 수행한 결과이며, 이번 문서·원본 추가 때문에 전체 컴파일을 반복한 것으로 표현하지 않습니다. 실제 CubeMX 열기·재생성은 계속 미검증입니다.

초기 설정 가이드 `GETTING_STARTED_KO.md`는 ST 공식 설치·프로젝트 생성 설명과 현재 저장소의 파일·설정에 맞춰 작성했습니다. 상대 문서 링크와 복사 대상 벅 모듈 8개의 경로를 정적으로 확인했으며 사용자 PC에서 설치·GUI 메뉴·전체 생성 절차를 실제 실행한 검증으로 표현하지 않습니다.
