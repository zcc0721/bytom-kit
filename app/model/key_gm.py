import hmac
import hashlib
from gmssl import sm2, func

# get_gm_root_xprv create rootxprv from seed
# seed_str length is 512 bits.
# root_xprv length is 512 bits.
# You can get more test data from: https://gist.github.com/zcc0721/8bfc1e1c92b7cd9f00743d6878097809
# test data 1:
#   seed_str: ecc2bbb6c0492873cdbc81edf56bd896d3b644047879840e357be735b7fa7b6f4af1be7b8d71cc649ac4ca3816f9ccaf11bf49f4effb845f3c19e16eaf8bfcda
#   root_xprv_str: a61d6b741b0e74b8d0836ac22b675bbf8e108148ef018d1b000aef1a899a136bd316c0f59e7333520ae1a429504073b2773869e95aa95bb3a4fa0ec76744025c
# test data 2:
#   seed_str: afa3a86bbec2f40bb32833fc6324593824c4fc7821ed32eac1f762b5893e56745f66a6c6f2588b3d627680aa4e0e50efd25065097b3daa8c6a19d606838fe7d4
#   root_xprv_str: 302a25c7c0a68a83fa043f594a2db8b44bc871fced553a8a33144b31bc7fb88887c9e75915bb6ba3fd0b9f94a60b7a5897ab9db6a48f888c2559132dba9152b0
# test data 3:
#   seed_str: b435f948bd3748ede8f9d6f59728d669939e79c6c885667a5c138e05bbabde1de0dcfcbe0c6112022fbbf0da522f4e224a9c2381016380688b51886248b3156f
#   root_xprv_str: 6532adeb967ac5ccbf988cf8190817bf9040c8cfd9cdfe3d5e400effb29469e6d478b61cc6be936f367ae769eb1dc65c473ee73cac2eb43cf6d5e7c62b7f0062
def get_gm_root_xprv(seed_str):
    hc_str = hmac.HMAC(b'Root', bytes.fromhex(seed_str), digestmod=hashlib.sha512).hexdigest()
    root_xprv_str = hc_str
    return {
        "root_xprv": root_xprv_str
    }


# get_gm_xpub derives new xpub from xprv
# xprv length is 64 bytes.
# xpub length is 65 bytes.
# You can get more test data from: https://gist.github.com/zcc0721/9e5761e6a924cce3aa7cf7f72721218a
# test data 1:
#   xprv_str: c003f4bcccf9ad6f05ad2c84fa5ff98430eb8e73de5de232bc29334c7d074759d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c
#   xpub_str: 02476044353971ae0ed41cba76f27d0bd2e09d09db5c238bb74f69569bf343f742d513bc370335cac51d77f0be5dfe84de024cfee562530b4d873b5f5e2ff4f57c
# test data 2:
#   xprv_str: 36667587de27eec684fc4b222276f22a24d9a82e947ee0119148bedd4dec461dd4e1b1d95dfb0f78896677ea1026af7510b41fabd3bd5771311c0cb6968337b2
#   xpub_str: 0396a36cd902db56eca016c213a8ac25de35a7afd78061351f1898529f0956c22ed4e1b1d95dfb0f78896677ea1026af7510b41fabd3bd5771311c0cb6968337b2
# test data 3:
#   xprv_str: 74a49c698dbd3c12e36b0b287447d833f74f3937ff132ebff7054baa18623c35a705bb18b82e2ac0384b5127db97016e63609f712bc90e3506cfbea97599f46f
#   xpub_str: 03cafbdedea4a639d31fe4c257f1bb58303359be1a00b9f90b5c605f57e4308ed1a705bb18b82e2ac0384b5127db97016e63609f712bc90e3506cfbea97599f46f
def get_gm_xpub(xprv_str):
    private_key_int = int(xprv_str[:64], 16)
    sm2_crypt = sm2.CryptSM2(private_key=xprv_str[:64], public_key="")
    public_key_str = sm2_crypt._kg(private_key_int, sm2.default_ecc_table['g'])
    pc = '0' + str(int(public_key_str[-1], 16) % 2 + 2)
    xpub_str = pc + public_key_str[:64] + xprv_str[64:]
    return {
        "xpub": xpub_str
    }


# get_gm_xprv create expanded private key from xprv
# You can get more test data from: https://gist.github.com/zcc0721/ef0bf2e69f5e92b29d716981f2a8fe7d
# test data 1:
#   xprv_str: 406c82307bf7978d17f3ecfeea7705370e9faef2027affa86c8027c6e11a8a50e231e65bd97048850ae6c39d0f46b63ae70aa24f5aac7877727c430c2201e6d6
#   expanded_private_key_str_xprv: 406c82307bf7978d17f3ecfeea7705370e9faef2027affa86c8027c6e11a8a50d828bf44b1a109c2bbb4c72685858e2f2ab8b405beef1e4ecc12d1ed8511e8eb
# test data 2:
#   xprv_str: 6032adeb967ac5ccbf988cf8190817bf9040c8cfd9cdfe3d5e400effb2946946d478b61cc6be936f367ae769eb1dc65c473ee73cac2eb43cf6d5e7c62b7f0062
#   expanded_private_key_str_xprv: 6032adeb967ac5ccbf988cf8190817bf9040c8cfd9cdfe3d5e400effb2946946ddbb71e7a76595c6bc24937d76085d24315713764cbdf1364ab9091953009cd8
# test data 3:
#   xprv_str: 509a095ad862322641b8d66e84561aae1d4816045167e2c4dfadf464928e114300c0a162d41c0cdf196d61f4492f546e50bfff253b9d5d930d1bb89197cd333d
#   expanded_private_key_str_xprv: 509a095ad862322641b8d66e84561aae1d4816045167e2c4dfadf464928e11432787f5e10f9598f80fb41e4a648b609463c06e625641366f3279658b2b0f5268
def get_gm_xprv(xprv_str):
    hc_str = hmac.HMAC(b'Expand', bytes.fromhex(xprv_str), digestmod=hashlib.sha512).hexdigest()
    expanded_private_key_str = xprv_str[:64] + hc_str[64:]
    return {
        "expanded_private_key": expanded_private_key_str
    }


# get_gm_public_key create 33 bytes public key from xpub
# xpub length is 65 bytes.
# You can get more test data from: https://gist.github.com/zcc0721/e159677bf776fe0209bca5b890cb87c3
# test data 1:
#   xpub_str: 03c74f3a946940d43e0f8c6da40680c0078e6e1008ca6ea869d57536c31b7ede20adc168c3698fa538fa587c4e519d1eb7a2593f178bfe0c93890a0f09e1634607
#   public_key_str: 03c74f3a946940d43e0f8c6da40680c0078e6e1008ca6ea869d57536c31b7ede20
# test data 2:
#   xpub_str: 02914d51fcc3b90a87ffe3424995a9db8757a9d67812edd85207c47edc9f7f34e368684ae4d706f68c710fe1dbd20d73a8faaaf34966678a5d58486ac193a851ca
#   public_key_str: 02914d51fcc3b90a87ffe3424995a9db8757a9d67812edd85207c47edc9f7f34e3
# test data 3:
#   xpub_str: 03603b2eb079257513d253a92ad45ce5ef12cc285dd8c13fc77c95844468f5eb4482f33c577c3a71ac733136b17d68b65a184b225431ab658555735e436fdb13e6
#   public_key_str: 03603b2eb079257513d253a92ad45ce5ef12cc285dd8c13fc77c95844468f5eb44
def get_gm_public_key(xpub_str):
    public_key_str = xpub_str[:66]
    return {
        "public_key": public_key_str
    }
