from datetime import time, date, datetime, timedelta


def dias()->int:
    D1=date(1998,1,23) #nacimiento
    D2=date(2022,2,23) #Fecha del 23 de febrero del 2022
    delta=D2-D1
    print(delta.days)
    return delta.days

def bloque()->int:
    return (dias()%3)+1


print(bloque())