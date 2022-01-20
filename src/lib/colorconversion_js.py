__all__ = ['colorconversion_js']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['hex_to_rgb', 'okhsv_to_srgb', 'rgb_to_hsv', 'srgb_to_okhsl', 'get_ST_max', 'linear_srgb_to_oklab', 'hsv_to_rgb', 'get_Cs', 'okhsl_to_srgb', 'rgb_to_hex', 'oklab_to_linear_srgb', 'srgb_to_okhsv', 'find_gamut_intersection', 'compute_max_saturation', 'rgb_to_hsl', 'hsl_to_rgb', 'srgb_transfer_function', 'cbrt', 'toe_inv', 'toe', 'find_cusp', 'get_ST_mid', 'srgb_transfer_function_inv'])
@Js
def PyJsHoisted_cbrt_(x, this, arguments, var=var):
    var = Scope({'x':x, 'this':this, 'arguments':arguments}, var)
    var.registers(['x'])
    return var.get('Math').callprop('pow', var.get('x'), (Js(1.0)/Js(3.0)))
PyJsHoisted_cbrt_.func_name = 'cbrt'
var.put('cbrt', PyJsHoisted_cbrt_)
@Js
def PyJsHoisted_rgb_to_hsl_(r, g, b, this, arguments, var=var):
    var = Scope({'r':r, 'g':g, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['l', 'h', 'r', 'min', 'b', 'g', 'max', 'd', 's'])
    var.put('r', Js(255.0), '/')
    var.put('g', Js(255.0), '/')
    var.put('b', Js(255.0), '/')
    var.put('max', var.get('Math').callprop('max', var.get('r'), var.get('g'), var.get('b')))
    var.put('min', var.get('Math').callprop('min', var.get('r'), var.get('g'), var.get('b')))
    var.put('l', ((var.get('max')+var.get('min'))/Js(2.0)))
    if (var.get('max')==var.get('min')):
        var.put('h', var.put('s', Js(0.0)))
    else:
        var.put('d', (var.get('max')-var.get('min')))
        var.put('s', ((var.get('d')/((Js(2.0)-var.get('max'))-var.get('min'))) if (var.get('l')>Js(0.5)) else (var.get('d')/(var.get('max')+var.get('min')))))
        while 1:
            SWITCHED = False
            CONDITION = (var.get('max'))
            if SWITCHED or PyJsStrictEq(CONDITION, var.get('r')):
                SWITCHED = True
                var.put('h', (((var.get('g')-var.get('b'))/var.get('d'))+(Js(6.0) if (var.get('g')<var.get('b')) else Js(0.0))))
                break
            if SWITCHED or PyJsStrictEq(CONDITION, var.get('g')):
                SWITCHED = True
                var.put('h', (((var.get('b')-var.get('r'))/var.get('d'))+Js(2.0)))
                break
            if SWITCHED or PyJsStrictEq(CONDITION, var.get('b')):
                SWITCHED = True
                var.put('h', (((var.get('r')-var.get('g'))/var.get('d'))+Js(4.0)))
                break
            SWITCHED = True
            break
        var.put('h', Js(6.0), '/')
    return Js([var.get('h'), var.get('s'), var.get('l')])
PyJsHoisted_rgb_to_hsl_.func_name = 'rgb_to_hsl'
var.put('rgb_to_hsl', PyJsHoisted_rgb_to_hsl_)
@Js
def PyJsHoisted_hsl_to_rgb_(h, s, l, this, arguments, var=var):
    var = Scope({'h':h, 's':s, 'l':l, 'this':this, 'arguments':arguments}, var)
    var.registers(['l', 'r', 'h', 'b', 'hue_to_rgb', 'g', 'q', 'p', 's'])
    @Js
    def PyJsHoisted_hue_to_rgb_(p, q, t, this, arguments, var=var):
        var = Scope({'p':p, 'q':q, 't':t, 'this':this, 'arguments':arguments}, var)
        var.registers(['p', 't', 'q'])
        if (var.get('t')<Js(0.0)):
            var.put('t', Js(1.0), '+')
        if (var.get('t')>Js(1.0)):
            var.put('t', Js(1.0), '-')
        if (var.get('t')<(Js(1.0)/Js(6.0))):
            return (var.get('p')+(((var.get('q')-var.get('p'))*Js(6.0))*var.get('t')))
        if (var.get('t')<(Js(1.0)/Js(2.0))):
            return var.get('q')
        if (var.get('t')<(Js(2.0)/Js(3.0))):
            return (var.get('p')+(((var.get('q')-var.get('p'))*((Js(2.0)/Js(3.0))-var.get('t')))*Js(6.0)))
        return var.get('p')
    PyJsHoisted_hue_to_rgb_.func_name = 'hue_to_rgb'
    var.put('hue_to_rgb', PyJsHoisted_hue_to_rgb_)
    if (var.get('s')==Js(0.0)):
        var.put('r', var.put('g', var.put('b', var.get('l'))))
    else:
        var.put('q', ((var.get('l')*(Js(1.0)+var.get('s'))) if (var.get('l')<Js(0.5)) else ((var.get('l')+var.get('s'))-(var.get('l')*var.get('s')))))
        var.put('p', ((Js(2.0)*var.get('l'))-var.get('q')))
        var.put('r', var.get('hue_to_rgb')(var.get('p'), var.get('q'), (var.get('h')+(Js(1.0)/Js(3.0)))))
        var.put('g', var.get('hue_to_rgb')(var.get('p'), var.get('q'), var.get('h')))
        var.put('b', var.get('hue_to_rgb')(var.get('p'), var.get('q'), (var.get('h')-(Js(1.0)/Js(3.0)))))
    return Js([(var.get('r')*Js(255.0)), (var.get('g')*Js(255.0)), (var.get('b')*Js(255.0))])
PyJsHoisted_hsl_to_rgb_.func_name = 'hsl_to_rgb'
var.put('hsl_to_rgb', PyJsHoisted_hsl_to_rgb_)
@Js
def PyJsHoisted_rgb_to_hsv_(r, g, b, this, arguments, var=var):
    var = Scope({'r':r, 'g':g, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['h', 'r', 'min', 'b', 'v', 'g', 'max', 'd', 's'])
    PyJsComma(PyJsComma(var.put('r', (var.get('r')/Js(255.0))),var.put('g', (var.get('g')/Js(255.0)))),var.put('b', (var.get('b')/Js(255.0))))
    var.put('max', var.get('Math').callprop('max', var.get('r'), var.get('g'), var.get('b')))
    var.put('min', var.get('Math').callprop('min', var.get('r'), var.get('g'), var.get('b')))
    var.put('v', var.get('max'))
    var.put('d', (var.get('max')-var.get('min')))
    var.put('s', (Js(0.0) if (var.get('max')==Js(0.0)) else (var.get('d')/var.get('max'))))
    if (var.get('max')==var.get('min')):
        var.put('h', Js(0.0))
    else:
        while 1:
            SWITCHED = False
            CONDITION = (var.get('max'))
            if SWITCHED or PyJsStrictEq(CONDITION, var.get('r')):
                SWITCHED = True
                var.put('h', (((var.get('g')-var.get('b'))/var.get('d'))+(Js(6.0) if (var.get('g')<var.get('b')) else Js(0.0))))
                break
            if SWITCHED or PyJsStrictEq(CONDITION, var.get('g')):
                SWITCHED = True
                var.put('h', (((var.get('b')-var.get('r'))/var.get('d'))+Js(2.0)))
                break
            if SWITCHED or PyJsStrictEq(CONDITION, var.get('b')):
                SWITCHED = True
                var.put('h', (((var.get('r')-var.get('g'))/var.get('d'))+Js(4.0)))
                break
            SWITCHED = True
            break
        var.put('h', Js(6.0), '/')
    return Js([var.get('h'), var.get('s'), var.get('v')])
PyJsHoisted_rgb_to_hsv_.func_name = 'rgb_to_hsv'
var.put('rgb_to_hsv', PyJsHoisted_rgb_to_hsv_)
@Js
def PyJsHoisted_hsv_to_rgb_(h, s, v, this, arguments, var=var):
    var = Scope({'h':h, 's':s, 'v':v, 'this':this, 'arguments':arguments}, var)
    var.registers(['r', 'h', 'b', 'g', 'f', 'q', 't', 'i', 'p', 'v', 's'])
    var.put('i', var.get('Math').callprop('floor', (var.get('h')*Js(6.0))))
    var.put('f', ((var.get('h')*Js(6.0))-var.get('i')))
    var.put('p', (var.get('v')*(Js(1.0)-var.get('s'))))
    var.put('q', (var.get('v')*(Js(1.0)-(var.get('f')*var.get('s')))))
    var.put('t', (var.get('v')*(Js(1.0)-((Js(1.0)-var.get('f'))*var.get('s')))))
    while 1:
        SWITCHED = False
        CONDITION = ((var.get('i')%Js(6.0)))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(0.0)):
            SWITCHED = True
            var.put('r', var.get('v'))
            var.put('g', var.get('t'))
            var.put('b', var.get('p'))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, Js(1.0)):
            SWITCHED = True
            var.put('r', var.get('q'))
            var.put('g', var.get('v'))
            var.put('b', var.get('p'))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, Js(2.0)):
            SWITCHED = True
            var.put('r', var.get('p'))
            var.put('g', var.get('v'))
            var.put('b', var.get('t'))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, Js(3.0)):
            SWITCHED = True
            var.put('r', var.get('p'))
            var.put('g', var.get('q'))
            var.put('b', var.get('v'))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, Js(4.0)):
            SWITCHED = True
            var.put('r', var.get('t'))
            var.put('g', var.get('p'))
            var.put('b', var.get('v'))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, Js(5.0)):
            SWITCHED = True
            var.put('r', var.get('v'))
            var.put('g', var.get('p'))
            var.put('b', var.get('q'))
            break
        SWITCHED = True
        break
    return Js([(var.get('r')*Js(255.0)), (var.get('g')*Js(255.0)), (var.get('b')*Js(255.0))])
