import math
import vigenere

def pre_treatment(message):
    # 提取字母
    tmp_text = ''
    for c in message:
        if c.isalpha():
            tmp_text += c
    # 全员大写
    return(tmp_text.upper())

def find_repeat_sequences_spacings(message):
    # 预处理字符串    
    tmp_text = pre_treatment(message)
    # 生成重复序列间隔字典
    dic = dict()
    # 查找3-5位字母长度的重复序列
    for strlen in range(3,6):
        for i in range(0,len(tmp_text)-2*strlen+1):
            tmp_str = tmp_text[i:i+strlen]
            tmp_count = tmp_text.count(tmp_str)
            if tmp_count > 1:
                if tmp_str not in dic.keys():
                    last = tmp_text.find(tmp_str)
                    find_list = [last]
                    for j in range(1,tmp_count):
                        now = tmp_text.find(tmp_str,last+strlen)
                        find_list.append(now)
                        last = now
                    spacing_list = []
                    listlen = len(find_list)
                    for j in range(0,listlen-1):
                        for k in range(j+1,listlen):
                            spacing_list.append(find_list[k]-find_list[j])
                    dic[tmp_str] = spacing_list
        
    return(dic)

def get_useful_factors(num):
    factors_list = []
    for i in range(2,math.isqrt(num)+1):
        if num % i == 0:
            factors_list.append(i)
            j = num//i
            if i != j:
                factors_list.append(j)
    factors_list.sort()
    
    return(factors_list)

def get_possible_keylen(message):
    tmp_dic = find_repeat_sequences_spacings(message)
    dic_fac =  dict()
    for i in tmp_dic:
        for j in tmp_dic[i]:
            tmp_fac = get_useful_factors(j)
            for k in tmp_fac:
                if k not in dic_fac:
                    dic_fac[k] = 1
                else:
                    dic_fac[k] += 1
    list_fac = []
    for i in sorted(dic_fac.items(), key=lambda x:(-x[1],x[0])):
        # print(i)
        list_fac.append(i[0])
    
    return(list_fac)

def get_nth_subkeys_letters(n, key_length, message):
    # 预处理字符串    
    tmp_text = pre_treatment(message)
    tmp_str = ''
    i = 0
    for c in tmp_text:
        if i % key_length == n-1:
            tmp_str += c
        i += 1

    return(tmp_str)

def freq_match_score(message):
    ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    match_score = 0
    tmp_text = pre_treatment(message)
    # 初始化计数字典并计数
#    base = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#    上面这行注释绝妙，无意间解决了ETAOIN排序问题
    dic_letter_freq = dict()
    for c in ETAOIN:
        dic_letter_freq[c] = 0
    for c in tmp_text:
        dic_letter_freq[c] += 1
    # 生成频数字母列表字典
    dic_freq_letter = dict()
    for i in dic_letter_freq.items():
        if i[1] not in dic_freq_letter.keys():
            dic_freq_letter[i[1]] = [i[0]]
        else:
            dic_freq_letter[i[1]].append(i[0])
    # 频数字典排序生成匹配串
    freq_string = ''
    for f in sorted(dic_freq_letter.items(),key=lambda x:(-x[0])):
        for c in f[1]:
            freq_string += c
    # 累计频率匹配分数
    for c in freq_string[:6]:
        if c in ETAOIN[:6]:
            match_score += 1
    for c in freq_string[-6:]:
        if c in ETAOIN[-6:]:
            match_score += 1

    return(match_score)

# 另一种字母频率分析
def freq_score(message):
    tmp_text = pre_treatment(message)
    dic_freq = dict()
    dic_freq = {'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253,
                'E': 12.702, 'F': 2.228, 'G': 2.015, 'H': 6.094,
                'I': 6.966, 'J': 0.153, 'K': 0.772, 'L': 4.025,
                'M': 2.406, 'N': 6.749, 'O': 7.507, 'P': 1.929,
                'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
                'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150,
                'Y': 1.974, 'Z': 0.074}
    count = 0
    sum = 0
    for c in tmp_text:
        count += 1
        sum += dic_freq[c]
    return(sum/count)

