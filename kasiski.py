import math
from vigenere import decrypt


def purify(message):
    """
    去除原始密文中的非字母字符，并全部大写
    :param message: 原始密文字符串
    :return: 纯化后密文字符串
    """
    tmp_text = ''
    for ch in message:
        if ch.isalpha():
            tmp_text += ch
    return tmp_text.upper()


def find_repeat_sequences_spacings(message):
    """
    查找重复序列，长度限制为3到5个字符
    :param message: 密文字符串
    :return: 一个字典，键是序列，值是序列间隔列表（重复序列之间间隔的字母数）
    """
    tmp_text = purify(message)
    dic = dict()

    for str_len in range(3, 6):
        for i in range(0, len(tmp_text) - 2 * str_len + 1):
            tmp_str = tmp_text[i:i + str_len]
            tmp_count = tmp_text.count(tmp_str)
            if tmp_count > 1 and tmp_str not in dic.keys():
                index = tmp_text.find(tmp_str)
                find_list = [index]
                for j in range(1, tmp_count):
                    index = tmp_text.find(tmp_str, index + str_len)
                    find_list.append(index)
                spacing_list = []
                list_len = len(find_list)
                for j in range(0, list_len - 1):
                    for k in range(j + 1, list_len):
                        spacing_list.append(find_list[k] - find_list[j])
                dic[tmp_str] = spacing_list

    return dic


def get_useful_factors(num):
    """
    通过因数找到最可能的密钥字符串长度
    :param num: 待分解数字
    :return: 因数列表
    """
    factors_list = []
    for i in range(2, math.isqrt(num) + 1):
        if num % i == 0:
            factors_list.append(i)
            j = num // i
            if i != j:
                factors_list.append(j)
    factors_list.sort()

    return factors_list


def get_possible_key_len(message):
    """
    根据密文分析得出密钥可能的长度
    :param message: 密文
    :return: 因数字典，按照频率逆序排列
    """
    tmp_dic = find_repeat_sequences_spacings(message)
    dic_fac = dict()
    for i in tmp_dic:
        for j in tmp_dic[i]:
            tmp_fac = get_useful_factors(j)
            for k in tmp_fac:
                if k not in dic_fac:
                    dic_fac[k] = 1
                else:
                    dic_fac[k] += 1
    list_fac = []
    for i in sorted(dic_fac.items(), key=lambda x: (-x[1], x[0])):
        list_fac.append(i[0])
    return list_fac


def get_nth_subkeys_letters(n, key_length, message):
    """
    将message字符串按照key_length长度分组，取每组中的第n个字符组成新字符串
    :param n: 每组中第几个字符
    :param key_length: 分组长度
    :param message: 原始字符串
    :return: 新字符串
    """
    tmp_text = purify(message)
    tmp_str = ''
    for i in range(n - 1, len(tmp_text), key_length):
        tmp_str += tmp_text[i]

    return tmp_str


def freq_match_score(message):
    """
    计算所给字符串的频率匹配分数
    :param message: 待分析字符串
    :return: 频率匹配分数
    """
    ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    match_score = 0
    tmp_text = purify(message)

    dic_letter_freq = dict()
    for c in ETAOIN:
        dic_letter_freq[c] = 0
    for c in tmp_text:
        dic_letter_freq[c] += 1

    dic_freq_letter = dict()
    for i in dic_letter_freq.items():
        if i[1] not in dic_freq_letter.keys():
            dic_freq_letter[i[1]] = [i[0]]
        else:
            dic_freq_letter[i[1]].append(i[0])

    freq_string = ''
    for f in sorted(dic_freq_letter.items(), key=lambda x: -x[0]):
        for c in f[1]:
            freq_string += c

    for c in freq_string[:6]:
        if c in ETAOIN[:6]:
            match_score += 1
    for c in freq_string[-6:]:
        if c in ETAOIN[-6:]:
            match_score += 1

    return match_score


def is_english(message, word_percentage=20, letter_percentage=85):
    """
    评估字符串内容是否为正常英文文本
    :param message: 待测字符串
    :param word_percentage: 单词匹配度
    :param letter_percentage: 字符匹配度
    :return: 判断结果
    """
    with open('dictionary.txt', 'r') as f:
        wordlist = f.readlines()
    for i in range(0, len(wordlist)):
        wordlist[i] = wordlist[i].rstrip('\n')

    tmp_text = message.upper()
    tmp_wordlist = []
    tmp_word = ''
    real_letter = 0
    real_word = 0
    for ch in tmp_text:
        if ch.isalpha():
            tmp_word += ch
            real_letter += 1
        else:
            if ch.isspace():
                real_letter += 1
            tmp_wordlist.append(tmp_word)
            tmp_word = ''
    for w in tmp_wordlist:
        if w in wordlist:
            real_word += 1
    freq_letter = real_letter / len(tmp_text) * 100
    freq_word = real_word / len(tmp_wordlist) * 100

    if (freq_letter >= letter_percentage) and (freq_word >= word_percentage):
        return True
    else:
        return False


def kasiski(message):
    """
    卡西斯基试验
    :param message: 密文字符串
    :return: 无
    """
    flag = False
    for key_len in get_possible_key_len(message)[:5]:
        print('Testing key_len:', key_len)
        dic_key = dict()
        top_guess = 3
        for i in range(0, key_len):
            base_string = get_nth_subkeys_letters(i + 1, key_len, message)
            dic_score = dict()
            for j in range(0, 26):
                tmp_string = ''
                for ch in base_string:
                    tmp_string += chr(ord('A') + (ord(ch) - ord('A') - j) % 26)
                dic_score[chr(ord('A')+j)] = freq_match_score(tmp_string)
            dic_key[i] = ''
            print("Position:", i)
            for k in sorted(dic_score.items(), key=lambda x: -x[1])[:top_guess]:
                dic_key[i] += k[0]
                print("Test letter:", "Freq_score:", k, end=" ")
            print()

        print("Trying keys...")
        for i in range(0, top_guess ** key_len):
            tmp_key = ''
            if i == 0:
                for j in range(0, key_len):
                    tmp_key += dic_key[j][0]
            else:
                tmp = i
                dkey = -1
                while tmp > 0:
                    dkey += 1
                    dvalue = tmp % top_guess
                    tmp_key += dic_key[dkey][dvalue]
                    tmp //= top_guess
                for j in range(dkey + 1, key_len):
                    tmp_key += dic_key[j][0]

            decrypted_text = decrypt(message, tmp_key)
            if is_english(decrypted_text):
                print('Found key:', tmp_key)
                print("The decrypted text is:")
                print(decrypted_text)
                flag = True
                break
        if flag:
            break
        print("Key_len", key_len, "is not correct.")


def main():
    message = ''
    with open('ciphertext_vigenere.txt', 'r') as f:
        for i in f.readlines():
            message += i
    print(message)
    kasiski(message)


if __name__ == '__main__':
    main()
