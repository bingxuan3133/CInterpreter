__author__ = 'Jing'


def generateErrorMessageWithNoArguement( ErrorMessage, ErrorToken):
        caretMessage = ' '*(ErrorToken.column-1)+'^'
        errorLabelWithLocation="Error[{}][{}]".format(ErrorToken.line,ErrorToken.column)
        firstLineError=errorLabelWithLocation+':'+ErrorMessage
        ErrorMessageWithInformation = firstLineError + '\n' + ErrorToken.oriString + '\n' + caretMessage
        return ErrorMessageWithInformation

def generateErrorMessageWithOneArguement(ErrorMessage, ErrorToken, Actual):
        # Put in message with this format:
        # Example: Expecting + before {} <- remain this braces for formatting purpose
        # This curly braces is the location of the arguement that you putted in.
        caretMessage = ' '*(ErrorToken.column-1)+'^'
        errorLabelWithLocation="Error[{}][{}]".format(ErrorToken.line,ErrorToken.column)
        ErrorMessage = ErrorMessage.format(Actual)
        firstLineError=errorLabelWithLocation+':'+ErrorMessage
        ErrorMessageWithInformation = firstLineError + '\n' + ErrorToken.oriString + '\n' + caretMessage
        return ErrorMessageWithInformation

def generateErrorMessageWithTwoArguement(ErrorMessage, ErrorToken, Actual, Expected):
        # Put in message with this format:
        # Example: Expecting {} before {} <-- remain the braces for formatting purpose
        # This curly braces is the location of the arguement that you putted in.
        caretMessage = ' '*(ErrorToken.column-1)+'^'
        errorLabelWithLocation="Error[{}][{}]".format(ErrorToken.line,ErrorToken.column)
        ErrorMessage = ErrorMessage.format(Expected, Actual)
        firstLineError=errorLabelWithLocation+':'+ErrorMessage
        ErrorMessageWithInformation = firstLineError + '\n' + ErrorToken.oriString + '\n' + caretMessage
        return ErrorMessageWithInformation