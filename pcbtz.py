"""
Compute the total self impedance from the track length 
and impedance characteristics of each layer from 
the Altium layer stack.

Usage: pcbtz --layer LAYER_NAME --tl TRACK_LENGTH [options]

Options:
  -h --help         Show this message and leave.
  --tw TRACK_WIDTH  Width of the track.
  --fo OP_FREQUENCY Operating frequency.
  --iz INTERFACE_IMP Interface impedance to compute reflection coef.

"""
from docopt import docopt
import yaml
from pprint import pprint
from pathlib import Path

__material_resistivity = {
    "cf-004": 1.7e-8 # Ohm . m
}

__material_temp_alpha = {
    "cf-004": 3.9e-3 # Ohm / Ohm / ºC
}

def main():
    args = docopt(__doc__)
    pprint(args)
    with open(Path(str(Path(__file__).resolve().parents[0]) + './cfg'), 'r') as cfgfile:
        cfg = yaml.safe_load(cfgfile)
    layerid = args['LAYER_NAME']
    tl = float(args['TRACK_LENGTH'])
    dt = tl*float(cfg['layer_stack'][layerid]['dt'])
    tw = float(cfg['layer_stack'][layerid]['tw'])
    th = float(cfg['layer_stack'][layerid]['th'])
    if args.get('--tw', None) != None:
        tw = float(args['--tw'])
    material = cfg['layer_stack'][layerid]['material']
    temp_coef = 1 + __material_temp_alpha[material] * (cfg['temperature']-25)
    res = temp_coef * __material_resistivity[material] * tl/(th * tw) * 1.2 # compensate for bends in the track
    ind = float(cfg['layer_stack'][layerid]['ind'])*tl
    cap = float(cfg['layer_stack'][layerid]['cap'])*tl
    fo = args.get("--fo", 1.0e-12)
    fo = 1.0e-12 if (fo == None) else float(fo)
    # compute track complex impedance from lumped elements T-model of the track
    zl = 1j* ind*1.0e-9 *2*3.1415*fo
    zc = 1/(1j* cap*1.0e-12 *2*3.1415*fo)
    zt = zl/2 + res/2 + (zc*(zl/2 + res/2) / (zc + zl/2 + res/2 ))
    pprint({
        "Resistance     [Ohm]: ": res,
        "Capacitance    [pF]:  ": cap,
        "Inductance     [nH]:  ": ind,
        "Delay          [ns]:  ": dt,
        "Z0             [Ohm]: ": zt,
        "|Z0|           [Ohm]: ": abs(zt),
    })
    if args.get("--iz", None) != None:
        iz = complex(args.get("--iz", None))
        reflect_coef = (zt-iz)/(zt + iz)
        print("Reflection Coefficient: ", abs(reflect_coef))

if __name__ == "__main__":
    main()