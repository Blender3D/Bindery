from djvubind import ocr

def translate(boxing, translate=True):
  page = ocr.djvuPageBox()
  line = ocr.djvuLineBox()
  word = ocr.djvuWordBox()
  
  for entry in boxing:
    if entry == 'newline':
      if word.children != []:
        line.add_element(word)
      
      page.add_element(line)
      line = ocr.djvuLineBox()
      word = ocr.djvuWordBox()
    elif entry == 'space':
      if word.children != []:
        line.add_element(word)
      
      word = ocr.djvuWordBox()
    else:
        word.add_character(entry)
  
  if word.children != []:
    line.add_element(word)
    
  if line.children != []:
    page.add_element(line)
  
  if translate:
    if page.children != []:
      return page.encode()
    else:
      return ''
  else:
    return page
