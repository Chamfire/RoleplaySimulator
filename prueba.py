class prueba:   
    def __init__(self):
        self.code = None 
    def isNumber(self, n):
            if (ord(n)>=48 and ord(n)<=57):
                return True
            else:
                return False
        
    def isProperFormat(self,code,it): #comprueba el formato 111.111.111:[49152-65535] -> puede haber de 1 a 3 números en la ip
        if((code != None or it>0)and it<=2): #si es 3, entonces estamos ya donde el puerto
            if(self.isNumber(code[0]) and ord(self.code[0]) != 48):
                if(len(code)>=2 and self.isNumber(code[1])):
                    if(len(code)>=3 and self.isNumber(code[2])):
                        if((it < 2 and (len(code)>=4 and code[3] == '.')) or (it == 2 and code[3] == ':')):
                            if(len(code)>=5):
                                code = code[4:]
                                return self.isProperFormat(code,it+1)
                            else:
                                return (False,None)
                        else:
                            return (False,None)
                    elif((it < 2 and (len(code)>=3 and code[2] == '.')) or (it == 2 and code[2] == ':')):
                        if(len(code)>=4):
                            code = code[3:]
                            return self.isProperFormat(code,it+1)
                        else:
                            return (False,None)
                    else:
                        return (False,None)
                elif((it < 2 and (len(code)>=2 and code[1] == '.')) or (it == 2 and code[1] == ':')):
                    if(len(code)>=3):
                        code = code[2:]
                        return self.isProperFormat(code,it+1)
                    else:
                        return (False,None)
                else:
                    return (False,None)
            else:
                return (False,None)
        elif(it != 3):
            return (False,None)
        else: #estamos donde el puerto
            if(len(code) == 5):
                for i in range(0,5):
                    if(self.isNumber(code[i])):
                        pass
                    else:
                        return (False,None)
                n = int(code)
                if(n>=49152 and n <=65535):
                    (ip,port) = self.code.split(':')
                    return (True,(ip,port))
            else:
                return (False,None)
            
prueb = prueba()
print(prueb.isNumber('4'))
prueb.code = "11.193.15:13567"
print(prueb.isProperFormat("11.193.15:13567",0))
prueb.code = "97.212.4:62123"
print(prueb.isProperFormat("97.212.4:62123",0))
prueb.code = "097.212.4:62123"
print(prueb.isProperFormat("097.212.4:62123",0))