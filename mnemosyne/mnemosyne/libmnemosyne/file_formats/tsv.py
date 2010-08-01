##############################################################################
#
# process_html_unicode
#
#   Parse html style escaped unicode (e.g. &#33267;)
#
##############################################################################
import re

re0 = re.compile(r"&#(.+?);", re.DOTALL | re.IGNORECASE)

def process_html_unicode(s):

    for match in re0.finditer(s):   
        u = unichr(int(match.group(1)))  # Integer part.
        s = s.replace(match.group(), u)  # Integer part with &# and ;.
        
    return s



##############################################################################
#
# import_txt
#
#   Question and answers on a single line, separated by tabs.
#   Or, for three-sided cards: written form, pronunciation, translation,
#   separated by tabs.
#
##############################################################################

def import_txt(filename, default_cat, reset_learning_data=False):
    
    global cards

    imported_cards = []

    # Parse txt file.

    avg_easiness = average_easiness()

    f = None
    try:
        f = file(filename)
    except:
        try:
            f = file(filename.encode("latin"))
        except:
            raise LoadError()
    
    for line in f:
        
        try:
            line = unicode(line, "utf-8")
        except:
            try:
                line = unicode(line, "latin")
            except:
                raise EncodingError()

        line = line.rstrip()
        line = process_html_unicode(line)
        
        if len(line) == 0:
            continue

        if line[0] == u'\ufeff': # Microsoft Word unicode export oddity.
            line = line[1:]

        fields = line.split('\t')

        # Three sided card.

        if len(fields) >= 3:

            # Card 1.
            
            card = Card()
            
            card.q = fields[0]
            card.a = fields[1] + '\n' + fields[2]
            card.easiness = avg_easiness
            card.cat = default_cat
            card.new_id()
                    
            imported_cards.append(card)

            id = card.id

            # Card 2.
            
            card = Card()
            
            card.q = fields[2]
            card.a = fields[0] + '\n' + fields[1]
            card.easiness = avg_easiness
            card.cat = default_cat
            card.id = id + '.tr.1'
                    
            imported_cards.append(card)

        # Two sided card.
        
        elif len(fields) == 2:
            
            card = Card()
            
            card.q = fields[0]
            card.a = fields[1]
            card.easiness = avg_easiness
            card.cat = default_cat
            card.new_id()
                    
            imported_cards.append(card)
            
        else:
            raise MissingAnswerError(info=line)

    return imported_cards



##############################################################################
#
# export_txt
#
#   Newlines are converted to <br> to keep cards on a single line.
#
##############################################################################

def export_txt(filename, cat_names_to_export, reset_learning_data=False):

    try:
        outfile = file(filename,'w')
    except:
        return False

    for e in cards:
        if e.cat.name in cat_names_to_export:
            question = e.q.encode("utf-8")
            question = question.replace("\t", " ")
            question = question.replace("\n", "<br>")
            
            answer = e.a.encode("utf-8")
            answer = answer.replace("\t", " ")
            answer = answer.replace("\n", "<br>")
            
            print >> outfile, question + "\t" + answer

    outfile.close()

    return True
    

#register_file_format(_("Text with tab separated Q/A"),
#                     filter=_("Text files (*.txt *.TXT)"),
#                     import_function=import_txt,
#                     export_function=export_txt)


##############################################################################
#
# import_txt_2
#
#   Question and answers each on a separate line.
#
##############################################################################

def import_txt_2(filename, default_cat, reset_learning_data=False):
    
    global cards

    imported_cards = []

    # Parse txt file.

    #avg_easiness = average_easiness()
    avg_easiness = 2.5

    f = None
    try:
        f = file(filename)
    except:
        try:
            f = file(filename.encode("latin"))
        except:
            raise LoadError()

    Q_A = []
    
    for line in f:
        
        try:
            line = unicode(line, "utf-8")
        except:
            try:
                line = unicode(line, "latin")
            except:
                raise EncodingError()

        line = line.rstrip()
        line = process_html_unicode(line)
        
        if len(line) == 0:
            continue

        if line[0] == u'\ufeff': # Microsoft Word unicode export oddity.
            line = line[1:]

        Q_A.append(line)

        if len(Q_A) == 2:
            
            card = Card()

            card.q = Q_A[0]
            card.a = Q_A[1]    
        
            card.easiness = avg_easiness
            card.cat = default_cat
            card.new_id()
                    
            imported_cards.append(card)

            Q_A = []

    return imported_cards

#register_file_format(_("Text with Q and A each on separate line"),
#                     filter=_("Text files (*.txt *.TXT)"),
#                     import_function=import_txt_2,
#                     export_function=False)


from mnemosyne.libmnemosyne.translator import _
from mnemosyne.libmnemosyne.file_format import FileFormat

class TabSeparated(FileFormat):    

    description = _("Text with tab separated Q/A")
    filename_filter = description + " (*.txt)"
    import_possible = True
    export_possible = False

    def do_import(self, filename, tag_names, reset_learning_data=False):

        db = self.database()
        try:
            fimp = file(filename)
        except IOError, exc_obj:
            self.main_widget().error_box(str(exc_obj))
            return -1 

        # Prepare progress bar widget
        progress = self.component_manager.get_current("progress_dialog")\
                   (self.component_manager)
        progress.set_text(_("Importing cards..."))
        progress.set_range(0, sum(1 for l in open(filename, 'r')))
        progress.set_value(0)
        count = 0
 
        for line in fimp:
            line = line.strip()
            if not line:
                continue
            count += 1
            progress.set_value(count)
            fields = line.split('\t')

            # Orphaned 2 or 3 sided card.
            card_type = self.card_type_by_id("1")
            fact_data = {"q": unicode(fields[0]), "a": unicode(fields[1])}
            self.controller().create_new_cards(fact_data, card_type, -1, \
                tag_names, check_for_duplicates=False, save=False)
