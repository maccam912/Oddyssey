# http://mewo2.com/notes/naming-language/
# Note: This is naming language algorithm implemented by following Martin O'Leary's instructions in his webpage.

import random

consonants = {'Minimal' :               {'p','t','k','m','n','l','s'},
              'English-ish' :           {'p','t','k','b','d','g','m','n','l','r','s','ʃ','z','ʒ','ʧ'},
              'Pirahã (very simple)' :  {'p','t','k','m','n','h'},
              'Hawaiian-ish' :          {'h','k','l','m','n','p','w','ʔ'},
              'Greenlandic-ish' :       {'p','t','k','q','v','s','g','r','m','n','ŋ','l','j'},
              'Arabic-ish' :            {'t','k','s','ʃ','d','b','q','ɣ','x','m','n','l','r','w','j'},
              'Arabic-lite' :           {'t','k','d','g','m','n','s','ʃ'},
              'English-lite':           {'p','t','k','b','d','g','m','n','s','z','ʒ','ʧ','h','j','w'}
              }

vowels = {'Standard 5-vowel' :      {'a','e','i','o','u'},
           '3-vowel a i u' :        {'a','i','u'},
           'Extra A E I' :          {'a','e','i','o','u','A','E','I'},
           'Extra U' :              {'a','e','i','o','u','U'},
           '5-vowel a i u A I' :    {'a','i','u','A','I'},
           '3-vowel e o u' :        {'e','o','u'},
           'Extra A O U' :          {'a','e','i','o','u','A','O','U'}
           }

sibilants = {'Just s' :     {'s'},
             's ʃ' :       {'s','ʃ'},
             's ʃ f' :     {'s','ʃ','f'}
             }

liquids = {'r l' :      {'r','l'},
           'Just r' :   {'r'},
           'Just l' :   {'l'},
           'w j' :      {'w','j'},
           'r l w j' :  {'r','l','w','j'}
           }

finals = {'m n' : {'m','n'},
          's k' : {'s','k'},
          'm n ŋ' : {'m','n','ŋ'},
          's ʃ z ʒ' : {'s','ʃ','z','ʒ'}
          }

structures = {'CVC', 'CVV?C', 'CVVC?', 'CVC?', 'CV', 'VC', 'CVF', 'C?VC', 'CVF?',\
              'CL?VC', 'CL?VF', 'S?CVC', 'S?CVF', 'S?CVC?', 'C?VF', 'C?VC?', 'C?VF?',\
              'C?L?VC', 'VC', 'CVL?C?', 'C?VL?C', 'C?VLC?'}

restrictions = {'None', 'Double sounds', 'Double sounds and hard clusters'}

vowel_orthography_set = {'Default' :        {'A': 'á', 'E': 'é', 'I': 'í', 'O': 'ó', 'U': 'ú'},
                         'Ácutes' :         {},
                         'Ümlauts' :        {'A': 'ä', 'E': 'ë', 'I': 'ï', 'O': 'ö', 'U': 'ü'},
                         'Welsh' :          {'A': 'â', 'E': 'ê', 'I': 'y', 'O': 'ô',  'U': 'w'},
                         'Diphthongs' :     {'A': 'au', 'E': 'ei', 'I': 'ie', 'O': 'ou', 'U': 'oo'},
                         'Doubles' :        {'A': 'aa', 'E': 'ee', 'I': 'ii', 'O': 'oo', 'U': 'uu'}
                         }

consonant_orthography_set = {'Default' :            {'ʃ': 'sh', 'ʒ': 'zh', 'ʧ': 'ch', 'ʤ': 'j', 'ŋ': 'ng', 'j': 'y', 'x': 'kh', 'ɣ': 'gh', 'ʔ': '`',},
                             'Slavic' :             {'ʃ': 'š', 'ʒ': 'ž', 'ʧ': 'č', 'ʤ': 'ǧ', 'j': 'j'},
                             'German' :             {'ʃ': 'sch', 'ʒ': 'zh', 'ʧ': 'tsch', 'ʤ': 'dz', 'j': 'j', 'x': 'ch'},
                             'French' :             {'ʃ': 'ch', 'ʒ': 'j', 'ʧ': 'tch', 'ʤ': 'dj', 'x': 'kh'},
                             'Chinese (pinyin)' :   {'ʃ': 'x', 'ʧ': 'q', 'ʤ': 'j'}
                             }

def generate_syllable(consonant_set, vowel_set, sibilant_set, liquid_set, final_set, structure, restriction, consonant_orthography_type, vowel_orthography_type):
    regenerate = True
    while(regenerate == True):        
        structure_list = phonotactics(structure)
        selected_structure = structure_list[random.randint(0, len(structure_list) - 1)]
        # Generate syllable according to structure
        syllable = ''
        for i in range(len(selected_structure)):
            if selected_structure[i] == 'C':
                syllable += random.choice(list(consonant_set))
            elif selected_structure[i] == 'V':
                syllable += random.choice(list(vowel_set))
            elif selected_structure[i] == 'S':
                syllable += random.choice(list(sibilant_set))
            elif selected_structure[i] == 'L':
                syllable += random.choice(list(liquid_set))
            elif selected_structure[i] == 'F':
                syllable += random.choice(list(final_set))
        # Check restriction criteria
        regenerate = check_regenerate_restriction(syllable, restriction, consonant_set)
    # Orthography
    syllable = orthography(syllable, selected_structure, consonant_orthography_type, vowel_orthography_type)    
    return syllable

def phonotactics(structure):
    structure_code = split_optional_structure(structure)
    structure_list = structure_code.split(',')
    return structure_list[:-1]