PyJsHoisted_hsv_to_rgb_.func_name = 'hsv_to_rgb'
var.put('hsv_to_rgb', PyJsHoisted_hsv_to_rgb_)
@Js
def PyJsHoisted_srgb_transfer_function_(a, this, arguments, var=var):
    var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
    var.registers(['a'])
    return ((Js(12.92)*var.get('a')) if (Js(0.0031308)>=var.get('a')) else ((Js(1.055)*var.get('Math').callprop('pow', var.get('a'), Js(0.4166666666666667)))-Js(0.055)))
PyJsHoisted_srgb_transfer_function_.func_name = 'srgb_transfer_function'
var.put('srgb_transfer_function', PyJsHoisted_srgb_transfer_function_)
@Js
def PyJsHoisted_srgb_transfer_function_inv_(a, this, arguments, var=var):
    var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
    var.registers(['a'])
    return (var.get('Math').callprop('pow', ((var.get('a')+Js(0.055))/Js(1.055)), Js(2.4)) if (Js(0.04045)<var.get('a')) else (var.get('a')/Js(12.92)))
PyJsHoisted_srgb_transfer_function_inv_.func_name = 'srgb_transfer_function_inv'
var.put('srgb_transfer_function_inv', PyJsHoisted_srgb_transfer_function_inv_)
@Js
def PyJsHoisted_linear_srgb_to_oklab_(r, g, b, this, arguments, var=var):
    var = Scope({'r':r, 'g':g, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['l', 'r', 's_', 'b', 'g', 'm_', 'l_', 'm', 's'])
    var.put('l', (((Js(0.4122214708)*var.get('r'))+(Js(0.5363325363)*var.get('g')))+(Js(0.0514459929)*var.get('b'))))
    var.put('m', (((Js(0.2119034982)*var.get('r'))+(Js(0.6806995451)*var.get('g')))+(Js(0.1073969566)*var.get('b'))))
    var.put('s', (((Js(0.0883024619)*var.get('r'))+(Js(0.2817188376)*var.get('g')))+(Js(0.6299787005)*var.get('b'))))
    var.put('l_', var.get('cbrt')(var.get('l')))
    var.put('m_', var.get('cbrt')(var.get('m')))
    var.put('s_', var.get('cbrt')(var.get('s')))
    return Js([(((Js(0.2104542553)*var.get('l_'))+(Js(0.793617785)*var.get('m_')))-(Js(0.0040720468)*var.get('s_'))), (((Js(1.9779984951)*var.get('l_'))-(Js(2.428592205)*var.get('m_')))+(Js(0.4505937099)*var.get('s_'))), (((Js(0.0259040371)*var.get('l_'))+(Js(0.7827717662)*var.get('m_')))-(Js(0.808675766)*var.get('s_')))])
PyJsHoisted_linear_srgb_to_oklab_.func_name = 'linear_srgb_to_oklab'
var.put('linear_srgb_to_oklab', PyJsHoisted_linear_srgb_to_oklab_)
@Js
def PyJsHoisted_oklab_to_linear_srgb_(L, a, b, this, arguments, var=var):
    var = Scope({'L':L, 'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['l', 's_', 'b', 'a', 's', 'L', 'l_', 'm', 'm_'])
    var.put('l_', ((var.get('L')+(Js(0.3963377774)*var.get('a')))+(Js(0.2158037573)*var.get('b'))))
    var.put('m_', ((var.get('L')-(Js(0.1055613458)*var.get('a')))-(Js(0.0638541728)*var.get('b'))))
    var.put('s_', ((var.get('L')-(Js(0.0894841775)*var.get('a')))-(Js(1.291485548)*var.get('b'))))
    var.put('l', ((var.get('l_')*var.get('l_'))*var.get('l_')))
    var.put('m', ((var.get('m_')*var.get('m_'))*var.get('m_')))
    var.put('s', ((var.get('s_')*var.get('s_'))*var.get('s_')))
    return Js([((((+Js(4.0767416621))*var.get('l'))-(Js(3.3077115913)*var.get('m')))+(Js(0.2309699292)*var.get('s'))), ((((-Js(1.2684380046))*var.get('l'))+(Js(2.6097574011)*var.get('m')))-(Js(0.3413193965)*var.get('s'))), ((((-Js(0.0041960863))*var.get('l'))-(Js(0.7034186147)*var.get('m')))+(Js(1.707614701)*var.get('s')))])
PyJsHoisted_oklab_to_linear_srgb_.func_name = 'oklab_to_linear_srgb'
var.put('oklab_to_linear_srgb', PyJsHoisted_oklab_to_linear_srgb_)
@Js
def PyJsHoisted_toe_(x, this, arguments, var=var):
    var = Scope({'x':x, 'this':this, 'arguments':arguments}, var)
    var.registers(['x', 'k_2', 'k_1', 'k_3'])
    var.put('k_1', Js(0.206))
    var.put('k_2', Js(0.03))
    var.put('k_3', ((Js(1.0)+var.get('k_1'))/(Js(1.0)+var.get('k_2'))))
    return (Js(0.5)*(((var.get('k_3')*var.get('x'))-var.get('k_1'))+var.get('Math').callprop('sqrt', ((((var.get('k_3')*var.get('x'))-var.get('k_1'))*((var.get('k_3')*var.get('x'))-var.get('k_1')))+(((Js(4.0)*var.get('k_2'))*var.get('k_3'))*var.get('x'))))))
PyJsHoisted_toe_.func_name = 'toe'
var.put('toe', PyJsHoisted_toe_)
@Js
def PyJsHoisted_toe_inv_(x, this, arguments, var=var):
    var = Scope({'x':x, 'this':this, 'arguments':arguments}, var)
    var.registers(['x', 'k_2', 'k_1', 'k_3'])
    var.put('k_1', Js(0.206))
    var.put('k_2', Js(0.03))
    var.put('k_3', ((Js(1.0)+var.get('k_1'))/(Js(1.0)+var.get('k_2'))))
    return (((var.get('x')*var.get('x'))+(var.get('k_1')*var.get('x')))/(var.get('k_3')*(var.get('x')+var.get('k_2'))))
PyJsHoisted_toe_inv_.func_name = 'toe_inv'
var.put('toe_inv', PyJsHoisted_toe_inv_)
@Js
def PyJsHoisted_compute_max_saturation_(a, b, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['k2', 'k0', 'l_dS', 'k3', 'S', 'wl', 'b', 'f', 'k4', 'k_m', 'm_dS2', 'f1', 's', 'k1', 'l', 'wm', 'k_s', 'k_l', 'm_dS', 'f2', 'l_dS2', 'ws', 'm_', 's_', 's_dS2', 's_dS', 'a', 'l_', 'm'])
    if ((((-Js(1.88170328))*var.get('a'))-(Js(0.80936493)*var.get('b')))>Js(1.0)):
        var.put('k0', (+Js(1.19086277)))
        var.put('k1', (+Js(1.76576728)))
        var.put('k2', (+Js(0.59662641)))
        var.put('k3', (+Js(0.75515197)))
        var.put('k4', (+Js(0.56771245)))
        var.put('wl', (+Js(4.0767416621)))
        var.put('wm', (-Js(3.3077115913)))
        var.put('ws', (+Js(0.2309699292)))
    else:
        if (((Js(1.81444104)*var.get('a'))-(Js(1.19445276)*var.get('b')))>Js(1.0)):
            var.put('k0', (+Js(0.73956515)))
            var.put('k1', (-Js(0.45954404)))
            var.put('k2', (+Js(0.08285427)))
            var.put('k3', (+Js(0.1254107)))
            var.put('k4', (+Js(0.14503204)))
            var.put('wl', (-Js(1.2684380046)))
            var.put('wm', (+Js(2.6097574011)))
            var.put('ws', (-Js(0.3413193965)))
        else:
            var.put('k0', (+Js(1.35733652)))
            var.put('k1', (-Js(0.00915799)))
            var.put('k2', (-Js(1.1513021)))
            var.put('k3', (-Js(0.50559606)))
            var.put('k4', (+Js(0.00692167)))
            var.put('wl', (-Js(0.0041960863)))
            var.put('wm', (-Js(0.7034186147)))
            var.put('ws', (+Js(1.707614701)))
    var.put('S', ((((var.get('k0')+(var.get('k1')*var.get('a')))+(var.get('k2')*var.get('b')))+((var.get('k3')*var.get('a'))*var.get('a')))+((var.get('k4')*var.get('a'))*var.get('b'))))
    var.put('k_l', (((+Js(0.3963377774))*var.get('a'))+(Js(0.2158037573)*var.get('b'))))
    var.put('k_m', (((-Js(0.1055613458))*var.get('a'))-(Js(0.0638541728)*var.get('b'))))
    var.put('k_s', (((-Js(0.0894841775))*var.get('a'))-(Js(1.291485548)*var.get('b'))))
    var.put('l_', (Js(1.0)+(var.get('S')*var.get('k_l'))))
    var.put('m_', (Js(1.0)+(var.get('S')*var.get('k_m'))))
    var.put('s_', (Js(1.0)+(var.get('S')*var.get('k_s'))))
    var.put('l', ((var.get('l_')*var.get('l_'))*var.get('l_')))
    var.put('m', ((var.get('m_')*var.get('m_'))*var.get('m_')))
    var.put('s', ((var.get('s_')*var.get('s_'))*var.get('s_')))
    var.put('l_dS', (((Js(3.0)*var.get('k_l'))*var.get('l_'))*var.get('l_')))
    var.put('m_dS', (((Js(3.0)*var.get('k_m'))*var.get('m_'))*var.get('m_')))
    var.put('s_dS', (((Js(3.0)*var.get('k_s'))*var.get('s_'))*var.get('s_')))
    var.put('l_dS2', (((Js(6.0)*var.get('k_l'))*var.get('k_l'))*var.get('l_')))
    var.put('m_dS2', (((Js(6.0)*var.get('k_m'))*var.get('k_m'))*var.get('m_')))
    var.put('s_dS2', (((Js(6.0)*var.get('k_s'))*var.get('k_s'))*var.get('s_')))
    var.put('f', (((var.get('wl')*var.get('l'))+(var.get('wm')*var.get('m')))+(var.get('ws')*var.get('s'))))
    var.put('f1', (((var.get('wl')*var.get('l_dS'))+(var.get('wm')*var.get('m_dS')))+(var.get('ws')*var.get('s_dS'))))
    var.put('f2', (((var.get('wl')*var.get('l_dS2'))+(var.get('wm')*var.get('m_dS2')))+(var.get('ws')*var.get('s_dS2'))))
    var.put('S', (var.get('S')-((var.get('f')*var.get('f1'))/((var.get('f1')*var.get('f1'))-((Js(0.5)*var.get('f'))*var.get('f2'))))))
    return var.get('S')
PyJsHoisted_compute_max_saturation_.func_name = 'compute_max_saturation'
var.put('compute_max_saturation', PyJsHoisted_compute_max_saturation_)
@Js
def PyJsHoisted_find_cusp_(a, b, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['b', 'rgb_at_max', 'a', 'S_cusp', 'C_cusp', 'L_cusp'])
    var.put('S_cusp', var.get('compute_max_saturation')(var.get('a'), var.get('b')))
    var.put('rgb_at_max', var.get('oklab_to_linear_srgb')(Js(1.0), (var.get('S_cusp')*var.get('a')), (var.get('S_cusp')*var.get('b'))))
    var.put('L_cusp', var.get('cbrt')((Js(1.0)/var.get('Math').callprop('max', var.get('Math').callprop('max', var.get('rgb_at_max').get('0'), var.get('rgb_at_max').get('1')), var.get('rgb_at_max').get('2')))))
    var.put('C_cusp', (var.get('L_cusp')*var.get('S_cusp')))
    return Js([var.get('L_cusp'), var.get('C_cusp')])
PyJsHoisted_find_cusp_.func_name = 'find_cusp'
var.put('find_cusp', PyJsHoisted_find_cusp_)
@Js
def PyJsHoisted_find_gamut_intersection_(a, b, L1, C1, L0, cusp, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'L1':L1, 'C1':C1, 'L0':L0, 'cusp':cusp, 'this':this, 'arguments':arguments}, var)
    var.registers(['C1', 'mdt2', 'g', 'b1', 'r2', 'dL', 'g1', 'm_dt', 'u_g', 'u_b', 'b', 'L0', 's_dt', 'mdt', 'C', 'k_m', 'g2', 'dC', 's', 'l', 't_g', 'l_dt', 'k_s', 'k_l', 'sdt', 't', 't_r', 'L1', 'b2', 'm_', 't_b', 'r', 's_', 'r1', 'u_r', 'sdt2', 'a', 'cusp', 'L', 'l_', 'm', 'ldt2', 'ldt'])
    if var.get('cusp').neg():
        var.put('cusp', var.get('find_cusp')(var.get('a'), var.get('b')))
    if ((((var.get('L1')-var.get('L0'))*var.get('cusp').get('1'))-((var.get('cusp').get('0')-var.get('L0'))*var.get('C1')))<=Js(0.0)):
        var.put('t', ((var.get('cusp').get('1')*var.get('L0'))/((var.get('C1')*var.get('cusp').get('0'))+(var.get('cusp').get('1')*(var.get('L0')-var.get('L1'))))))
    else:
        var.put('t', ((var.get('cusp').get('1')*(var.get('L0')-Js(1.0)))/((var.get('C1')*(var.get('cusp').get('0')-Js(1.0)))+(var.get('cusp').get('1')*(var.get('L0')-var.get('L1'))))))
        var.put('dL', (var.get('L1')-var.get('L0')))
        var.put('dC', var.get('C1'))
        var.put('k_l', (((+Js(0.3963377774))*var.get('a'))+(Js(0.2158037573)*var.get('b'))))
        var.put('k_m', (((-Js(0.1055613458))*var.get('a'))-(Js(0.0638541728)*var.get('b'))))
        var.put('k_s', (((-Js(0.0894841775))*var.get('a'))-(Js(1.291485548)*var.get('b'))))
        var.put('l_dt', (var.get('dL')+(var.get('dC')*var.get('k_l'))))
        var.put('m_dt', (var.get('dL')+(var.get('dC')*var.get('k_m'))))
        var.put('s_dt', (var.get('dL')+(var.get('dC')*var.get('k_s'))))
        var.put('L', ((var.get('L0')*(Js(1.0)-var.get('t')))+(var.get('t')*var.get('L1'))))
        var.put('C', (var.get('t')*var.get('C1')))
        var.put('l_', (var.get('L')+(var.get('C')*var.get('k_l'))))
        var.put('m_', (var.get('L')+(var.get('C')*var.get('k_m'))))
        var.put('s_', (var.get('L')+(var.get('C')*var.get('k_s'))))
        var.put('l', ((var.get('l_')*var.get('l_'))*var.get('l_')))
        var.put('m', ((var.get('m_')*var.get('m_'))*var.get('m_')))
        var.put('s', ((var.get('s_')*var.get('s_'))*var.get('s_')))
        var.put('ldt', (((Js(3.0)*var.get('l_dt'))*var.get('l_'))*var.get('l_')))
        var.put('mdt', (((Js(3.0)*var.get('m_dt'))*var.get('m_'))*var.get('m_')))
        var.put('sdt', (((Js(3.0)*var.get('s_dt'))*var.get('s_'))*var.get('s_')))
        var.put('ldt2', (((Js(6.0)*var.get('l_dt'))*var.get('l_dt'))*var.get('l_')))
        var.put('mdt2', (((Js(6.0)*var.get('m_dt'))*var.get('m_dt'))*var.get('m_')))
        var.put('sdt2', (((Js(6.0)*var.get('s_dt'))*var.get('s_dt'))*var.get('s_')))
        var.put('r', ((((Js(4.0767416621)*var.get('l'))-(Js(3.3077115913)*var.get('m')))+(Js(0.2309699292)*var.get('s')))-Js(1.0)))
        var.put('r1', (((Js(4.0767416621)*var.get('ldt'))-(Js(3.3077115913)*var.get('mdt')))+(Js(0.2309699292)*var.get('sdt'))))
        var.put('r2', (((Js(4.0767416621)*var.get('ldt2'))-(Js(3.3077115913)*var.get('mdt2')))+(Js(0.2309699292)*var.get('sdt2'))))
        var.put('u_r', (var.get('r1')/((var.get('r1')*var.get('r1'))-((Js(0.5)*var.get('r'))*var.get('r2')))))
        var.put('t_r', ((-var.get('r'))*var.get('u_r')))
        var.put('g', (((((-Js(1.2684380046))*var.get('l'))+(Js(2.6097574011)*var.get('m')))-(Js(0.3413193965)*var.get('s')))-Js(1.0)))
        var.put('g1', ((((-Js(1.2684380046))*var.get('ldt'))+(Js(2.6097574011)*var.get('mdt')))-(Js(0.3413193965)*var.get('sdt'))))
        var.put('g2', ((((-Js(1.2684380046))*var.get('ldt2'))+(Js(2.6097574011)*var.get('mdt2')))-(Js(0.3413193965)*var.get('sdt2'))))
        var.put('u_g', (var.get('g1')/((var.get('g1')*var.get('g1'))-((Js(0.5)*var.get('g'))*var.get('g2')))))
        var.put('t_g', ((-var.get('g'))*var.get('u_g')))
        var.put('b', (((((-Js(0.0041960863))*var.get('l'))-(Js(0.7034186147)*var.get('m')))+(Js(1.707614701)*var.get('s')))-Js(1.0)))
        var.put('b1', ((((-Js(0.0041960863))*var.get('ldt'))-(Js(0.7034186147)*var.get('mdt')))+(Js(1.707614701)*var.get('sdt'))))
        var.put('b2', ((((-Js(0.0041960863))*var.get('ldt2'))-(Js(0.7034186147)*var.get('mdt2')))+(Js(1.707614701)*var.get('sdt2'))))
        var.put('u_b', (var.get('b1')/((var.get('b1')*var.get('b1'))-((Js(0.5)*var.get('b'))*var.get('b2')))))
        var.put('t_b', ((-var.get('b'))*var.get('u_b')))
        var.put('t_r', (var.get('t_r') if (var.get('u_r')>=Js(0.0)) else Js(1000000.0)))
        var.put('t_g', (var.get('t_g') if (var.get('u_g')>=Js(0.0)) else Js(1000000.0)))
        var.put('t_b', (var.get('t_b') if (var.get('u_b')>=Js(0.0)) else Js(1000000.0)))
        var.put('t', var.get('Math').callprop('min', var.get('t_r'), var.get('Math').callprop('min', var.get('t_g'), var.get('t_b'))), '+')
    return var.get('t')
PyJsHoisted_find_gamut_intersection_.func_name = 'find_gamut_intersection'
var.put('find_gamut_intersection', PyJsHoisted_find_gamut_intersection_)
@Js
def PyJsHoisted_get_ST_max_(a_, b_, cusp, this, arguments, var=var):
    var = Scope({'a_':a_, 'b_':b_, 'cusp':cusp, 'this':this, 'arguments':arguments}, var)
    var.registers(['cusp', 'L', 'b_', 'C', 'a_'])
    if var.get('cusp').neg():
        var.put('cusp', var.get('find_cusp')(var.get('a_'), var.get('b_')))
    var.put('L', var.get('cusp').get('0'))
    var.put('C', var.get('cusp').get('1'))
    return Js([(var.get('C')/var.get('L')), (var.get('C')/(Js(1.0)-var.get('L')))])
PyJsHoisted_get_ST_max_.func_name = 'get_ST_max'
var.put('get_ST_max', PyJsHoisted_get_ST_max_)
@Js
def PyJsHoisted_get_ST_mid_(a_, b_, this, arguments, var=var):
    var = Scope({'a_':a_, 'b_':b_, 'this':this, 'arguments':arguments}, var)
    var.registers(['b_', 'a_'])
    var.put('S', (Js(0.11516993)+(Js(1.0)/(((+Js(7.4477897))+(Js(4.1590124)*var.get('b_')))+(var.get('a_')*(((-Js(2.19557347))+(Js(1.75198401)*var.get('b_')))+(var.get('a_')*(((-Js(2.13704948))-(Js(10.02301043)*var.get('b_')))+(var.get('a_')*(((-Js(4.24894561))+(Js(5.38770819)*var.get('b_')))+(Js(4.69891013)*var.get('a_'))))))))))))
    var.put('T', (Js(0.11239642)+(Js(1.0)/(((+Js(1.6132032))-(Js(0.68124379)*var.get('b_')))+(var.get('a_')*(((+Js(0.40370612))+(Js(0.90148123)*var.get('b_')))+(var.get('a_')*(((-Js(0.27087943))+(Js(0.6122399)*var.get('b_')))+(var.get('a_')*(((+Js(0.00299215))-(Js(0.45399568)*var.get('b_')))-(Js(0.14661872)*var.get('a_'))))))))))))
    return Js([var.get('S'), var.get('T')])
PyJsHoisted_get_ST_mid_.func_name = 'get_ST_mid'
var.put('get_ST_mid', PyJsHoisted_get_ST_mid_)
@Js
def PyJsHoisted_get_Cs_(L, a_, b_, this, arguments, var=var):
    var = Scope({'L':L, 'a_':a_, 'b_':b_, 'this':this, 'arguments':arguments}, var)
    var.registers(['T_mid', 'S_mid', 'C_b', 'C_max', 'C_0', 'L', 'b_', 'k', 'ST_max', 'C_mid', 'a_', 'C_a'])
    var.put('cusp', var.get('find_cusp')(var.get('a_'), var.get('b_')))
    var.put('C_max', var.get('find_gamut_intersection')(var.get('a_'), var.get('b_'), var.get('L'), Js(1.0), var.get('L'), var.get('cusp')))
    var.put('ST_max', var.get('get_ST_max')(var.get('a_'), var.get('b_'), var.get('cusp')))
    var.put('S_mid', (Js(0.11516993)+(Js(1.0)/(((+Js(7.4477897))+(Js(4.1590124)*var.get('b_')))+(var.get('a_')*(((-Js(2.19557347))+(Js(1.75198401)*var.get('b_')))+(var.get('a_')*(((-Js(2.13704948))-(Js(10.02301043)*var.get('b_')))+(var.get('a_')*(((-Js(4.24894561))+(Js(5.38770819)*var.get('b_')))+(Js(4.69891013)*var.get('a_'))))))))))))
    var.put('T_mid', (Js(0.11239642)+(Js(1.0)/(((+Js(1.6132032))-(Js(0.68124379)*var.get('b_')))+(var.get('a_')*(((+Js(0.40370612))+(Js(0.90148123)*var.get('b_')))+(var.get('a_')*(((-Js(0.27087943))+(Js(0.6122399)*var.get('b_')))+(var.get('a_')*(((+Js(0.00299215))-(Js(0.45399568)*var.get('b_')))-(Js(0.14661872)*var.get('a_'))))))))))))
    var.put('k', (var.get('C_max')/var.get('Math').callprop('min', (var.get('L')*var.get('ST_max').get('0')), ((Js(1.0)-var.get('L'))*var.get('ST_max').get('1')))))
    var.put('C_a', (var.get('L')*var.get('S_mid')))
    var.put('C_b', ((Js(1.0)-var.get('L'))*var.get('T_mid')))
    var.put('C_mid', ((Js(0.9)*var.get('k'))*var.get('Math').callprop('sqrt', var.get('Math').callprop('sqrt', (Js(1.0)/((Js(1.0)/(((var.get('C_a')*var.get('C_a'))*var.get('C_a'))*var.get('C_a')))+(Js(1.0)/(((var.get('C_b')*var.get('C_b'))*var.get('C_b'))*var.get('C_b')))))))))
    var.put('C_a', (var.get('L')*Js(0.4)))
    var.put('C_b', ((Js(1.0)-var.get('L'))*Js(0.8)))
    var.put('C_0', var.get('Math').callprop('sqrt', (Js(1.0)/((Js(1.0)/(var.get('C_a')*var.get('C_a')))+(Js(1.0)/(var.get('C_b')*var.get('C_b')))))))
    return Js([var.get('C_0'), var.get('C_mid'), var.get('C_max')])
PyJsHoisted_get_Cs_.func_name = 'get_Cs'
var.put('get_Cs', PyJsHoisted_get_Cs_)
@Js
def PyJsHoisted_okhsl_to_srgb_(h, s, l, this, arguments, var=var):
    var = Scope({'h':h, 's':s, 'l':l, 'this':this, 'arguments':arguments}, var)
    var.registers(['l', 'k_2', 'h', 'k_0', 'C_max', 't', 'C_0', 'L', 'b_', 'C', 'Cs', 'rgb', 'C_mid', 'a_', 's', 'k_1'])
    if (var.get('l')==Js(1.0)):
        return Js([Js(255.0), Js(255.0), Js(255.0)])
    else:
        if (var.get('l')==Js(0.0)):
            return Js([Js(0.0), Js(0.0), Js(0.0)])
    var.put('a_', var.get('Math').callprop('cos', ((Js(2.0)*var.get('Math').get('PI'))*var.get('h'))))
    var.put('b_', var.get('Math').callprop('sin', ((Js(2.0)*var.get('Math').get('PI'))*var.get('h'))))
    var.put('L', var.get('toe_inv')(var.get('l')))
    var.put('Cs', var.get('get_Cs')(var.get('L'), var.get('a_'), var.get('b_')))
    var.put('C_0', var.get('Cs').get('0'))
    var.put('C_mid', var.get('Cs').get('1'))
    var.put('C_max', var.get('Cs').get('2'))
    if (var.get('s')<Js(0.8)):
        var.put('t', (Js(1.25)*var.get('s')))
        var.put('k_0', Js(0.0))
        var.put('k_1', (Js(0.8)*var.get('C_0')))
        var.put('k_2', (Js(1.0)-(var.get('k_1')/var.get('C_mid'))))
    else:
        var.put('t', (Js(5.0)*(var.get('s')-Js(0.8))))
        var.put('k_0', var.get('C_mid'))
        var.put('k_1', (((((Js(0.2)*var.get('C_mid'))*var.get('C_mid'))*Js(1.25))*Js(1.25))/var.get('C_0')))
        var.put('k_2', (Js(1.0)-(var.get('k_1')/(var.get('C_max')-var.get('C_mid')))))
    var.put('C', (var.get('k_0')+((var.get('t')*var.get('k_1'))/(Js(1.0)-(var.get('k_2')*var.get('t'))))))
    var.put('rgb', var.get('oklab_to_linear_srgb')(var.get('L'), (var.get('C')*var.get('a_')), (var.get('C')*var.get('b_'))))
    return Js([(Js(255.0)*var.get('srgb_transfer_function')(var.get('rgb').get('0'))), (Js(255.0)*var.get('srgb_transfer_function')(var.get('rgb').get('1'))), (Js(255.0)*var.get('srgb_transfer_function')(var.get('rgb').get('2')))])
PyJsHoisted_okhsl_to_srgb_.func_name = 'okhsl_to_srgb'
var.put('okhsl_to_srgb', PyJsHoisted_okhsl_to_srgb_)
@Js
def PyJsHoisted_srgb_to_okhsl_(r, g, b, this, arguments, var=var):
    var = Scope({'r':r, 'g':g, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['k_0', 'g', 'k_2', 'h', 'b', 'b_', 'C', 'Cs', 'C_mid', 's', 'l', 'C_max', 'lab', 'C_0', 't', 'r', 'L', 'a_', 'k_1'])
    var.put('lab', var.get('linear_srgb_to_oklab')(var.get('srgb_transfer_function_inv')((var.get('r')/Js(255.0))), var.get('srgb_transfer_function_inv')((var.get('g')/Js(255.0))), var.get('srgb_transfer_function_inv')((var.get('b')/Js(255.0)))))
    var.put('C', var.get('Math').callprop('sqrt', ((var.get('lab').get('1')*var.get('lab').get('1'))+(var.get('lab').get('2')*var.get('lab').get('2')))))
    var.put('a_', (var.get('lab').get('1')/var.get('C')))
    var.put('b_', (var.get('lab').get('2')/var.get('C')))
    var.put('L', var.get('lab').get('0'))
    var.put('h', (Js(0.5)+((Js(0.5)*var.get('Math').callprop('atan2', (-var.get('lab').get('2')), (-var.get('lab').get('1'))))/var.get('Math').get('PI'))))
    var.put('Cs', var.get('get_Cs')(var.get('L'), var.get('a_'), var.get('b_')))
    var.put('C_0', var.get('Cs').get('0'))
    var.put('C_mid', var.get('Cs').get('1'))
    var.put('C_max', var.get('Cs').get('2'))
    if (var.get('C')<var.get('C_mid')):
        var.put('k_0', Js(0.0))
        var.put('k_1', (Js(0.8)*var.get('C_0')))
        var.put('k_2', (Js(1.0)-(var.get('k_1')/var.get('C_mid'))))
        var.put('t', ((var.get('C')-var.get('k_0'))/(var.get('k_1')+(var.get('k_2')*(var.get('C')-var.get('k_0'))))))
        var.put('s', (var.get('t')*Js(0.8)))
    else:
        var.put('k_0', var.get('C_mid'))
        var.put('k_1', (((((Js(0.2)*var.get('C_mid'))*var.get('C_mid'))*Js(1.25))*Js(1.25))/var.get('C_0')))
        var.put('k_2', (Js(1.0)-(var.get('k_1')/(var.get('C_max')-var.get('C_mid')))))
        var.put('t', ((var.get('C')-var.get('k_0'))/(var.get('k_1')+(var.get('k_2')*(var.get('C')-var.get('k_0'))))))
        var.put('s', (Js(0.8)+(Js(0.2)*var.get('t'))))
    var.put('l', var.get('toe')(var.get('L')))
    return Js([var.get('h'), var.get('s'), var.get('l')])
PyJsHoisted_srgb_to_okhsl_.func_name = 'srgb_to_okhsl'
var.put('srgb_to_okhsl', PyJsHoisted_srgb_to_okhsl_)
@Js
def PyJsHoisted_okhsv_to_srgb_(h, s, v, this, arguments, var=var):
    var = Scope({'h':h, 's':s, 'v':v, 'this':this, 'arguments':arguments}, var)
    var.registers(['C_vt', 'L_v', 'C_v', 'L_new', 'rgb_scale', 'h', 'S_max', 'v', 'b_', 'C', 's', 'T', 'L_vt', 'k', 'ST_max', 'scale_L', 'S_0', 'cusp', 'L', 'rgb', 'a_'])
    var.put('a_', var.get('Math').callprop('cos', ((Js(2.0)*var.get('Math').get('PI'))*var.get('h'))))
    var.put('b_', var.get('Math').callprop('sin', ((Js(2.0)*var.get('Math').get('PI'))*var.get('h'))))
    var.put('cusp', var.get(u"null"))
    var.put('ST_max', var.get('get_ST_max')(var.get('a_'), var.get('b_'), var.get('cusp')))
    var.put('S_max', var.get('ST_max').get('0'))
    var.put('S_0', Js(0.5))
    var.put('T', var.get('ST_max').get('1'))
    var.put('k', (Js(1.0)-(var.get('S_0')/var.get('S_max'))))
    var.put('L_v', (Js(1.0)-((var.get('s')*var.get('S_0'))/((var.get('S_0')+var.get('T'))-((var.get('T')*var.get('k'))*var.get('s'))))))
    var.put('C_v', (((var.get('s')*var.get('T'))*var.get('S_0'))/((var.get('S_0')+var.get('T'))-((var.get('T')*var.get('k'))*var.get('s')))))
    var.put('L', (var.get('v')*var.get('L_v')))
    var.put('C', (var.get('v')*var.get('C_v')))
    var.put('L_vt', var.get('toe_inv')(var.get('L_v')))
    var.put('C_vt', ((var.get('C_v')*var.get('L_vt'))/var.get('L_v')))
    var.put('L_new', var.get('toe_inv')(var.get('L')))
    var.put('C', ((var.get('C')*var.get('L_new'))/var.get('L')))
    var.put('L', var.get('L_new'))
    var.put('rgb_scale', var.get('oklab_to_linear_srgb')(var.get('L_vt'), (var.get('a_')*var.get('C_vt')), (var.get('b_')*var.get('C_vt'))))
    var.put('scale_L', var.get('cbrt')((Js(1.0)/var.get('Math').callprop('max', var.get('rgb_scale').get('0'), var.get('rgb_scale').get('1'), var.get('rgb_scale').get('2'), Js(0.0)))))
    var.put('L', (var.get('L')*var.get('scale_L')))
    var.put('C', (var.get('C')*var.get('scale_L')))
    var.put('rgb', var.get('oklab_to_linear_srgb')(var.get('L'), (var.get('C')*var.get('a_')), (var.get('C')*var.get('b_'))))
    return Js([(Js(255.0)*var.get('srgb_transfer_function')(var.get('rgb').get('0'))), (Js(255.0)*var.get('srgb_transfer_function')(var.get('rgb').get('1'))), (Js(255.0)*var.get('srgb_transfer_function')(var.get('rgb').get('2')))])
PyJsHoisted_okhsv_to_srgb_.func_name = 'okhsv_to_srgb'
var.put('okhsv_to_srgb', PyJsHoisted_okhsv_to_srgb_)
@Js
def PyJsHoisted_srgb_to_okhsv_(r, g, b, this, arguments, var=var):
    var = Scope({'r':r, 'g':g, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['h', 'T', 'r', 'S_0', 'b', 'cusp', 'lab', 'S_max', 'g', 'L', 'b_', 'L_v', 'k', 'C', 'C_v', 'ST_max', 'a_'])
    var.put('lab', var.get('linear_srgb_to_oklab')(var.get('srgb_transfer_function_inv')((var.get('r')/Js(255.0))), var.get('srgb_transfer_function_inv')((var.get('g')/Js(255.0))), var.get('srgb_transfer_function_inv')((var.get('b')/Js(255.0)))))
    var.put('C', var.get('Math').callprop('sqrt', ((var.get('lab').get('1')*var.get('lab').get('1'))+(var.get('lab').get('2')*var.get('lab').get('2')))))
    var.put('a_', (var.get('lab').get('1')/var.get('C')))
    var.put('b_', (var.get('lab').get('2')/var.get('C')))
    var.put('L', var.get('lab').get('0'))
    var.put('h', (Js(0.5)+((Js(0.5)*var.get('Math').callprop('atan2', (-var.get('lab').get('2')), (-var.get('lab').get('1'))))/var.get('Math').get('PI'))))
    var.put('cusp', var.get(u"null"))
    var.put('ST_max', var.get('get_ST_max')(var.get('a_'), var.get('b_'), var.get('cusp')))
    var.put('S_max', var.get('ST_max').get('0'))
    var.put('S_0', Js(0.5))
    var.put('T', var.get('ST_max').get('1'))
    var.put('k', (Js(1.0)-(var.get('S_0')/var.get('S_max'))))
    var.put('t', (var.get('T')/(var.get('C')+(var.get('L')*var.get('T')))))
    var.put('L_v', (var.get('t')*var.get('L')))
    var.put('C_v', (var.get('t')*var.get('C')))
    var.put('L_vt', var.get('toe_inv')(var.get('L_v')))
    var.put('C_vt', ((var.get('C_v')*var.get('L_vt'))/var.get('L_v')))
    var.put('rgb_scale', var.get('oklab_to_linear_srgb')(var.get('L_vt'), (var.get('a_')*var.get('C_vt')), (var.get('b_')*var.get('C_vt'))))
    var.put('scale_L', var.get('cbrt')((Js(1.0)/var.get('Math').callprop('max', var.get('rgb_scale').get('0'), var.get('rgb_scale').get('1'), var.get('rgb_scale').get('2'), Js(0.0)))))
    var.put('L', (var.get('L')/var.get('scale_L')))
    var.put('C', (var.get('C')/var.get('scale_L')))
    var.put('C', ((var.get('C')*var.get('toe')(var.get('L')))/var.get('L')))
    var.put('L', var.get('toe')(var.get('L')))
    var.put('v', (var.get('L')/var.get('L_v')))
    var.put('s', (((var.get('S_0')+var.get('T'))*var.get('C_v'))/((var.get('T')*var.get('S_0'))+((var.get('T')*var.get('k'))*var.get('C_v')))))
    return Js([var.get('h'), var.get('s'), var.get('v')])
PyJsHoisted_srgb_to_okhsv_.func_name = 'srgb_to_okhsv'
var.put('srgb_to_okhsv', PyJsHoisted_srgb_to_okhsv_)
@Js
def PyJsHoisted_hex_to_rgb_(hex, this, arguments, var=var):
    var = Scope({'hex':hex, 'this':this, 'arguments':arguments}, var)
    var.registers(['r', 'hex', 'b', 'a', 'g'])
    if (var.get('hex').callprop('substr', Js(0.0), Js(1.0))==Js('#')):
        var.put('hex', var.get('hex').callprop('substr', Js(1.0)))
    if var.get('hex').callprop('match', JsRegExp('/^([0-9a-f]{3})$/i')):
        var.put('r', ((var.get('parseInt')(var.get('hex').callprop('charAt', Js(0.0)), Js(16.0))/Js(15.0))*Js(255.0)))
        var.put('g', ((var.get('parseInt')(var.get('hex').callprop('charAt', Js(1.0)), Js(16.0))/Js(15.0))*Js(255.0)))
        var.put('b', ((var.get('parseInt')(var.get('hex').callprop('charAt', Js(2.0)), Js(16.0))/Js(15.0))*Js(255.0)))
        return Js([var.get('r'), var.get('g'), var.get('b')])
    if var.get('hex').callprop('match', JsRegExp('/^([0-9a-f]{6})$/i')):
        var.put('r', var.get('parseInt')(var.get('hex').callprop('substr', Js(0.0), Js(2.0)), Js(16.0)))
        var.put('g', var.get('parseInt')(var.get('hex').callprop('substr', Js(2.0), Js(2.0)), Js(16.0)))
        var.put('b', var.get('parseInt')(var.get('hex').callprop('substr', Js(4.0), Js(2.0)), Js(16.0)))
        return Js([var.get('r'), var.get('g'), var.get('b')])
    if var.get('hex').callprop('match', JsRegExp('/^([0-9a-f]{1})$/i')):
        var.put('a', ((var.get('parseInt')(var.get('hex').callprop('substr', Js(0.0)), Js(16.0))/Js(15.0))*Js(255.0)))
        return Js([var.get('a'), var.get('a'), var.get('a')])
    if var.get('hex').callprop('match', JsRegExp('/^([0-9a-f]{2})$/i')):
        var.put('a', var.get('parseInt')(var.get('hex').callprop('substr', Js(0.0), Js(2.0)), Js(16.0)))
        return Js([var.get('a'), var.get('a'), var.get('a')])
    return var.get(u"null")
PyJsHoisted_hex_to_rgb_.func_name = 'hex_to_rgb'
var.put('hex_to_rgb', PyJsHoisted_hex_to_rgb_)
@Js
def PyJsHoisted_rgb_to_hex_(r, g, b, this, arguments, var=var):
    var = Scope({'r':r, 'g':g, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['b', 'r', 'componentToHex', 'g'])
    @Js
    def PyJsHoisted_componentToHex_(x, this, arguments, var=var):
        var = Scope({'x':x, 'this':this, 'arguments':arguments}, var)
        var.registers(['x', 'hex'])
        var.put('hex', var.get('Math').callprop('round', var.get('x')).callprop('toString', Js(16.0)))
        return ((Js('0')+var.get('hex')) if (var.get('hex').get('length')==Js(1.0)) else var.get('hex'))
    PyJsHoisted_componentToHex_.func_name = 'componentToHex'
    var.put('componentToHex', PyJsHoisted_componentToHex_)
    return (((Js('#')+var.get('componentToHex')(var.get('r')))+var.get('componentToHex')(var.get('g')))+var.get('componentToHex')(var.get('b')))
PyJsHoisted_rgb_to_hex_.func_name = 'rgb_to_hex'
var.put('rgb_to_hex', PyJsHoisted_rgb_to_hex_)


# Add lib to the module scope
colorconversion_js = var.to_python()