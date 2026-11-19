# Estimate steady-state PoE voltage at the powered device

This method estimates a constant-power load on a DC source and a resistive cable loop. It does not model IEEE 802.3 detection, classification, negotiation, current limiting, startup transients, bundled-cable heating or code compliance. Use the [interactive PoE cable voltage drop checker](https://deals.vyonetixsolutions.com.au/tools/poe-cable-voltage-drop-checker/?utm_source=github&utm_medium=reference&utm_campaign=engineering_toolbox) as a planning aid.

## Use the loop resistance

Enter the PSE voltage, expected steady load power and the **total loop resistance**. The resistance must account for both energized conductors, the chosen parallel-pair arrangement, cable length, patch leads and connections. Prefer measured resistance or a cable-specific calculation over a generic per-metre value.

For constant power `P`, source voltage `Vs` and loop resistance `R`, the load voltage `Vpd` follows:

```text
P = Vpd × (Vs - Vpd) / R
Vpd = (Vs + sqrt(Vs² - 4 × R × P)) / 2   (higher-voltage steady solution)
current = P / Vpd
```

When `R` is zero, the estimated load voltage equals the source voltage. If the square-root term is negative, the simplified model has no real steady-state solution for the entered values; investigate the actual PSE/device behaviour and the inputs.

## Worked example with hypothetical values

For `Vs = 48 V`, `P = 15 W`, and `R = 8 Ω`, the higher-voltage solution is about `45.35 V`. The estimated current is about `0.331 A`, so the calculated drop is about `2.65 V`. These are illustrative arithmetic results, not an IEEE class, product guarantee or installation pass.

Compare the result with the powered device's minimum input voltage and the PSE's per-port limit. Check cable temperature, bundle size and manufacturer ratings. A constant-power load draws more current as its voltage falls, so a simple `I × R` estimate using a fixed current can understate drop when the endpoint regulates its power.

## Reference

- Cisco, [PoE troubleshooting: DC loop resistance and voltage drop](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst3750/software/troubleshooting/g_power_over_ethernet.html).
