#!/usr/bin/env python3
"""Check reconstructed IOC/C agreement; this is not a CubeMX regeneration test."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent


def properties(path):
    result = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.strip() or line.lstrip().startswith(('#', '!')):
            continue
        key, value = line.split('=', 1)
        key = re.sub(r'\\(.)', r'\1', key)
        assert key not in result, f'duplicate IOC key: {key}'
        result[key] = value
    return result


def assignments(text, field):
    return [re.sub(r'\s+', '', value) for value in
            re.findall(r'\b' + re.escape(field) + r'\s*=\s*([^;]+);', text)]


def user_regions(text):
    stack = []
    result = {}
    for match in re.finditer(r'/\* USER CODE (BEGIN|END) (.*?) \*/', text):
        kind, label = match.groups()
        if kind == 'BEGIN':
            assert not stack, f'nested USER CODE: {label}'
            assert label not in result, f'duplicate USER CODE: {label}'
            stack.append((label, match.end()))
        else:
            assert stack and stack[-1][0] == label, f'unpaired USER CODE: {label}'
            _, start = stack.pop()
            result[label] = text[start:match.start()]
    assert not stack, 'unterminated USER CODE'
    return result


def main():
    p = properties(ROOT / 'buck_f303ze.ioc')
    src = ROOT / 'Core/Src'
    main_c = (src / 'main.c').read_text(encoding='utf-8')
    msp = (src / 'stm32f3xx_hal_msp.c').read_text(encoding='utf-8')
    it = (src / 'stm32f3xx_it.c').read_text(encoding='utf-8')
    assert p['Mcu.CPN'] == 'STM32F303ZET6'
    assert p['board'] == 'NUCLEO-F303ZE'
    for prefix, count_key in (('Mcu.Pin', 'Mcu.PinsNb'), ('Mcu.IP', 'Mcu.IPNb')):
        values = [p[prefix + str(i)] for i in range(int(p[count_key]))]
        assert len(values) == len(set(values)), f'duplicate {prefix}'
        assert len([key for key in p if re.fullmatch(re.escape(prefix) + r'\d+', key)]) == len(values)
    timer_hz = int(p['RCC.TIM1Freq_Value'])
    assert timer_hz == int(p['RCC.HCLKFreq_Value']) == 72000000
    assert p['TIM1.CounterMode'] == 'TIM_COUNTERMODE_UP'
    assert timer_hz / (int(p['TIM1.Prescaler']) + 1) / (int(p['TIM1.Period']) + 1) == 50000
    assert int(p['TIM1.Pulse-PWM Generation4 No Output']) / timer_hz == 5e-6
    assert p['PC0.Signal'] == 'S_TIM1_CH1' and p['PA7.Signal'] == 'TIM1_CH1N'
    assert p['PC6.Signal'] == 'GPIO_Output' and p['PC6.PinState'] == 'GPIO_PIN_RESET'
    assert p['ProjectManager.TargetToolchain'] == 'STM32CubeIDE'
    assert p['ProjectManager.KeepUserCode'] == 'true'
    assert p['ProjectManager.ProjectFileName'] == 'buck_f303ze.ioc'
    assert int(p['ADC1.NbrOfConversion']) == 3
    for i in range(3):
        suffix = f'-{i}#ChannelRegularConversion'
        assert p['ADC1.Rank' + suffix] == str(i + 1)
        assert p['ADC1.Channel' + suffix] == f'ADC_CHANNEL_{i+1}'
        assert p[f'PA{i}.Signal'] == f'ADC1_IN{i+1}'
    for key, field in (
        ('ADC1.ClockPrescaler', 'hadc1.Init.ClockPrescaler'),
        ('ADC1.ScanConvMode', 'hadc1.Init.ScanConvMode'),
        ('ADC1.ExternalTrigConv', 'hadc1.Init.ExternalTrigConv'),
        ('ADC1.ExternalTrigConvEdge', 'hadc1.Init.ExternalTrigConvEdge'),
        ('ADC1.DMAContinuousRequests', 'hadc1.Init.DMAContinuousRequests'),
        ('ADC1.NbrOfConversion', 'hadc1.Init.NbrOfConversion'),
        ('ADC1.Overrun', 'hadc1.Init.Overrun'),
        ('TIM1.Prescaler', 'htim1.Init.Prescaler'),
        ('TIM1.CounterMode', 'htim1.Init.CounterMode'),
        ('TIM1.Period', 'htim1.Init.Period'),
        ('TIM1.AutoReloadPreload', 'htim1.Init.AutoReloadPreload'),
        ('TIM1.DeadTime', 'sBreakDeadTimeConfig.DeadTime'),
        ('TIM1.OffStateRunMode', 'sBreakDeadTimeConfig.OffStateRunMode'),
        ('TIM1.OffStateIDLEMode', 'sBreakDeadTimeConfig.OffStateIDLEMode'),
        ('TIM1.AutomaticOutput', 'sBreakDeadTimeConfig.AutomaticOutput'),
        ('TIM1.TIM_MasterOutputTrigger', 'sMasterConfig.MasterOutputTrigger'),
        ('RCC.ADC12PRES', 'PeriphClkInit.Adc12ClockSelection'),
        ('USART3.BaudRate', 'huart3.Init.BaudRate'),
    ):
        assert assignments(main_c, field) == [p[key]], f'IOC/C mismatch: {key}'
    assert assignments(main_c, 'sConfig.Channel') == [f'ADC_CHANNEL_{i}' for i in (1, 2, 3)]
    assert assignments(main_c, 'sConfig.Rank') == [f'ADC_REGULAR_RANK_{i}' for i in (1, 2, 3)]
    assert assignments(main_c, 'sConfig.SamplingTime') == [p['ADC1.SamplingTime-0#ChannelRegularConversion']]
    assert assignments(main_c, 'sConfigOC.Pulse') == [p['TIM1.Pulse-PWM Generation1 CH1 CH1N'], p['TIM1.Pulse-PWM Generation4 No Output']]
    assert assignments(main_c, 'sConfigOC.OCMode') == [p['TIM1.OCMode_PWM-PWM Generation1 CH1 CH1N'], p['TIM1.OCMode_PWM-PWM Generation4 No Output']]
    for name in ('Direction', 'PeriphInc', 'MemInc', 'PeriphDataAlignment', 'MemDataAlignment', 'Mode', 'Priority'):
        assert assignments(msp, 'hdma_adc1.Init.' + name) == [p['Dma.ADC1.0.' + name]], name
    assert assignments(msp, 'hdma_adc1.Instance') == [p['Dma.ADC1.0.Instance']]
    assert '__HAL_LINKDMA(hadc, DMA_Handle, hdma_adc1)' in msp
    assert 'HAL_DMA_IRQHandler(&hdma_adc1)' in it
    assert 'HAL_ADC_IRQHandler(&hadc1)' in it
    initializers = re.findall(r'^  (MX_\w+_Init)\(\);', main_c, re.M)
    assert initializers.index('MX_DMA_Init') < initializers.index('MX_ADC1_Init')
    assert main_c.index('HAL_GPIO_WritePin(BUCK_EN_GPIO_Port, BUCK_EN_Pin, GPIO_PIN_RESET)') < main_c.index('HAL_GPIO_Init(BUCK_EN_GPIO_Port, &GPIO_InitStruct)')
    regions = {name: user_regions((src / name).read_text(encoding='utf-8')) for name in ('main.c', 'stm32f3xx_hal_msp.c', 'stm32f3xx_it.c')}
    assert 'Buck_Init();' in regions['main.c']['2']
    assert 'Buck_Poll();' in regions['main.c']['3']
    assert 'Buck_EmergencyOff();' in regions['main.c']['Error_Handler_Debug']
    assert 'buck_arm_request = 2u;' in regions['main.c']['4']
    assert 'LAB_MODE' not in main_c and 'HAL_TIM_PWM_Start(' not in re.sub(r'/\*.*?\*/', '', main_c, flags=re.S)
    combined = '\n'.join(path.read_text(encoding='utf-8') for path in src.glob('*.c'))
    for callback in ('HAL_ADC_ConvHalfCpltCallback', 'HAL_ADC_ConvCpltCallback', 'HAL_ADC_ErrorCallback'):
        assert len(re.findall(r'\bvoid\s+' + callback + r'\s*\(', combined)) == 1, callback
    for name in ('NonMaskableInt', 'HardFault', 'MemoryManagement', 'BusFault', 'UsageFault'):
        assert any('Buck_EmergencyOff();' in body for label, body in regions['stm32f3xx_it.c'].items() if label.startswith(name)), name
    profile = (ROOT / 'Core/Inc/buck_board.h').read_text(encoding='utf-8')
    assert re.search(r'#define\s+BUCK_BOARD_VERIFIED\s+0u', profile)
    assert (ROOT / 'VERSION').read_text().strip() == '0.0.2'
    assert '#define BUCK_VERSION "0.0.2"' in (ROOT / 'Core/Inc/buck_app.h').read_text()
    assert hashlib.sha256((ROOT / 'reference/v0.0.1/ex1.ioc').read_bytes()).hexdigest() == 'e97fede057d79c63cae36afb8ff8fd3d85cce6c9351ebb20e224f8dc8655fb1c'
    for name, expected in json.loads((ROOT / 'reference/uploaded/SHA256.json').read_text()).items():
        assert hashlib.sha256((ROOT / 'reference/uploaded' / name).read_bytes()).hexdigest() == expected, name
    assert (src / 'system_stm32f3xx.c').read_bytes() == (ROOT / 'reference/uploaded/system_stm32f3xx.c').read_bytes()
    print('project contract: IOC/C timing, ranks, DMA, USER CODE, callback ownership and reference hashes passed')
    print('NOT PROVEN: CubeMX schema acceptance or regenerated output equivalence')


if __name__ == '__main__':
    main()
