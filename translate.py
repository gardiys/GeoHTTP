def transliterate(name):
    """Transliteration method to translate Russian -> Translite"""
    letters = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'kh',
      'ц':'ts','ч':'cz','ш':'sh','щ':'shch','ъ':"",'ы':'y','ь':"’",'э':'e',
      'ю':'u','я':'ya', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'E',
      'Ж':'Zh','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
      'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'H',
      'Ц':'C','Ч':'Cz','Ш':'Sh','Щ':'Shch','Ъ':'','Ы':'y','Ь':"’",'Э':'E',
      'Ю':'U','Я':'Ya',',':'','?':'',' ':' ','~':'','!':'','@':'','#':'',
      '$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'-','=':'','+':'',
      ':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
      '[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
      'Є':'e', '—':'',"1":"1","2":"2","3":"3","4":"4","5":"5","6":"6","7":"7",
               "8":"8","9":"9","0":"0"}

    res = ""
    for letter in name:
        res += letters[letter]
    return res

if __name__ == "__main__":
    pass
