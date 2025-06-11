class autoGenerator:
    def __init__(self):
        self.main()
    def printNextSentence(self,name, n1,n2, n3, n4):
        r1 =round((float(1200/n1)),4)
        r2 = round((float(700/n2)),4)
        r3 = round((float(1200/n3)),4)
        r4 = round((float(700/n4)),4)
        codigo = "self.screen.blit(pygame.transform.scale("+name+", (self.width/"+str(r1)+", self.height/"+str(r2)+")), (self.width/"+str(r3)+", self.height/"+str(r4)+"))"
        print(codigo)
    def main(self):
        name = ""
        arr = [None,None,None,None]
        print("Name:")
        name = input()
        print("n1 n2 n3 n4:")
        inp = input()
        try:
            ar = inp.split(" ")
        
            for i in range(0,4):
                arr[i] = int(ar[i])
        except:
            print("bad arguments")
        self.printNextSentence(name,arr[0],arr[1],arr[2],arr[3])

generador = autoGenerator()
