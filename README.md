# PCB Total Track Impedance Calculator

A PCB track impedance calculator to aid 
when designing PCB layouts with Altium. 

## Configuration File:

The layer stackup information, including 
controlled impedance routing (Delay, Capacitance and 
Inductance per meter) should be provided in the 
configuration file ```cfg```.

```yaml
temperature: 27 # temperature in celsius - º
layer_stack:
  Sig1:
    zo: 49.98 # characteristic impedance - Ohms
    tw: 0.1e-3 # track width in meters - m
    th: 0.01519e-3 # layer thickness - m
    dt: 6.87671 # delay per meter - ns/ m
    ind: 343.67376 # inductance per meter - nH/ m
    cap: 137.5965 # capacitance per meter - pF/ m
    material: cf-004 # material of the layer

  Sig2:
    zo: 49.98 
    tw: 0.1e-3 
    th: 0.01519e-3 
    dt: 6.92756 
    ind: 346.1959
    cap: 138.61683
    material: cf-004
```

## Usage
Example input:
```zsh
pcbtz --layer Sig1 --tl 46.8e-3 --fo 62.5e6 --iz 0+5.6j
```

Example output:
```zsh
{'--fo': '62.5e6',
 '--help': False,
 '--iz': '0+5.6j',
 '--layer': True,
 '--tl': True,
 '--tw': None,
 'LAYER_NAME': 'Sig1',
 'TRACK_LENGTH': '46.8e-3'}
{'Capacitance    [pF]:  ': 6.4395162,
 'Delay          [ns]:  ': 0.321830028,
 'Inductance     [nH]:  ': 16.083931968,
 'Resistance     [Ohm]: ': 0.6334212086899277,
 'Z0             [Ohm]: ': (0.6385405134267328+6.341120703853094j),
 '|Z0|           [Ohm]: ': 6.37318960710582}
Reflection Coefficient:  0.0818068087578706
```
