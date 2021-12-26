class Text:
    def __init__(self, text):
        self.text = text
        
        self.RUS = {'q':"й",'w':'ц','e':'у','r':'к','t':'е','y':'н','u':'г','i':'ш','o':'щ','p':'з','[':'х',']':'ъ',
                    'a':'ф','s':'ы','d':'в','f':'а','g':'п','h':'р','j':'о','k':'л','l':'д',';':'ж',"'":'э',
                    'z':'я','x':'ч','c':'с','v':'м','b':'и','n':'т','m':'ь',',':'б','.':'ю',
                    "Q":'Й','W':'Ц','E':'У','R':'К','T':'Е','Y':'Н','U':'Г','I':'Ш','O':'Щ','P':'З','{':'Х','}':'Ъ',
                    'A':'Ф','S':'Ы','D':'В','F':'А','G':'П','H':'Р','J':'О','K':'Л','L':'Д',':':'Ж','"':'Э',
                    'Z':'Я','X':'Ч','C':'С','V':'М','B':'И','N':'Т','M':'Ь','<':'Б','>':'Ю'}
        self.ENG = {"й":'q','ц':'w','у':'e','к':'r','е':'t','н':'y','г':'u','ш':'i','щ':'o','з':'p','х':'[','ъ':']',
                    'ф':'a','ы':'s','в':'d','а':'f','п':'g','р':'h','о':'j','л':'k','д':'l','ж':';','э':"'",
                    'я':'z','ч':'x','с':'c','м':'v','и':'b','т':'n','ь':'m','б':',','ю':'.',
                    'Й':'Q','Ц':'W','У':'E','К':'R','Е':'T','Н':'Y','Г':'U','Ш':'I','Щ':'O','З':'P','Х':'{','Ъ':'}',
                    'Ф':'A','Ы':'S','В':'D','А':'F','П':'G','Р':'H','О':'J','Л':'K','Д':'L','Ж':';',"Э":'"',
                    'Я':'Z','Ч':'X','С':'C','М':'V','И':'B','Т':'N','Ь':'M','Б':'<','Ю':'>'}
                    
        self.ENG_UP = {'q':"Q",'w':'W','e':'E','r':'R','t':'T','y':'Y','u':'U','i':'I','o':'O','p':'P',
                    'a':'A','s':'S','d':'D','f':'F','g':'G','h':'H','j':'J','k':'K','l':'L',
                    'z':'Z','x':'X','c':'C','v':'V','b':'B','n':'N','m':'M'}
        self.RUS_UP = {"й":'Й','ц':'Ц','у':'У','к':'К','е':'Е','н':'Н','г':'Г','ш':'Ш','щ':'Щ','з':'З','х':'Х','ъ':'Ъ',
                    'ф':'Ф','ы':'Ы','в':'В','а':'А','п':'П','р':'Р','о':'О','л':'Л','д':'Д','ж':'Ж','э':"Э",
                    'я':'Я','ч':'Ч','с':'С','м':'М','и':'И','т':'Т','ь':'Ь','б':'Б','ю':'Ю'}
                    
        self.ENG_DOWN = {"Q":'q','W':'w','E':'e','R':'r','T':'t','Y':'y','U':'u','I':'i','O':'o','P':'p',
                    'A':'a','S':'s','D':'d','F':'f','G':'g','H':'h','J':'j','K':'k','L':'l',
                    'Z':'z','X':'x','C':'c','V':'v','B':'b','N':'n','M':'m'}
        self.RUS_DOWN = {'Й':'й','Ц':'ц','У':'у','К':'к','Е':'е','Н':'н','Г':'г','Ш':'ш','Щ':'щ','З':'з','Х':'х','Ъ':'ъ',
                    'Ф':'ф','Ы':'ы','В':'в','А':'а','П':'п','Р':'р','О':'о','Л':'л','Д':'д','Ж':'ж',"Э":'э',
                    'Я':'я','Ч':'ч','С':'с','М':'м','И':'и','Т':'т','Ь':'ь','Б':'б','Ю':'ю'}
                    
        self.RUS_TRANSLIT = {"й":'y','ц':'c','у':'u','к':'k','е':'e','н':'n','г':'g','ш':'sh','щ':'shch','з':'z','х':'h','ъ':'',
                    'ф':'f','ы':'y','в':'v','а':'a','п':'p','р':'r','о':'o','л':'l','д':'d','ж':'j','э':"e",
                    'я':'ya','ч':'ch','с':'s','м':'m','и':'i','т':'t','ь':'','б':'b','ю':'yu',
                    'Й':'Y','Ц':'C','У':'U','К':'K','Е':'E','Н':'N','Г':'G','Ш':'Sh','Щ':'Shch','З':'Z','Х':'H','Ъ':'',
                    'Ф':'F','Ы':'Y','В':'V','А':'A','П':'P','Р':'R','О':'O','Л':'L','Д':'D','Ж':'J',"Э":'E',
                    'Я':'Ya','Ч':'Ch','С':'S','М':'M','И':'I','Т':'T','Ь':'','Б':'B','Ю':'Yu'}
        self.ENG_TRANSLIT = {'q':"ку",'w':'в','e':'е','r':'р','t':'е','y':'й','u':'у','i':'и','o':'о','p':'п',
                    'a':'а','s':'с','d':'д','f':'ф','g':'г','h':'х','j':'ж','k':'к','l':'л',
                    'z':'з','c':'ц','v':'в','b':'б','n':'н','m':'м',
                    "Q":'Ку','W':'В','E':'Е','R':'Р','T':'Т','Y':'Й','U':'У','I':'И','O':'О','P':'П',
                    'A':'А','S':'С','D':'Д','F':'Ф','G':'Г','H':'Х','J':'Ж','K':'К','L':'Л',
                    'Z':'З','C':'Ц','V':'В','B':'Б','N':'Н','M':'М'}
       
    def upper(self):
        _text = ""
        for num, symbol in enumerate(self.text):
            if symbol in self.RUS_UP:
                _text += self.RUS_UP[symbol]
            elif symbol in self.ENG_UP:
                _text += self.ENG_UP[symbol]
                
            else:
                _text += symbol
                
        return _text
        
    def lower(self):
        _text = ""
        for num, symbol in enumerate(self.text):
            if symbol in self.RUS_DOWN:
                _text += self.RUS_DOWN[symbol]
            elif symbol in self.ENG_DOWN:
                _text += self.ENG_DOWN[symbol]
                
            else:
                _text += symbol
                
        return _text
       
    def eng_to_rus(self):
        _text = ""
        for num, symbol in enumerate(self.text):
            if symbol in self.RUS:
                _text += self.RUS[symbol]
                
            else:
                _text += symbol
                   
        return _text
        
    def rus_to_eng(self):
        _text = ""
        for num, symbol in enumerate(self.text):
            if symbol in self.ENG:
                _text += self.ENG[symbol]
            
            else:
                _text += symbol
                
        return _text
        
    def translit(self, lang:str="rus"):
        _text=""
        
        if lang == "rus":
            _LANG = self.RUS_TRANSLIT     
        if lang == "eng":
            _LANG = self.ENG_TRANSLIT
            
        else:
            return print("Text.translit Error(1): lang not found.")
        
        for num, symbol in enumerate(self.text):
            if symbol in _LANG:
                _text += _LANG[symbol]
                    
            else:
                _text += symbol

        return _text
        
