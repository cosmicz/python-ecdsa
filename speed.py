import six
import timeit
from ecdsa.curves import curves

def do(setup_statements, statement):
    # extracted from timeit.py
    t = timeit.Timer(stmt=statement,
                     setup="\n".join(setup_statements))
    # determine number so that 0.2 <= total time < 2.0
    for i in range(1, 10):
        number = 10**i
        x = t.timeit(number)
        if x >= 0.2:
            break
    return x / number

prnt_form = ("{name:>10}{sep:1} {siglen:>6} {keygen:>9{form}}{unit:1} "
    "{keygen_inv:>9{form_inv}} {sign:>9{form}}{unit:1} "
    "{sign_inv:>9{form_inv}} {verify:>9{form}}{unit:1} "
    "{verify_inv:>9{form_inv}}")

print(prnt_form.format(siglen="siglen", keygen="keygen", keygen_inv="keygen/s",
                       sign="sign", sign_inv="sign/s", verify="verify",
                       verify_inv="verify/s", name="", sep="", unit="",
                       form="", form_inv=""))

for curve in [i.name for i in curves]:
    S1 = "import six; from ecdsa import SigningKey, %s" % curve
    S2 = "sk = SigningKey.generate(%s)" % curve
    S3 = "msg = six.b('msg')"
    S4 = "sig = sk.sign(msg)"
    S5 = "vk = sk.get_verifying_key()"
    S6 = "vk.verify(sig, msg)"
    # We happen to know that .generate() also calculates the
    # verifying key, which is the time-consuming part. If the code
    # were changed to lazily calculate vk, we'd need to change this
    # benchmark to loop over S5 instead of S2
    keygen = do([S1], S2)
    sign = do([S1,S2,S3], S4)
    verf = do([S1,S2,S3,S4,S5], S6)
    import ecdsa
    c = getattr(ecdsa, curve)
    sig = ecdsa.SigningKey.generate(c).sign(six.b("msg"))
    print(prnt_form.format(
        name=curve, sep=":", siglen=len(sig), unit="s", keygen=keygen,
        keygen_inv=1.0/keygen, sign=sign, sign_inv=1.0/sign, verify=verf,
        verify_inv=1.0/verf, form=".5f", form_inv=".2f"))
