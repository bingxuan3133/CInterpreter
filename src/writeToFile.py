__author__ = 'JingWen'


class writeToFile:

    def __init__(self, byteCodeGenerator):
        self.byteCodeGenerator = byteCodeGenerator

    def writeAllToFile(self):
        tempList = self.byteCodeGenerator.byteCodeList

        file = open('myFirstByteCode', 'wb')
        for code in tempList:
            file.write(bytearray(code.to_bytes(4, "little")))
        file.flush()

        file.close()
        """
            file.write(bytes(0x03))

                """
