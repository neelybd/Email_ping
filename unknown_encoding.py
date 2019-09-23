import pandas as pd

def open_unknown_csv(file_in, delimination):
    encode_index = 0
    encoders = ['utf_8', 'latin1', 'utf_16',
                'ascii', 'big5', 'big5hkscs', 'cp037', 'cp424',
                'cp437', 'cp500', 'cp720', 'cp737', 'cp775',
                'cp850', 'cp852', 'cp855', 'cp856', 'cp857',
                'cp858', 'cp860', 'cp861', 'cp862', 'cp863',
                'cp864', 'cp865', 'cp866', 'cp869', 'cp874',
                'cp875', 'cp932', 'cp949', 'cp950', 'cp1006',
                'cp1026', 'cp1140', 'cp1250', 'cp1251', 'cp1252',
                'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257',
                'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr',
                'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp',
                'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext',
                'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4',
                'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9',
                'iso8859_10', 'iso8859_11', 'iso8859_13', 'iso8859_14', 'iso8859_15',
                'iso8859_16', 'johab', 'koi8_r', 'koi8_u', 'mac_cyrillic',
                'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish',
                'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_32',
                'utf_32_be', 'utf_32_le', 'utf_16', 'utf_16_be', 'utf_16_le',
                'utf_7', 'utf_8', 'utf_8_sig']

    data = open_file(file_in, encoders[encode_index], delimination)
    encoder = encoders[encode_index]
    while type(data) == str:
        print("Encoder error: " + encoders[encode_index])
        if encode_index < len(encoders) - 1:
            encode_index = encode_index + 1
            try:
                print("Trying encoder: " + encoders[encode_index])
                data = open_file(file_in, encoders[encode_index], delimination)
            except:
                continue
            print("")
            encoder = encoders[encode_index]
        else:
            print("Can't find appropriate encoder")
            input("Program Terminated. Press Enter to continue...")
            exit()

    return data

def encoding_selection(statement):
    basic_encoders = ['utf_8', 'latin1', 'utf_16', 'See All Encoders']
    advanced_encoders = ['ascii', 'big5', 'big5hkscs', 'cp037', 'cp424',
                         'cp437', 'cp500', 'cp720', 'cp737', 'cp775',
                         'cp850', 'cp852', 'cp855', 'cp856', 'cp857',
                         'cp858', 'cp860', 'cp861', 'cp862', 'cp863',
                         'cp864', 'cp865', 'cp866', 'cp869', 'cp874',
                         'cp875', 'cp932', 'cp949', 'cp950', 'cp1006',
                         'cp1026', 'cp1140', 'cp1250', 'cp1251', 'cp1252',
                         'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257',
                         'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr',
                         'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp',
                         'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext',
                         'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4',
                         'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9',
                         'iso8859_10', 'iso8859_11', 'iso8859_13', 'iso8859_14', 'iso8859_15',
                         'iso8859_16', 'johab', 'koi8_r', 'koi8_u', 'mac_cyrillic',
                         'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish',
                         'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_32',
                         'utf_32_be', 'utf_32_le', 'utf_16', 'utf_16_be', 'utf_16_le',
                         'utf_7', 'utf_8', 'utf_8_sig']
    while True:
        try:
            print()
            print(statement)
            for j, i in enumerate(basic_encoders):
                if j != len(basic_encoders) - 1:
                    print(str(j) + ": to use " + str(i) + "")
                else:
                    print(str(j) + ": to see all possible encoders.")
            encoder = basic_encoders[int(input("Enter Selection: "))]
        except ValueError:
            print("Input must be integer between 0 and " + str(len(basic_encoders)))
            continue
        else:
            break

    if encoder == 'See All Encoders':
        while True:
            try:
                print()
                print(statement)
                for j, i in enumerate(advanced_encoders):
                    print(str(j) + ": to use " + str(i) + "")
                encoder = advanced_encoders[int(input("Enter Selection: "))]
            except ValueError:
                print("Input must be integer between 0 and " + str(len(advanced_encoders)))
                continue
            else:
                break
    print()
    return encoder

def open_file(file_in, encoder, delimination):
    try:
        data = pd.read_csv(file_in, low_memory=False, encoding=encoder, delimiter=delimination)
        print("Opened file using encoder: " + encoder)

    except UnicodeDecodeError:
        print("Encoder Error for: " + encoder)
        return "Encode Error"
    return data
