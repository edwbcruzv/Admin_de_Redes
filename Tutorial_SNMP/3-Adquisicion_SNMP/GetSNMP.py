from pysnmp.hlapi import *


def consultaSNMP(comunidad,host,oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        # hace la solicitud getsnmp
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, 161)), # udp
               ContextData(),
               ObjectType(ObjectIdentity(oid)))) 

    # tratamiento de errores
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado= varB.split()[2] # se agarra la ultima parte de la consulta
    return resultado