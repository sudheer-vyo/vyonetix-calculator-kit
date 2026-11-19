# Compare uncompressed video bandwidth with link payload

Pixel resolution and refresh rate alone do not describe the required link rate. The timing includes blanking intervals, and chroma format changes the bits carried per pixel. The [Vyonetix video link bandwidth estimator](https://deals.vyonetixsolutions.com.au/tools/display-video-link-bandwidth-estimator/?utm_source=github&utm_medium=reference&utm_campaign=engineering_toolbox) compares an entered pixel clock and colour format with an entered usable payload rate.

## Calculate the uncompressed stream rate

```text
rate (Gb/s) = pixel clock (MHz) × bits per pixel / 1000
```

For component bit depth `b`, use `3b` bits/pixel for 4:4:4, `2b` for 4:2:2, and `1.5b` for 4:2:0. Use the mode's total pixel clock, including blanking, and compare against usable link payload after coding/transport overhead. A raw signaling rate is not the same as usable payload.

For a hypothetical 594 MHz timing at 8 bits per component, the uncompressed estimate is 14.256 Gb/s for 4:4:4, 9.504 Gb/s for 4:2:2 and 7.128 Gb/s for 4:2:0. These figures omit audio and secondary data, and do not account for Display Stream Compression (DSC).

## Check the endpoints and mode

Verify the exact timing, bit depth, chroma, color format, link rate, lane count and transport supported by both source and display. Check whether DSC is enabled and supported end-to-end. Consult the applicable VESA or HDMI source material and device specifications; this simplified estimate is not a certification or compatibility verdict.

## References

- VESA, [DisplayPort HBR3 and link payload overview](https://vesa.org/featured-articles/vesa-rolls-out-early-certification-program-for-video-source-and-display-products-using-hbr3-high-bandwidth-link-rate/).
- VESA, [DisplayPort compliance information](https://compliance.vesa.org/).
