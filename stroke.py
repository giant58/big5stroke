# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 12:41:45 2020

@author: Giant Su
"""

# source: https://shann.idv.tw/Chinese/b5strok-bs.html

common_char=((1,'一'),(2,'丁'),(3,'三'),(4,'丑'),(5,'丙'),
             (6,'丞'),(7,'串'),(8,'並'),(9,'亟'),(10,'乘'),
             (11,'乾'),(12,'傢'),(13,'亂'),(14,'僧'),(15,'億'),
             (16,'儒'),(17,'優'),(18,'叢'),(19,'儳'),(20,'嚷'),
             (21,'儷'),(22,'儼'),(23,'囌'),(24,'囑'),(25,'廳'),
             (26,'灤'),(27,'纜'),(28,'豔'),(29,'爨'),(30,'鸞'),(32,'籲'))
rare_char=((2,'乂'),(3,'万'),(4,'丏'),(5,'丱'),
           (6,'伎'),(7,'佖'),(8,'丳'),(9,'俍'),(10,'倞'),
           (11,'乿'),(12,'傛'),(13,'亃'),(14,'僦'),(15,'僿'),
           (16,'儜'),(17,'儦'),(18,'儱'),(19,'儴'),(20,'匷'),
           (21,'儺'),(22,'亹'),(23,'儽'),(24,'囓'),(25,'囔'),
           (26,'圞'),(27,'灨'),(28,'戇'),(26,'鬮'),(28,'鸙'),(33,'爩'),(29,'虋'),(30,'癵'),
           (31,'灩'),(32,'灪'),(33,'麤'),(35,'齾'),(36,'齉'),(48,'龘'))
# below rare characters cannot be encoded by big5 in current Python version
special_char={'碁':13,'銹':15,'裏':13,'墻':16,'恒':9,'粧':12,'嫺':15}

common_code=((1,'a440'),(2,'a442'),(3,'a454'),(4,'a4a1'),(5,'a4fe'),
             (6,'a5e0'),(7,'a6ea'),(8,'a8c3'),(9,'ab45'),(10,'adbc'),
             (11,'b0ae'),(12,'b3c3'),(13,'b6c3'),(14,'b9ac'),(15,'bbf5'),
             (16,'bea7'),(17,'c075'),(18,'c24f'),(19,'c35f'),(20,'c457'),
             (21,'c4d7'),(22,'c56b'),(23,'c5c8'),(24,'c5f1'),(25,'c655'),
             (26,'c665'),(27,'c66c'),(28,'c676'),(29,'c679'),(30,'c67d'),
             (32,'c67e'),(-1,'c67f'))  # last record is for search algorithm as upper boundry
rare_code=((2,'c940'),(3,'c945'),(4,'c94d'),(5,'c963'),
           (6,'c9ab'),(7,'ca5a'),(8,'cbb1'),(9,'cddd'),(10,'d0c8'),
           (11,'d44b'),(12,'d851'),(13,'dcb1'),(14,'e0f0'),(15,'e4e6'),
           (16,'e8f4'),(17,'ecb9'),(18,'efb7'),(19,'f1eb'),(20,'f3fd'),
           (21,'f5c0'),(22,'f6d6'),(23,'f7d0'),(24,'f8a5'),(25,'f8ee'),
           (26,'f96b'),(27,'f9a2'),(28,'f9ba'),(26,'f9c4'),(28,'f9c5'),(33,'f9c6'),(29,'f9c7'),(30,'f9cc'),
           (31,'f9d0'),(32,'f9d1'),(33,'f9d2'),(35,'f9d3'),(36,'f9d4'),
           (48,'f9d5'),(-1,'f9d6'))  # last record is for search algorithm as upper boundry
    
common_len=len(common_code)
common_min=common_code[0][1]
common_max=common_code[common_len-1][1]
rare_len=len(rare_code)
rare_min=rare_code[0][1]
rare_max=rare_code[rare_len-1][1]

def is_chinese(ch):
    ''' check if ch is a Chinese character (including Simplified Chinese)
    '''
    return '\u4e00' <= ch <= '\u9fa5'

def big5_code(ch):
    ''' input a unicode char and return it's big5 code
    if it can not be encoded into big5, the return value is ''
    '''
    return ch.encode('big5',errors='ignore').hex()  # ignore error & return ''
#    return ch.encode('big5',errors='replace').hex()  # return'?' if error

def is_big5(ch):
    ''' check if ch is a Traditional Chinese
    '''
    return ch in special_char or is_chinese(ch) and (big5_code(ch)!='')

def big5_str(s):
    ''' return the big5 encoded hex string of the input string
    could be used for chinese char sort (by stroke)
    '''
    return ''.join([big5_code(ch) for ch in s])

def csorted(lst,reverse=False):
    ''' sort a list by stroke and return the sorted result
    only works for Traditional Chinese characters, big5 code is sorted by stroke
    '''
    return sorted(lst,key=lambda a:a.encode('big5',errors='replace'),reverse=reverse)

def cstrip(s):
    ''' return a string only contains Chinese characters
    '''
    return ''.join([ch for ch in s if is_chinese(ch)])

def big5strip(s):
    ''' return a string only contains Traditional Chinese characters
    '''
    return ''.join([ch for ch in s if is_big5(ch)])

'''
# pre-process to convert char tuple into big5 code
common_code, rare_code = [], []
for i in range(common_len):
    common_code.append((common_char[i][0],big5_code(common_char[i][1])))
for i in range(rare_len):
    rare_code.append((rare_char[i][0],big5_code(rare_char[i][1])))
'''
"""
def find_stroke2(array, length, x):
    ''' use recursive binary search to find the stroke of a char
    ''' 
    if length>=2: 
        mid = (length-1) // 2
        if array[mid][1] <= x < array[mid+1][1]: 
            return array[mid][0] 
        elif array[mid][1] > x: 
            return find_stroke2(array[:mid+1], mid+1, x) 
        else: 
            return find_stroke2(array[mid+1:], length-mid-1, x) 
    else: 
        # something wrong 
        print('binary search error')
        return -1