def split_optional_structure(structure):
    structure_code = ''
    if '?' in structure:
        structure_1 = structure[:structure.index('?')] + structure[structure.index('?') + 1:]
        structure_2 = structure[:structure.index('?')-1] + structure[structure.index('?') + 1:]
        structure_code += split_optional_structure(structure_1)
        structure_code += split_optional_structure(structure_2)
    else:
        structure_code += (structure + ',')
    return structure_code

def orthography(syllable, selected_structure, consonant_orthography_type, vowel_orthography_type):
    output = ''
    for i in range(len(syllable)):
        if selected_structure[i] == 'C' or selected_structure[i] == 'S' or selected_structure[i] == 'F':
            output += phoneme_orthography(syllable[i], consonant_orthography_type, consonant_orthography_set)
        elif selected_structure[i] == 'V':
            output += phoneme_orthography(syllable[i], vowel_orthography_type, vowel_orthography_set)
        else:
            output += syllable[i]
    return output

def phoneme_orthography(phoneme, orthography_type, orthography_set):
    if orthography_type in orthography_set.keys():
        lookup_dict = orthography_set[orthography_type]
        if phoneme in lookup_dict.keys():
            phoneme = lookup_dict[phoneme]
        elif phoneme in orthography_set['Default']:
            phoneme = orthography_set['Default'][phoneme]
    return phoneme

def check_regenerate_restriction(syllable, restriction, consonant_set):
    if restriction == 'None':
        return False
    elif restriction == 'Double sounds':
        return check_double_sound(syllable, consonant_set)       
    elif restriction == 'Double sounds and hard clusters':
        return (check_double_sound(syllable, consonant_set) or check_hard_clusters(syllable)) 

def check_double_sound(syllable, consonant_set):
    for i in range(len(syllable)):
        if syllable.count(syllable[i]) > 1 and syllable[i] in consonant_set:
            if i != len(syllable) -1 and syllable[i] == syllable[i+1]:
                return True
    return False

def check_hard_clusters(syllable):
    hard_cluster_cases = ['ss','sʃ','ʃs','ʃʃ','fs','fʃ','rl','lr','ll','rr']
    for cluster in hard_cluster_cases:
        if cluster in syllable:
            return True
    return False

def generate_morpheme(language_style, num_of_syllables):
    morpheme = ''
    for i in range(num_of_syllables):
        morpheme += generate_syllable(consonant_set=consonants[language_style['consonant']], vowel_set=vowels[language_style['vowel']], \
                                  sibilant_set=sibilants[language_style['sibilant']], liquid_set=liquids[language_style['liquid']], \
                                  final_set=finals[language_style['final']], structure=language_style['structure'], restriction=language_style['restriction'], \
                                  consonant_orthography_type=language_style['consonant_orthography_type'], vowel_orthography_type=language_style['vowel_orthography_type'])
    return morpheme

def geneate_morpheme_pool(language_style, pool_size, min_syllable=1, max_syllable=2):
    pool = set()
    for i in range(pool_size):
        num_of_syllables = random.randint(min_syllable, max_syllable)
        pool.add(generate_morpheme(language_style, num_of_syllables))    
    return pool

def generate_name_from_morpheme_pool(generic_morpheme_pool, meaningful_morpheme_pool, connection_morpheme_pool, min_word=1, max_word=3):
    name = ''
    connection_used = False
    num_of_word = random.randint(min_word, max_word)    
    for i in range(num_of_word):        
        if i > 0 and i != num_of_word - 1 and not connection_used:
            connect_prob = random.random()
            if connect_prob > 0.5:
                name += random.choice(list(connection_morpheme_pool)) + ' '
                connection_used = True
        else:
            prob = random.random()
            if prob > 0.5:
                word = ( random.choice(list(generic_morpheme_pool)) + random.choice(list(meaningful_morpheme_pool)))
                name += word[0].upper() + word[1:] + ' '
            else:
                word = ( random.choice(list(meaningful_morpheme_pool)) + random.choice(list(generic_morpheme_pool)))
                name += word[0].upper() + word[1:] + ' '
    return name[:-1]

if __name__ == '__main__':    
    consonant = random.choice(list(consonants.keys()))
    vowel = random.choice(list(vowels.keys()))
    sibilant = random.choice(list(sibilants.keys()))
    liquid = random.choice(list(liquids.keys()))
    final = random.choice(list(finals.keys()))
    structure = random.choice(list(structures))
    restriction = random.choice(list(restrictions))
    consonant_orthography_type = random.choice(list(consonant_orthography_set.keys()))
    vowel_orthography_type = random.choice(list(vowel_orthography_set.keys()))
    
    language_style = {'consonant' :                     consonant,
                      'vowel' :                         vowel,
                      'sibilant' :                      sibilant,
                      'liquid' :                        liquid,
                      'final' :                         final,
                      'structure' :                     structure,
                      'restriction' :                   restriction,
                      'consonant_orthography_type' :    consonant_orthography_type,
                      'vowel_orthography_type' :        vowel_orthography_type}
    
    generic_morpheme_pool = geneate_morpheme_pool(language_style, pool_size=10, min_syllable=1, max_syllable=1)
    city_morpheme_pool = geneate_morpheme_pool(language_style, pool_size=3, min_syllable=1, max_syllable=1)
    connection_morpheme_pool = geneate_morpheme_pool(language_style, pool_size=2, min_syllable=1, max_syllable=1)
    
    name = generate_name_from_morpheme_pool(generic_morpheme_pool, city_morpheme_pool, connection_morpheme_pool, min_word=1, max_word=3)
    print(name)