class Cipher:
    def __init__(self, text):
        self.text = text
        
        self.RUS_ABC = ['а','б','в','г','д','е','ё','ж','з','и','й',
                        'к','л','м','н','о','п','р','с','т','у','ф',
                        'х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я']
                        
        self.ENG_ABC = ['a','b','c','d','e','f','g','h','i','j','k',
                        'l','m','n','o','p','q','r','s','t','u','v',
                        'w','x','y','z']
        
    def transposing(self):
        _text=""
        num1 = 0
        for i in range(4):
            num1 += 1
            num2 = num1
            for symbol in range(len(self.text)+1):
                if symbol == num2:
                    num2+=4
                    _text+=self.text[symbol-1]

        return _text
        
    def to_A1Z26(self, lang:str="rus"):
        _text = ''
        low_text = Text(self.text).lower()
        
        if lang == 'rus':
            _ABC = self.RUS_ABC
        elif lang == 'eng':
            _ABC = self.ENG_ABC
            
        else:
            return print("Text.translit Error(1): lang not found.")
            
        for num, symbol in enumerate(low_text):
            if symbol in _ABC:
                _text += str(_ABC.index(symbol))
                    
                if num+1 != len(self.text):
                    if low_text[num+1] != ' ':
                        _text += '-'    
            elif symbol == ' ':
                _text += ' '
                    
            else:
                return print("Cipher.to_A1Z26 Error(2): symbol not found.")
                    
        return _text
        
    def from_A1Z26(self, lang:str="rus"):
        _text = ''
        _int = ''
        
        if lang == 'rus':
            _ABC = self.RUS_ABC
        elif lang == 'eng':
            _ABC = self.ENG_ABC
            
        else:
            return print("Text.translit Error(1): lang not found.")
            
        for num, symbol in enumerate(self.text):
            try:
                if symbol == '-' or symbol == ' ':
                    continue
                else:
                    int(symbol)
            except:
                return print("Cipher.from_A1Z26 Error(3): letters must be integer or '-' and ' '.")
                              
            if symbol != '-' or symbol != ' ':
                _int += symbol
                            
            try:
                if self.text[num+1]=='-' or self.text[num+1]==' ':
                    _text += self.RUS_ABC[int(_int.replace('-', ''))]
                    _int = ''
                        
                    if self.text[num+1]==' ':
                        _text += ' '
            except:
                _text += self.RUS_ABC[int(_int.replace('-', ''))]
                    
        return _text