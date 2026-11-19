"""Compact display only; never rounds source data before finding winners."""
def sci(value):
    value=float(value)
    if value==0:return '0'
    mantissa,exponent=f'{value:.3e}'.split('e')
    return f'{mantissa.rstrip("0").rstrip(".")}e{int(exponent)}'
