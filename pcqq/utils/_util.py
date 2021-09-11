import random
import hashlib

def GetRandomBin(length: int)->bytes:
    '''生成指定长度的随机字节集'''
    dst = [random.randint(0,255).to_bytes(1,"big") for _ in range(length)]
    return b''.join(dst)

def HashMD5(src: bytes)->bytes:
    '''将字节集编码为md5 16bit字节集'''
    return hashlib.md5(src).digest()

def Bin2HexTo(src: bytes)->str:
    '''字节集转十六进制文本'''
    s = " ".join([hex(b)[2:].upper() for b in src])
    return s

def Hex2Bin(s: str)->bytes:
    '''十六进制文本转字节集'''
    return bytes([int("0x"+i,16) for i in s.split(" ")])

def GroupToGid(groupId:int)->int:
    '''群号转GID'''
    group = str(groupId)
    left = int(group[0:-6])
    if left >= 0 and left <= 10:
        right = group[-6:]
        gid = str(left + 202) + right
    elif left >= 11 and left <= 19:
        right = group[-6:]
        gid = str(left + 469) + right
    elif left >= 20 and left <= 66:
        left = int(str(left)[0:1])
        right = group[-7:]
        gid = str(left + 208) + right
    elif left >= 67 and left <= 156:
        right = group[-6:]
        gid = str(left + 1943) + right
    elif left >= 157 and left <= 209:
        left = int(str(left)[0:2])
        right = group[-7:]
        gid = str(left + 199) + right
    elif left >= 210 and left <= 309:
        left = int(str(left)[0:2])
        right = group[-7:]
        gid = str(left + 389) + right
    elif left >= 310 and left <= 335:
        left = int(str(left)[0:2])
        right = group[-7:]
        gid = str(left + 349) + right
    elif left >= 336 and left <= 386:
        left = int(str(left)[0:3])
        right = group[-6:]
        gid = str(left + 2265) + right
    elif left >= 387 and left <= 499:
        left = int(str(left)[0:3])
        right = group[-6:]
        gid = str(left + 3490) + right
    elif left >= 500:
        return int(group)
    return int(gid)

def GidToGroup(gid:int)->int:
    '''GID转群号'''
    gid = str(gid)
    if int(gid[0:3]) >= 500:
        return int(gid)
    left = int(gid[0:-6])

    if left == 202:
        right = gid[-6:]
        group = int(right)
    elif left >= 203 and left <= 212:
        right = gid[-6:]
        group = int(str(left-202) + right)
    elif left >= 480 and left <= 488:
        right = gid[-6:]
        group = int(str(left-469) + right)
    elif left >= 2010 and left <= 2099:
        right = gid[-6:]
        group = int(str(left-1943) + right)
    elif left >= 2100 and left <= 2146:
        left = int(str(left)[0:3])
        right = gid[-7:]
        group = int(str(left-208) + right)
    elif left >= 2147 and left <= 2199:
        left = int(str(left)[0:3])
        right = gid[-7:]
        group = int(str(left-199) + right)
    elif left >= 2601 and left <= 2651:
        left = int(str(left)[0:4])
        right = gid[-6:]
        group = int(str(left-2265) + right)
    elif left >= 3800 and left <= 3989:
        left = int(str(left)[0:3])
        right = gid[-7:]
        group = int(str(left-349) + right)
    elif left >= 4100 and left <= 4199:
        left = int(str(left)[0:3])
        right = gid[-7:]
        group = int(str(left-389) + right)
    else:
        group = 0
    
    return group