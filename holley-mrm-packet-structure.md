# Holley MRM packet structure


### Meter Reading Message (MRM)
| Size (byte)   | 1         | \[0...30\]    |
|---------------|-----------|---------------|
| Name          | Header    | Content       |


### Header

| Bit#          | 7..6      | 5..1      | 0         |
|-|-|-|-|
| Name          | Mark      | Identifier| Status    |

#### Mark

| Mark Bits     | Description                       |
|-|-|
| 00            | LoRaWAN Meter Protocol V1         |
| 01..11        | Reserved for Future use           |

#### Identifier

| Qualifier Bits    | Meter Type    | Description    |
|-|-|-|
| 00000             | None (when only sending status) | |
| 00111             | mME-DTZ541    | Record 1 from Meter |
| 01000             | mME-DTZ541    | Record 2 from Meter |
| 01001..11111      | Reserved for Future use           | |

#### Record 1

| Byte-Length | 14              | 3             | 2                 | 4             | 2                 |
|-|-|-|-|-|-| 
| Content     | Meter Number    | Meter FW Ver  | Meter FW Checksum | Adapter FW Ver| LoRa Module FW Ver|

#### Record 2

| Byte-Length | 5 | 5 | 5 | 5 | 5 | 5 | 3 | 3 | 3 | 3 | 4 | 4 |
|-|-|-|-|-|-|-|-|-|-|-|-|-|
| Content | 1.8.0 (Active Wh L1) | 1.8.1 (Active Wh L2) | 1.8.2 (Active Wh L3) | 2.8.0 (Active Wh returned L1) | 2.8.1 (Active Wh returned L2) | 2.8.2 (Active Wh returned L3) | Psum | P(L1) | P(L2) | P(L3) | Status Word | Second index |

where x.x.x is OBIS codes

#### Status bits

| Value | Description|
|-|-|
| 0 | Not OK, serious errors within metrological part of the meter |
| 1 | OK |

#### Hex interpretation

5 Byte Usage (0,1Wh):\
Z.B 000000FFFF interpreted as 65.535*0,1*Wh = 6553,5 Wh= 6,5535 kWh\
3 Byte Usage (0,1W):\
z.B. 0000FF interpreted as 255*0,1*W = 25,5 W

#### Example payload

```1100000623CD00000623CD00000000000000000000000000000000000000000000610000000000610000000008010400483A68```


```
Verbrauchswert_1.8.0: "40.2381 kWh",
Verbrauchswert_1.8.1: "40.2381 kWh",
Verbrauchswert_1.8.2: "0 kWh",
Verbrauchswert_2.8.0: "0 kWh",
Verbrauchswert_2.8.1: "0 kWh",
Verbrauchswert_2.8.2: "0 kWh",
Leistung_PSumme: "9.7 W",
Leistung_PL1: "0 W",
Leistung_PL2: "9.7 W",
Leistung_PL3: "0 W",
Sekundeindex: 4733544,
Statuswort: "00080104",
• "S08_Messwerk": "Anlauf",
• "S09_Magnetische_Manipulation": "Nein",
• "S10_Klemmendeckel_Manipulation": "Nein",
• "S11_Energierichtung": "+A",
• "S12_Energierichtung_L1": "+A",
• "S13_Energierichtung_L2": "+A",
• "S14_Energierichtung_L3": "+A",
• "S15_Drehfeld_L1_L2_L3": "Ja",
• "S16_Ruecklaufsperre": "inaktiv",
• "S17_Fehler_eichrelevant": "Nein",
• "S18_Spannung_L1": "nicht vorhanden",
• "S19_Spannung_L2": "vorhanden",
• "S20_Spannung_L3": "nicht vorhanden"
```

