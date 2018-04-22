# This class will hold the structure of 3 address code for the IR representation
class CodeObject:

    # Initializes a 3Address code list object, will be created at parent nodes(+ = *)
    # @param = codelist = send in all the code from the left hand side's children, then the right hand side.
    def __init__(self, codelist, resultLoc, type):
        self.ir_nodes = codelist    # this will hold IR nodes containing the 3AC code
        self.resultLoc = resultLoc  # this will hold the Temp or variable containing the result of the expression.
        self.type = type            # int or float

    def getCode(self):
        return self.ir_nodes

    def setCode(self, codelist):
        self.ir_nodes = codelist

    def getResultLoc(self):
        return self.resultLoc

    def setResultLoc(self, loc):
        self.resultLoc = loc


    # This should probably live in the IRGenerate class, it keeps track of the Temp #    
    def static_vars(**kwargs):
        def decorate(func):
            for k in kwargs:
                setattr(func, k, kwargs[k])
            return func
        return decorate

    @static_vars(counter=0)
    def getTemp():
        getTemp.counter += 1
        return "T" + getTemp.counter
        def getTmp(self):
            static