"""

def find_stroke(array, low, high, x):
    ''' use binary search to find the stroke of a char
    ''' 
    while high >= low: 
        mid = (high + low) // 2
        if array[mid][1] <= x < array[mid+1][1]: 
            return array[mid][0] 
        elif array[mid][1] > x:
            high=mid-1
        else: 
            low=mid + 1 
    else: 
        print('binary search error')
        return -1

def stroke(s):
    ''' return the stroke numbers for each characters in the input string
    
    * Argument:
        s: input string (not necessary all Chinese characters)
        
    * Return values in the list:
        >0: stroke number of the big5 character
        =0: is not a Chinese character
        -1: is not a big5 character (i.e. simplified Chinese)
        -2: something wrong
        
    >>> stroke('鸞籲乂一丁齉龘碁粧')
    [30, 32, 2, 1, 2, 36, 48, 13, 12]
    >>> stroke('?1x苏纪安')
    [0, 0, 0, -1, -1, 6]
    '''
    if type(s)!=str:
        print('input is not a string')
        return -1
    else:
        num=[-2 for i in range(len(s))]
        for i in range(len(s)):
            # if not a Chinese character
            if not is_chinese(s[i]):
#                print(s[i],'is not a Chinese character!')
                num[i] = 0
            # if it's special Chinese character
            elif s[i] in special_char:
                num[i]=special_char[s[i]]
            # is other Chinese character
            else:
                bc=big5_code(s[i])
                if common_min <= bc < common_max:
                    num[i] = find_stroke(common_code,0,common_len,bc)
                elif rare_min <= bc < rare_max:
                    num[i] = find_stroke(rare_code,0,rare_len,bc)
                elif bc=='': 
#                    print(s[i],'can not be encoded into big5')
                    num[i] = -1
        return num

''' below is for unit test
if __name__ == '__main__':
    import doctest
    doctest.testmod()
'''