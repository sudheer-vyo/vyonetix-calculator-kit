# Calculate SFP optical receiver margin from a link budget

This guide explains a screening calculation for a fibre link. It is not a transceiver compatibility check or an optical certification. Vyonetix publishes the [interactive SFP link budget checker](https://deals.vyonetixsolutions.com.au/tools/sfp-optical-link-budget-checker/?utm_source=github&utm_medium=reference&utm_campaign=engineering_toolbox).

## Gather values for the exact transceiver

From the transmitter and receiver datasheets, record minimum and maximum transmit output, receiver sensitivity, and maximum receiver input. Measure or engineer the total channel loss for the installed route, including the fibre, connectors, splices and other passive components. Keep all power values in dBm and losses/margins in dB.

## Calculate both operating extremes

Use:

```text
lowest received power = minimum Tx output - path loss
sensitivity margin = lowest received power - receiver sensitivity
highest received power = maximum Tx output - path loss
overload headroom = maximum receiver input - highest received power
```

For example only, if a selected module's minimum Tx output were −8 dBm, its maximum Tx output −3 dBm, the specified receiver sensitivity −14 dBm, the receiver maximum input −1 dBm, and measured route loss 2 dB, the arithmetic gives a 4 dB sensitivity margin and 4 dB overload headroom. Those example values are not product specifications. Replace each with the values for the actual module and link.

## Interpret carefully

A positive sensitivity margin does not prove a stable link. Check wavelength, fibre type, dispersion, connector quality and reflectance, FEC/BER requirements, module limits, DOM readings, and both ends' vendor interoperability. Use field measurements for acceptance. The Vyonetix calculator intentionally reports arithmetic headroom only.

## References

- Cisco, [Gigabit Ethernet SFP module data and channel insertion loss](https://www.cisco.com/c/en/us/products/collateral/interfaces-modules/gigabit-ethernet-gbic-sfp-modules/datasheet-c78-366584.html).
- Cisco, [Optical link budget and worst-case margin](https://www.cisco.com/c/en/us/td/docs/interfaces_modules/port_adapters/install_upgrade/atm/pa-a3_ATM_install_config/pa_a3/5117ovr.html).
