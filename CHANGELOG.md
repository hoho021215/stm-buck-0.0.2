# 변경 기록

## 0.0.2

사용자가 제공한 CubeIDE 스타일의 C·metadata를 검토하고, 별도 저장소 `hoho021215/stm-buck-0.0.2`에 통합한 개발 버전입니다. 출발 커밋과 보존 원본은 [ORIGIN.md](ORIGIN.md)를 확인합니다.

### 설정·통합

- `buck_f303ze.ioc` 개발 프로필 추가. 첨부 C와 0.0.1의 preflight 조건을 근거로 수작업 재구성했으며 실제 CubeMX Generate Code 실행본이라고 표현하지 않음.
- 약 10kHz center-aligned/ARR3599 목표를 Up/ARR1439의 50kHz로 변경.
- ADC1 3채널 순서 IL/Vout/Vin, async PLL72MHz/1, 19.5cycle, TIM1 OC4REF trigger, DMA1 Channel1 circular halfword 연결 추가.
- 내부 CH4 PWM2/CCR360, DTG22, OSSI/OSSR enable와 PC6 전용 EN 초기 LOW 개발 설정 추가.
- 첨부의 `USER CODE` 형식을 유지한 main·MSP·IRQ·헤더 통합 참고본 추가.
- LAB_COPY/SPWM, software trigger 덮어쓰기, ADC polling/DAC 복사, 듀티50% 자동 PWM 시작을 벅 앱 통합 경로로 교체.
- 오류·fault의 게이트 차단, PC13 정지 및 DMA/ADC HAL IRQ 연결 정리.
- 첨부 원본 6개와 변경 전 ex1.ioc를 `reference/`에 보존하고 빌드 제외 안내 추가.
- CubeMX 생성 후 직접 넣을 사용자 구역과 주변장치 변경 절차를 한글로 설명.

### 유지·한계

- 0.0.1의 피드포워드·소프트스타트·듀티 상승 제한·전류 duty-cap·anti-windup·기동 및 타이밍 감시·출력 UV·PGOOD·첫 고장 기록 유지.
- `BUCK_BOARD_VERIFIED=0` 기본 기동 차단 유지.
- 기존 제어 이득과 보호 임계값을 검증된 새 값으로 포장하지 않음.
- L·C/ESR·MOSFET이 미확정인 평균 전류 이중 루프·CC/CV·예측 제어는 구현 대상으로 확정하지 않음.
- CubeMX 재생성, ARM 대상 검사와 실제 보드 검증 중 실제 수행한 범위만 [VALIDATION.md](VALIDATION.md)에 기록.

## 0.0.1

기준 커밋 `8afeccf0fa9f0db86e918d682b2de543b231f403`. 최초 원본은 `hoho021215/stm32@7ca7403b81a52a61761bc1bd1a0e785e88e7fef2`의 `stm32-buck-f303ze`입니다.

- 정상 기동 후 UV 히스테리시스·50ms 차단과 PGOOD ±5%/5ms 자격 시간 추가.
- 첫 고장 raw ADC·환산값·제어 상태 스냅샷 추가.
- ADC/TIM/DMA 실제 설정 preflight, DMA Parent 연결, bootstrap MOE 소실, 명시적 clear와 초기 ADC watchdog 조건 보강.
- 재현 가능한 호스트 시험과 고정 공식 HAL/CMSIS 의존성 추가.
- 원본 ex1.ioc 보존과 기본 기동 차단 유지.
