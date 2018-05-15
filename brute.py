#!/usr/local/bin/python3
import sys
from lib.keystore import from_bip39_seed
from lib.storage import WalletStorage
from lib.wallet import Standard_Wallet
from itertools import permutations

seed_words = ''
address = ''
start_index = 1250
dictionary = ''
attack_type = 2 #[0=>'pin_sequential', 1=>'pin_permutation', 2=>'dictionary']

def _create_standard_wallet(ks):
    gap_limit = 1  # make tests run faster
    store = WalletStorage('if_this_exists_mocking_failed_648151893')
    store.put('keystore', ks.dump())
    store.put('gap_limit', gap_limit)
    w = Standard_Wallet(store)
    w.synchronize()
    return w


def check_bip39_seed_bip49_p2sh_segwit(password, index):
    ks = from_bip39_seed(seed_words, password, "m/49'/0'/0'")
    w = _create_standard_wallet(ks)
    addr = w.get_receiving_addresses()[0]

    if (addr == address):
        print(index + '\t PASSWORD FOUND: ' + password)
        return True
    else:
        print(index + '\t' + str(addr) + '\t' + password)
        return False

def readDic (dic):
    with open(dic) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

if (attack_type == 0):
    for i in range(0, 9999):
        pwd = str(i).zfill(4)
        print()
        # check_bip39_seed_bip49_p2sh_segwit(str(pwd),str(i))

elif(attack_type == 1):
    pin = '1 2 3 4 5 6 7 8 9'
    words = pin.split()
    i = 0
    for p in permutations(words, 9):
        i = i + 1
        if (i < start_index):
            continue
        pwd = "".join(str(x) for x in p)
        check_bip39_seed_bip49_p2sh_segwit(str(pwd), str(i))

elif(attack_type == 2):
    w = readDic('bip39list.txt')
    for i in range(0, 2048):
        check_bip39_seed_bip49_p2sh_segwit(str(w[i]), str(i))
