__all__ = ['SAPC_0_98G_4g_minimal']

# Don't look below, you will not understand this Python code :) I don't.
# translated from :
#   https://github.com/Myndex/SAPC-APCA/blob/master/JS/SAPC_0_98G_4g_minimal.js

from js2py.pyjs import *
import pudb

# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['deltaYmin', 'loBoWoffset', 'APCAcontrast', 'scaleWoB', 'loBoWfactor', 'sGco', 'sRco', 'sRGBtoY', 'loClip', 'blkClmp', 'blkThrs', 'scaleBoW', 'loBoWthresh', 'revBG', 'normBG', 'normTXT', 'sBco', 'revTXT', 'mainTRC'])
@Js
def PyJsHoisted_sRGBtoY_(sRGBcolor, this, arguments, var=var):
    var = Scope({'sRGBcolor':sRGBcolor, 'this':this, 'arguments':arguments}, var)
    var.registers(['b', 'r', 'simpleExp', 'g', 'sRGBcolor'])
    @Js
    def PyJsHoisted_simpleExp_(chan, this, arguments, var=var):
        var = Scope({'chan':chan, 'this':this, 'arguments':arguments}, var)
        var.registers(['chan'])
        return var.get('Math').callprop('pow', (var.get('chan')/Js(255.0)), var.get('mainTRC'))
    PyJsHoisted_simpleExp_.func_name = 'simpleExp'
    var.put('simpleExp', PyJsHoisted_simpleExp_)
    var.put('r', ((var.get('sRGBcolor')&Js(16711680))>>Js(16.0)))
    var.put('g', ((var.get('sRGBcolor')&Js(65280))>>Js(8.0)))
    var.put('b', (var.get('sRGBcolor')&Js(255)))
    pass
    return (((var.get('sRco')*var.get('simpleExp')(var.get('r')))+(var.get('sGco')*var.get('simpleExp')(var.get('g'))))+(var.get('sBco')*var.get('simpleExp')(var.get('b'))))
PyJsHoisted_sRGBtoY_.func_name = 'sRGBtoY'
var.put('sRGBtoY', PyJsHoisted_sRGBtoY_)
@Js
def PyJsHoisted_APCAcontrast_(txtY, bgY, this, arguments, var=var):
    var = Scope({'txtY':txtY, 'bgY':bgY, 'this':this, 'arguments':arguments}, var)
    var.registers(['SAPC', 'outputContrast', 'txtY', 'bgY'])
    var.put('SAPC', Js(0.0))
    var.put('outputContrast', Js(0.0))
    var.put('txtY', (var.get('txtY') if (var.get('txtY')>var.get('blkThrs')) else (var.get('txtY')+var.get('Math').callprop('pow', (var.get('blkThrs')-var.get('txtY')), var.get('blkClmp')))))
    var.put('bgY', (var.get('bgY') if (var.get('bgY')>var.get('blkThrs')) else (var.get('bgY')+var.get('Math').callprop('pow', (var.get('blkThrs')-var.get('bgY')), var.get('blkClmp')))))
    if (var.get('Math').callprop('abs', (var.get('bgY')-var.get('txtY')))<var.get('deltaYmin')):
        return Js(0.0)
    if (var.get('bgY')>var.get('txtY')):
        var.put('SAPC', ((var.get('Math').callprop('pow', var.get('bgY'), var.get('normBG'))-var.get('Math').callprop('pow', var.get('txtY'), var.get('normTXT')))*var.get('scaleBoW')))
        var.put('outputContrast', (Js(0.0) if (var.get('SAPC')<var.get('loClip')) else ((var.get('SAPC')-((var.get('SAPC')*var.get('loBoWfactor'))*var.get('loBoWoffset'))) if (var.get('SAPC')<var.get('loBoWthresh')) else (var.get('SAPC')-var.get('loBoWoffset')))))
    else:
        var.put('SAPC', ((var.get('Math').callprop('pow', var.get('bgY'), var.get('revBG'))-var.get('Math').callprop('pow', var.get('txtY'), var.get('revTXT')))*var.get('scaleWoB')))
        var.put('outputContrast', (Js(0.0) if (var.get('SAPC')>(-var.get('loClip'))) else ((var.get('SAPC')-((var.get('SAPC')*var.get('loWoBfactor'))*var.get('loWoBoffset'))) if (var.get('SAPC')>(-var.get('loWoBthresh'))) else (var.get('SAPC')+var.get('loWoBoffset')))))
    return (var.get('outputContrast')*Js(100.0))
PyJsHoisted_APCAcontrast_.func_name = 'APCAcontrast'
var.put('APCAcontrast', PyJsHoisted_APCAcontrast_)
var.put('mainTRC', Js(2.4))
var.put('sRco', Js(0.2126729))
var.put('sGco', Js(0.7151522))
var.put('sBco', Js(0.072175))
var.put('normBG', Js(0.56))
var.put('normTXT', Js(0.57))
var.put('revTXT', Js(0.62))
var.put('revBG', Js(0.65))
var.put('blkThrs', Js(0.022))
var.put('blkClmp', Js(1.414))
var.put('scaleBoW', Js(1.14))
var.put('scaleWoB', Js(1.14))
var.put('loBoWthresh', var.put('loWoBthresh', Js(0.035991)))
var.put('loBoWfactor', var.put('loWoBfactor', Js(27.7847239587675)))
var.put('loBoWoffset', var.put('loWoBoffset', Js(0.027)))
var.put('loClip', Js(0.001))
var.put('deltaYmin', Js(0.0005))
pass
pass
pass


# Add lib to the module scope
SAPC_0_98G_4g_minimal = var.to_python()
