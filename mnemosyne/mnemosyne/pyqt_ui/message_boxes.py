##############################################################################
#
# Message boxes for warnings and errors. <Peter.Bienstman@UGent.be>
#
##############################################################################

import sys, os
from mnemosyne.libmnemosyne.exceptions import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *



##############################################################################
#
# Display extra errors generated by the library.
#
#  We don't provide these strings in libmnemosyne because they need to be
#  exposed to Qt's internationalisation mechanism.
#
##############################################################################

def messagebox_errors(self, e):

    # Kludgy...
    

         
    if e.info:
        msg = QString(msg).append(QString("\n")).append(e.info)
                                   
    QMessageBox.critical(None, self.trUtf8("Mnemosyne"), msg,
                         self.trUtf8("&OK"), "", "", 0, -1)



##############################################################################
#
# queryOverwriteFile
#
##############################################################################

def queryOverwriteFile(self, fileName):
    
    status = QMessageBox.warning(None,
                                 self.trUtf8("Mnemosyne"),
                                 self.trUtf8("File exists:")\
                                 .append(QString("\n" + fileName)),
                                 self.trUtf8("&Overwrite"),
                                 self.trUtf8("&Cancel"),
                                 "", 1, -1)
    if status == 0:
        return True
    else:
        return False
