
import sys
import jmbitcoin as btc
from jmbase import jmprint
from jmclient import (jm_single, get_p2pk_vbyte, get_p2sh_vbyte,
                      BTCEngine, TYPE_P2PKH, TYPE_P2SH_P2WPKH,
                      BTC_P2PKH, BTC_P2SH_P2WPKH)
from jmbase.support import EXIT_FAILURE


def quit(parser, errmsg): #pragma: no cover
    parser.error(errmsg)
    sys.exit(EXIT_FAILURE)

def get_utxo_info(upriv):
    """Verify that the input string parses correctly as (utxo, priv)
    and return that.
    """
    try:
        u, priv = upriv.split(',')
        u = u.strip()
        priv = priv.strip()
        txid, n = u.split(':')
        assert len(txid)==64
        assert len(n) in range(1, 4)
        n = int(n)
        assert n in range(256)
    except:
        #not sending data to stdout in case privkey info
        jmprint("Failed to parse utxo information for utxo", "error")
        raise
    try:
        raw, keytype = BTCEngine.wif_to_privkey(priv)
        assert keytype in [TYPE_P2PKH, TYPE_P2SH_P2WPKH]
    except:
        jmprint("failed to parse privkey, make sure it's WIF compressed format.", "error")
        raise
    return u, priv
    
def validate_utxo_data(utxo_datas, retrieve=False, segwit=False):
    """For each txid: N, privkey, first
    convert the privkey and convert to address,
    then use the blockchain instance to look up
    the utxo and check that its address field matches.
    If retrieve is True, return the set of utxos and their values.
    If segwit is true, assumes a p2sh wrapped p2wpkh, i.e.
    native segwit is NOT currently supported here. If segwit
    is false, p2pkh is assumed.
    """
    results = []
    for u, priv in utxo_datas:
        jmprint('validating this utxo: ' + str(u), "info")
        rawpriv, keytype = BTCEngine.wif_to_privkey(priv)
        if keytype == TYPE_P2PKH:
            walletcls = BTC_P2PKH
        elif keytype == TYPE_P2SH_P2WPKH:
            walletcls = BTC_P2SH_P2WPKH
        else:
            assert False, "invalid key type"
        addr = walletcls.privkey_to_address(rawpriv)
        jmprint('claimed address: ' + addr, "info")
        res = jm_single().bc_interface.query_utxo_set([u])
        if len(res) != 1 or None in res:
            jmprint("utxo not found on blockchain: " + str(u), "error")
            return False
        if res[0]['address'] != addr:
            jmprint("privkey corresponds to the wrong address for utxo: " + str(u), "error")
            jmprint("blockchain returned address: {}".format(res[0]['address']), "error")
            jmprint("your privkey gave this address: " + addr, "error")
            return False
        if retrieve:
            results.append((u, res[0]['value']))
    jmprint('all utxos validated OK', "success")
    if retrieve:
        return results
    return True
