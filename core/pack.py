# 组装协议包
from .utils import *
from time import time
from .client import NetClient


class QQ_PACK():
    def __init__(self):
        self.Client = NetClient()
        self.QQ = qqStruct.QQ_Struct()
        self.QQ.PublicKey = util.Hex2Bin("03 94 3D CB E9 12 38 61 EC F7 AD BD E3 36 91 91 07 01 50 BE 50 39 1C D3 32")
        self.QQ.ShareKey = util.Hex2Bin("FD 0B 79 78 31 E6 88 54 FC FA EA 84 52 9C 7D 0B")
        self.QQ.RandHead16 = util.GetRandomBin(16)

    def pack_0825(self,packType: int) -> bytes:
        '''
        :param packType: 取二维码(1)/二维码登录(2)
        '''
        data = b''
        tea = qqTea.Tea()
        pack = packEncrypt.PackEncrypt()
        self.QQ.RandHead16 = util.GetRandomBin(16)

        if packType == 1:
            pack.SetHex("00 18 00 16 00 01 00 00 04 4C 00 00 00 01 00 00 15 51 00 00 00 00 00 00 00 00 00 04 00 0C 00 00 00 08 71 72 5F 6C 6F 67 69 6E 03 09 00 08 00 01 00 00 00 00 00 04 01 14 00 1D")
            pack.SetHex("01 02")
            pack.SetShort(len((self.QQ.PublicKey)))
            pack.SetBin(self.QQ.PublicKey)
            data = tea.Encrypt(pack.GetAll(),self.QQ.RandHead16)

            pack.Empty()
            pack.SetHex("02 36 39")
            pack.SetHex("08 25")
            pack.SetBin(util.GetRandomBin(2))
            pack.SetHex("00 00 00 00 03 00 00 00 01 01 01 00 00 67 B7 00 00 00 00")
            pack.SetBin(self.QQ.RandHead16)
            pack.SetBin(data)
            pack.SetHex("03")
            data = pack.GetAll()
        elif packType == 2:
            pack.SetHex("00 18 00 16 00 01 00 00 04 4C 00 00 00 01 00 00 15 51")
            pack.SetBin(self.QQ.BinQQ)
            pack.SetHex("00 00 00 00 03 09 00 08 00 01")
            pack.SetBin(self.QQ.ConnectSeverIp)
            pack.SetHex("00 01 00 36 00 12 00 02 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 14 00 1D")
            pack.SetHex("01 02")
            pack.SetShort(len(self.QQ.PublicKey))
            pack.SetBin(self.QQ.PublicKey)
            data = tea.Encrypt(pack.GetAll(),self.QQ.RandHead16)

            pack.Empty()
            pack.SetHex("02 36 39")
            pack.SetHex("08 25")
            pack.SetBin(util.GetRandomBin(2))
            pack.SetBin(self.QQ.BinQQ)
            pack.SetHex("03 00 00 00 01 01 01 00 00 67 B7 00 00 00 00")
            pack.SetBin(self.QQ.RandHead16)
            pack.SetBin(data)
            pack.SetHex("03")
            data = pack.GetAll()
        return data

    def pack_0818(self) -> bytes:
        '''获取二维码'''
        tea = qqTea.Tea()
        pack = packEncrypt.PackEncrypt()
        self.QQ.RandHead16 = util.GetRandomBin(16)

        pack.Empty()
        pack.SetHex("00 19 00 10 00 01 00 00 04 4C 00 00 00 01 00 00 15 51 00 00 01 14 00 1D")
        pack.SetHex("01 02")
        pack.SetShort(len(self.QQ.PublicKey))
        pack.SetBin(self.QQ.PublicKey)
        pack.SetHex("03 05 00 1E 00 00 00 00 00 00 00 05 00 00 00 04 00 00 00 00 00 00 00 48 00 00 00 02 00 00 00 02 00 00")
        data = tea.Encrypt(pack.GetAll(),self.QQ.RandHead16)

        pack.Empty()
        pack.SetHex("02 36 39")
        pack.SetHex("08 18")
        pack.SetBin(util.GetRandomBin(2))
        pack.SetHex("00 00 00 00 03 00 00 00 01 01 01 00 00 67 B7 00 00 00 00")
        pack.SetBin(self.QQ.RandHead16)
        pack.SetBin(data)
        pack.SetHex("03")
        data = pack.GetAll()

        return data

    def pack_0819(self,codeId: str, login: bool) -> bytes:
        '''
        检查二维码状态
        :param codeId: 二维码ID
        :param login: 授权登录(True)/取二维码验证状态(False)
        '''

        tea = qqTea.Tea()
        pack = packEncrypt.PackEncrypt()
        self.QQ.RandHead16 = util.GetRandomBin(16)

        pack.SetHex("00 19 00 10 00 01 00 00 04 4C 00 00 00 01 00 00 15 51 00 00 03 01 00 22")

        pack.SetShort(len(codeId))
        pack.SetStr(codeId)
        if login:
            pack.SetHex("03 14 00 02 00 00")
        data = tea.Encrypt(pack.GetAll(),self.QQ.PcKeyFor0819)

        pack.Empty()
        pack.SetHex("02 36 39")
        pack.SetHex("08 19")
        pack.SetBin(util.GetRandomBin(2))
        pack.SetHex("00 00 00 00 03 00 00 00 01 01 01 00 00 67 B7 00 00 00 00 00 30 00 3A")
        pack.SetShort(len(self.QQ.PcToken0038From0818))
        pack.SetBin(self.QQ.PcToken0038From0818)
        pack.SetBin(data)
        pack.SetHex("03")
        data = pack.GetAll()

        return data

    def pack_0836(self) -> bytes:
        tlv = qqTlv.Tlv()
        tea = qqTea.Tea()
        pack = packEncrypt.PackEncrypt()
        self.QQ.RandHead16 = util.GetRandomBin(16)

        pack.Empty()
        pack.SetBin(tlv.Tlv112(self.QQ.PcToken0038From0825))
        pack.SetBin(tlv.Tlv30F("DawnNights"))
        pack.SetBin(tlv.Tlv005(self.QQ.BinQQ))
        pack.SetBin(tlv.Tlv303(self.QQ.PcToken0060From0819))
        pack.SetBin(tlv.Tlv015())
        pack.SetBin(tlv.Tlv01A(self.QQ.PcKeyTgt))
        pack.SetBin(tlv.Tlv018(self.QQ.BinQQ))
        pack.SetBin(tlv.Tlv103())
        pack.SetBin(tlv.Tlv312())
        pack.SetBin(tlv.Tlv313())
        pack.SetBin(tlv.Tlv102(self.QQ.PcToken0038From0825))
        data = tea.Encrypt(pack.GetAll(),self.QQ.ShareKey)

        pack.Empty()
        pack.SetHex("02 36 39")
        pack.SetHex("08 36")
        pack.SetBin(util.GetRandomBin(2))
        pack.SetBin(self.QQ.BinQQ)
        pack.SetHex("03 00 00 00 01 01 01 00 00 67 B7 00 00 00 00 00 01")
        pack.SetHex("01 02")
        pack.SetShort(len(self.QQ.PublicKey))
        pack.SetBin(self.QQ.PublicKey)
        pack.SetHex("00 00 00 10")
        pack.SetBin(self.QQ.RandHead16)
        pack.SetBin(data)
        pack.SetHex("03")
        data = pack.GetAll()
        return data

    def pack_0828(self) -> bytes:
        tlv = qqTlv.Tlv()
        tea = qqTea.Tea()
        pack = packEncrypt.PackEncrypt()

        pack.Empty()

        pack.SetBin(tlv.Tlv007(self.QQ.PcToken0088From0836))
        pack.SetBin(tlv.Tlv00C(self.QQ.ConnectSeverIp))
        pack.SetBin(tlv.Tlv015())
        pack.SetBin(tlv.Tlv036())
        pack.SetBin(tlv.Tlv018(self.QQ.BinQQ))
        pack.SetBin(tlv.Tlv01F())
        pack.SetBin(tlv.Tlv105())
        pack.SetBin(tlv.Tlv10B())
        pack.SetBin(tlv.Tlv02D())
        data = tea.Encrypt(pack.GetAll(),self.QQ.PcKeyFor0828Send)

        pack.Empty()
        pack.SetHex("02 36 39")
        pack.SetHex("08 28")
        pack.SetBin(util.GetRandomBin(2))
        pack.SetBin(self.QQ.BinQQ)
        pack.SetHex("02 00 00 00 01 01 01 00 00 67 B7 00 30 00 3A")
        pack.SetShort(len((self.QQ.PcToken0038From0836)))
        pack.SetBin(self.QQ.PcToken0038From0836)
        pack.SetBin(data)
        pack.SetHex("03")
        data = pack.GetAll()
        return data

    def pack_001D(self) -> bytes:
        '''更新Clientkey'''
        tea = qqTea.Tea()
        pack = packEncrypt.PackEncrypt()

        pack.Empty()

        pack.SetHex("11")
        data = tea.Encrypt(pack.GetAll(),self.QQ.SessionKey)

        pack.Empty()
        pack.SetHex("02 36 39")
        pack.SetHex("00 1D")
        pack.SetBin(util.GetRandomBin(2))
        pack.SetBin(self.QQ.BinQQ)
        pack.SetHex("02 00 00 00 01 01 01 00 00 67 B7")
        pack.SetBin(data)
        pack.SetHex("03")
        data = pack.GetAll()
        return data

    def pack_00EC(self,state: int) -> bytes:
        '''
        置上线状态
        :param state:
        1 = 在线
        2 = Q我吧
        3 = 离开
        4 = 忙碌
        5 = 请勿打扰
        6 = 隐身
        '''
        tea = qqTea.Tea()
        pack = packEncrypt.PackEncrypt()
        pack.SetHex("01 00")

        if state == 1:
            pack.SetHex("0A")
        elif state == 2:
            pack.SetHex("3C")
        elif state == 3:
            pack.SetHex("1E")
        elif state == 4:
            pack.SetHex("32")
        elif state == 5:
            pack.SetHex("46")
        elif state == 6:
            pack.SetHex("28")
        else:
            pack.SetHex("0A")

        pack.SetHex("00 01 00 01 00 04 00 00 00 00")
        data = tea.Encrypt(pack.GetAll(),self.QQ.SessionKey)
        pack.Empty()
        pack.SetHex("02 36 39")
        pack.SetHex("00 EC")
        pack.SetBin(util.GetRandomBin(2))
        pack.SetBin(self.QQ.BinQQ)
        pack.SetHex("02 00 00 00 01 01 01 00 00 67 B7")
        pack.SetBin(data)
        pack.SetHex("03")
        data = pack.GetAll()
        return data


    def pack_0017(self, sendData: bytes, sequence: bytes) -> bytes:
        '''
        确认群消息已读
        :param sendData: 消息包解密前16位
        :param sequence: 消息包序列
        '''
        tea = qqTea.Tea()
        pack = packEncrypt.PackEncrypt()

        pack.Empty()
        pack.SetBin(sendData)
        data = tea.Encrypt(pack.GetAll(),self.QQ.SessionKey)

        pack.Empty()
        pack.SetHex("02 36 39")
        pack.SetHex("00 17")
        pack.SetBin(sequence)
        pack.SetBin(self.QQ.BinQQ)
        pack.SetHex("02 00 00 00 01 01 01 00 00 67 B7")
        pack.SetBin(data)

        pack.SetHex("03")
        data = pack.GetAll()
        return data

    def pack_00CE(self,sendData: bytes, sequence: bytes) -> bytes:
        '''
        确认好友消息已读
        :param sendData: 消息包解密前16位
        :param sequence: 消息包序列
        '''
        tea = qqTea.Tea()
        pack = packEncrypt.PackEncrypt()

        pack.Empty()
        pack.SetBin(sendData)
        data = tea.Encrypt(sendData,self.QQ.SessionKey)

        pack.Empty()
        pack.SetHex("02 36 39")
        pack.SetHex("00 CE")
        pack.SetBin(sequence)
        pack.SetBin(self.QQ.BinQQ)
        pack.SetHex("02 00 00 00 01 01 01 00 00 67 B7")
        pack.SetBin(data)

        pack.SetHex("03")
        data = pack.GetAll()
        return data

    def pack_0002(self, groupId: int, content: str) -> bytes:
        '''
        构建发送群文本消息包
        :param groupId: 发送群号
        :param content: 消息内容
        '''

        tea = qqTea.Tea()
        pack = packEncrypt.PackEncrypt()
        self.QQ.Time = int(time()).to_bytes(4,"big")
        Msg = content.encode()

        pack.Empty()
        pack.SetHex("00 01 01 00 00 00 00 00 00 00 4D 53 47 00 00 00 00 00")
        pack.SetBin(self.QQ.Time)
        pack.SetBin(self.QQ.Time[::-1])
        pack.SetHex("00 00 00 00 09 00 86 00 00 06 E5 AE 8B E4 BD 93 00 00 01")
        pack.SetShort(len(Msg) + 3)
        pack.SetHex("01")
        pack.SetShort(len(Msg))
        pack.SetBin(Msg)
        data = pack.GetAll()

        pack.Empty()
        pack.SetHex("2A")
        pack.SetInt(groupId)
        pack.SetShort(len(data))
        pack.SetBin(data)
        data = tea.Encrypt(pack.GetAll(),self.QQ.SessionKey)

        pack.Empty()
        pack.SetHex("02 36 39")
        pack.SetHex("00 02")
        pack.SetBin(util.GetRandomBin(2))
        pack.SetBin(self.QQ.BinQQ)
        pack.SetHex("02 00 00 00 01 01 01 00 00 67 B7")
        pack.SetBin(data)
        pack.SetHex("03")
        data = pack.GetAll()
        return data

    def pack_00CD(self, userId: int, content: str) -> bytes:
        '''
        构建发送好友文本消息包
        :param userId: 发送帐号
        :param content: 消息内容
        '''

        tea = qqTea.Tea()
        pack = packEncrypt.PackEncrypt()
        self.QQ.Time = int(time()).to_bytes(4, "big")
        Msg = content.encode()

        pack.Empty()
        pack.SetBin(self.QQ.BinQQ)
        pack.SetInt(userId)
        pack.SetHex("00 00 00 08 00 01 00 04 00 00 00 00 36 39")
        pack.SetBin(self.QQ.BinQQ)
        pack.SetInt(userId)

        pack.SetBin(util.HashMD5(self.QQ.Time))

        pack.SetHex("00 0B 4A B6")
        pack.SetBin(self.QQ.Time)
        pack.SetHex("02 55 00 00 00 00 01 00 00 00 01 4D 53 47 00 00 00 00 00")
        pack.SetBin(self.QQ.Time)
        pack.SetBin(self.QQ.Time[::-1])
        pack.SetHex("00 00 00 00 09 00 86 00 00 06 E5 AE 8B E4 BD 93 00 00 01")
        pack.SetShort(len(Msg) + 3)
        pack.SetHex("01")
        pack.SetShort(len(Msg))
        pack.SetBin(Msg)
        data = tea.Encrypt(pack.GetAll(),self.QQ.SessionKey)

        pack.Empty()
        pack.SetHex("02 36 39")
        pack.SetHex("00 CD")
        pack.SetBin(util.GetRandomBin(2))
        pack.SetBin(self.QQ.BinQQ)
        pack.SetHex("02 00 00 00 01 01 01 00 00 67 B7")
        pack.SetBin(data)
        pack.SetHex("03")
        data = pack.GetAll()
        return data