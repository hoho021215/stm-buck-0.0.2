# 출처와 원본 보존 — 0.0.2

| 항목 | 값 |
|---|---|
| 새 버전 저장소 | [hoho021215/stm-buck-0.0.2](https://github.com/hoho021215/stm-buck-0.0.2) |
| 코드 출발점 | [hoho021215/stm-buck-0.0.1](https://github.com/hoho021215/stm-buck-0.0.1) |
| 확인한 0.0.1 커밋 | [`8afeccf0fa9f0db86e918d682b2de543b231f403`](https://github.com/hoho021215/stm-buck-0.0.1/commit/8afeccf0fa9f0db86e918d682b2de543b231f403) |
| 최초 원본 | [hoho021215/stm32 / stm32-buck-f303ze](https://github.com/hoho021215/stm32/tree/7ca7403b81a52a61761bc1bd1a0e785e88e7fef2/stm32-buck-f303ze) |
| 최초 원본 SHA | `7ca7403b81a52a61761bc1bd1a0e785e88e7fef2` |
| 보존한 원본 .ioc | `reference/v0.0.1/ex1.ioc` |
| 원본 .ioc 크기 / SHA-256 | 9535 bytes / `e97fede057d79c63cae36afb8ff8fd3d85cce6c9351ebb20e224f8dc8655fb1c` |

0.0.2 작업 시작 시 0.0.1의 GitHub main SHA를 확인하고 29개 원격 blob과 로컬 출발점의 해시를 대조했습니다. 원본 `hoho021215/stm32`와 0.0.1에는 쓰지 않으며 변경 사항은 지정된 0.0.2 저장소에 반영합니다.

## 이번 사용자 첨부

아래 파일을 `reference/uploaded/`에 원본 바이트로 보관합니다. 펌웨어 빌드에서 제외합니다. 첨부 안의 주석·metadata는 검토 자료이며 사용자의 작업 지시로 취급하지 않습니다.

- `.project`
- `.mxproject`
- `main.c`
- `stm32f3xx_hal_msp.c`
- `stm32f3xx_it.c`
- `system_stm32f3xx.c`

| 첨부 파일 | SHA-256 |
|---|---|
| `.project` | `87fee814150d937a0bd1d30180cb8a4dfebc90884b930700a2865a97e31458aa` |
| `.mxproject` | `efbf62d2b612d6aa894a6b1138cb858535c6437aea14ac173e635c7859375a6d` |
| `main.c` | `a5744a6cfadd174725b8a7e799f7f0a12a57376eecc571ae6f2573e347478caa` |
| `stm32f3xx_it.c` | `8043500d499397bbc4330e0e5d4048d2aa83a97f6ab09a17ace97312e5ba2477` |
| `stm32f3xx_hal_msp.c` | `ff0d90e283c4b1817df60d5fe54243b9f3bdf2d40eaffcc7e926b98335ab7be1` |
| `system_stm32f3xx.c` | `f1482dd9661a091b418f4479d837c30a60744f4f6021c4dd516da08e5e951169` |

첨부에는 `.ioc`, `.cproject`, `main.h`, IRQ/HAL config 헤더, startup·linker·vendor pack 전체가 없습니다. `buck_f303ze.ioc`와 관련 초기화 참고본은 수작업 재구성한 개발 목표이며 첨부 원본의 완전 역변환이나 실제 CubeMX 생성 결과로 표시하지 않습니다.

`Core/Src/system_stm32f3xx.c`는 첨부 원본을 사용합니다. system source는 제품 빌드에서 한 개만 포함합니다. 파일별 검증 해시와 버전 표식은 `RELEASE_MANIFEST.json`, 변경 이유는 [CHANGELOG.md](CHANGELOG.md), 실제 검사 범위는 [VALIDATION.md](VALIDATION.md)에 기록합니다.
