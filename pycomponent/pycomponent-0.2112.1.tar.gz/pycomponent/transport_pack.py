import boxx
import gzip
import pickle

from boxx import np


class TransportPack:
    @classmethod
    def pack(cls, obj, compress=False, compresslevel=9):
        import msgpack

        binary = pickle.dumps(obj)
        if compress:
            binary = gzip.compress(binary, compresslevel=compresslevel)

        dic = {b"compress": compress, b"binary": binary}
        boxx.mg()
        return msgpack.packb(dic)

    @classmethod
    def unpack(cls, packed):
        import msgpack

        dic = msgpack.unpackb(packed)
        binary = dic[b"binary"]
        if dic[b"compress"]:
            binary = gzip.decompress(binary)
        obj = pickle.loads(binary)
        return obj

    @classmethod
    def test(cls, obj=None):
        if obj is None:
            img = boxx.uint8(np.random.random((2 ** 20)))
            obj = {"str": "abc", "img": img}
        with boxx.timeit("packed"):
            packed = cls.pack(obj)
            obj1 = cls.unpack(packed)
        print(f"with size {len(packed)//1024}KB")
        with boxx.timeit("zip_packed"):
            zip_packed = cls.pack(obj, True)
            obj2 = cls.unpack(zip_packed)
        print(f"with size {len(zip_packed)//1024}KB")
        tree - [obj, obj1, obj2]

        g()


if __name__ == "__main__":
    from boxx import *

    TransportPack.test(imread("/home/dl/mars火星.jpg"))
