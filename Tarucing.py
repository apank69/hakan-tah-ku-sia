import time

import os

P = 2**256 - 2**32 - 977

N = 115792089237316195423570985008687907852837564279074904382605163141518161494337

A = 0

B = 7

Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240

Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424

G = (Gx, Gy)

def getG():

    return G

def inv(a, n):

    if a == 0:

        return 0

    lm, hm = 1, 0

    low, high = a % n, n

    while low > 1:

        r = high//low

        nm, new = hm-lm*r, high-low*r

        lm, low, hm, high = nm, new, lm, low

    return lm % n

def isinf(p):

    return p[0] == 0 and p[1] == 0

def to_jacobian(p):

    o = (p[0], p[1], 1)

    return o

def jacobian_double(p):

    if not p[1]:

        return (0, 0, 0)

    ysq = (p[1] ** 2) % P

    S = (4 * p[0] * ysq) % P

    M = (3 * p[0] ** 2 + A * p[2] ** 4) % P

    nx = (M**2 - 2 * S) % P

    ny = (M * (S - nx) - 8 * ysq ** 2) % P

    nz = (2 * p[1] * p[2]) % P

    return (nx, ny, nz)

def jacobian_add(p, q):

    if not p[1]:

        return q

    if not q[1]:

        return p

    U1 = (p[0] * q[2] ** 2) % P

    U2 = (q[0] * p[2] ** 2) % P

    S1 = (p[1] * q[2] ** 3) % P

    S2 = (q[1] * p[2] ** 3) % P

    if U1 == U2:

        if S1 != S2:

            return (0, 0, 1)

        return jacobian_double(p)

    H = U2 - U1

    R = S2 - S1

    H2 = (H * H) % P

    H3 = (H * H2) % P

    U1H2 = (U1 * H2) % P

    nx = (R ** 2 - H3 - 2 * U1H2) % P

    ny = (R * (U1H2 - nx) - S1 * H3) % P

    nz = (H * p[2] * q[2]) % P

    return (nx, ny, nz)

def from_jacobian(p):

    z = inv(p[2], P)

    return p[0] * z**2 % P, p[1] * z**3 % P

def jacobian_multiply(a, n):

    if a[1] == 0 or n == 0:

        return (0, 0, 1)

    if n == 1:

        return a

    if n < 0 or n >= N:

        return jacobian_multiply(a, n % N)

    if (n % 2) == 0:

        return jacobian_double(jacobian_multiply(a, n//2))

    if (n % 2) == 1:

        return jacobian_add(jacobian_double(jacobian_multiply(a, n//2)), a)

def fast_multiply(a, n):

    return from_jacobian(jacobian_multiply(to_jacobian(a), n))

def fast_add(a, b):

    return from_jacobian(jacobian_add(to_jacobian(a), to_jacobian(b)))

# Functions for handling pubkey and privkey formats

def add_pubkeys(p1, p2):

    return fast_add(p1,p2)

def add_privkeys(p1, p2):

    return p1 + p2 % N

def mul_privkeys(p1, p2):

    return p1 *p2 % N

def multiply(pubkey, privkey):

    if not isinf(pubkey) and (pubkey[0]**3+B-pubkey[1]*pubkey[1]) % P != 0:

        raise Exception("Point not on curve")

    return fast_multiply(pubkey, privkey)

def divide(pubkey, privkey):

    factor = inv(privkey, N)

    return multiply(pubkey, factor)

def neg_pubkey(pubkey):

    return pubkey[0],P-pubkey[1] % P

def neg_privkey(privkey):

    privkey = privkey

    return N - privkey % N

def subtract_pubkeys(p1, p2):

    k2 = p2

    return fast_add(p1, (k2[0], (P - k2[1]) % P))

def subtract_privkeys(p1, p2):

    k2 = p2

    return p1- k2 % N

aa=(55073920805980091370333867208788820467743546980766790997044541979511098533584, 82529960212721529776690183538437684871955847274552233572796862643478055552180)

aq=(63004655751848499058589887215149057167805706207141784701705408548476267919372, 33776887358425213876727286236887696644549240079971817446727643228044518554934)

start = time.time()

konter = 0

while(konter<N):

    Waktu = float(time.time() - start)  

    konter = konter + 1

    a1=multiply(aq,konter)

    a2=subtract_pubkeys(aa,a1)

    if a2==aq:

        print("TARGET_KAPANGGIH:NEGATIV", Waktu ,"Detik")

        print("ADDRESS :a4 ",a2)

        print("KONTER : ", konter)

        break

    else:

        print(os.linesep + "Waktu Berjalan: %.4f Detik" % Waktu)   

",a2)

        print("KONTER : ", konter)

        break

    else:

        print(os.linesep + "Waktu Berjalan: %.4f Detik" % Waktu)   