def is_english(message, word_percentage=20, letter_percentage=85):
    # 加载字典生成字典列表
    with open('dictionary.txt', 'r') as f:
        wordlist = f.readlines()
    for i in range(0,len(wordlist)):
        wordlist[i] = wordlist[i].rstrip('\n')
    # 英文检测
    tmp_text = message.upper()
    tmp_wordlist = []
    tmp_word = ''
    sum_letter = 0
    sum_word = 0
    for c in tmp_text:
        if c.isalpha():
            tmp_word += c
            sum_letter += 1
        else:
            if c.isspace():
                sum_letter += 1
            tmp_wordlist.append(tmp_word)
            tmp_word = ''
    for w in tmp_wordlist:
        if w in wordlist:
            sum_word += 1
    freq_letter = sum_letter / len(tmp_text) * 100
    freq_word = sum_word / len(tmp_wordlist) * 100
#    print(freq_letter)
#    print(freq_word)
    if (freq_letter >= letter_percentage) and (freq_word >= word_percentage):
        return(True)
    else:
        return(False)

def test():
    ciphertext = 'Ppqca xqvekg ybnkmazu ybngbal jon i tszm jyim. Vrag voht vrau c tksg. Ddwuo xitlazu vavv raz c vkb qp iwpou.'
    
    # print(find_repeat_sequences_spacings(ciphertext))
    # print(get_useful_factors(24))

    # print(get_possible_keylen(ciphertext))

    # for i in range(1, 5):
    #     print(get_nth_subkeys_letters(i, 4, ciphertext))
    
    # message = 'I rc ascwuiluhnviwuetnh,osgaa ice tipeeeee slnatsfietgi tittynecenisl. e fo f fnc isltn sn o a yrs sd onisli ,l erglei trhfmwfrogotn,l stcofiit.aea wesn,lnc ee w,l eIh eeehoer ros iol er snh nl oahsts ilasvih tvfeh rtira id thatnie.im ei-dlmf i thszonsisehroe, aiehcdsanahiec gv gyedsB affcahiecesd d lee onsdihsoc nin cethiTitx eRneahgin r e teom fbiotd n ntacscwevhtdhnhpiwru'
    # print(freq_match_score(message))

def kasiski(message):
    flag = False
    # 尝试最有可能的5种密钥长度
    for keylen in get_possible_keylen(message)[:5]:
        print('keylen = ', keylen)
        dic_key = dict()
        for i in range(0, keylen):
            base_string = get_nth_subkeys_letters(i+1, keylen, message)
            dic_score = dict()
            top_guess = 3   # 每位密钥测试3个最有可能的字母
            for j in range(0, 26):
                tmp_string = ''
                for c in base_string:
                    tmp_string += chr(ord('A')+(ord(c)-ord('A')-j) % 26)
                    dic_score[chr(ord('A')+j)] = freq_score(tmp_string)
            dic_key[i] = ''
            tmp_count = 0
            for k in sorted(dic_score.items(),key=lambda x:-x[1]):
                tmp_count += 1
                dic_key[i] += k[0]
                print(i,tmp_count, k)
                if tmp_count == top_guess:
                    break
        print(dic_key)
        # 参考二进制思想生成可能密钥
        for i in range(0, top_guess**keylen):
            tmp_key = ''
            if i == 0:
                for j in range(0, keylen):
                    tmp_key += dic_key[j][0]
            else:
                tmp = i
                dkey = -1
                while tmp > 0:
                    dkey += 1
                    dvalue = tmp % top_guess
                    tmp_key += dic_key[dkey][dvalue]
                    tmp //= top_guess
                for j in range(dkey+1, keylen):
                    tmp_key += dic_key[j][0]
            # 尝试解密
            decrypted_text = vigenere.decrypt(message, tmp_key)
            if is_english(decrypted_text):
                print(decrypted_text)
                print('key =',tmp_key)
                flag = True
                break
        if flag:
            break

def main():
    message = '' 
    with open('ciphertext_vigenere.txt','r') as f:
        for i in f.readlines():
            message += i

    print(message)

    kasiski(message)

if __name__ == '__main__':
#    test()
    main()