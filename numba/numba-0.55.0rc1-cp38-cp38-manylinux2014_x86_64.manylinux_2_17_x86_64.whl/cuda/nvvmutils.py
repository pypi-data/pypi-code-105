import itertools
from llvmlite import ir
from numba.core import cgutils
from .cudadrv import nvvm
from .api import current_context


def declare_atomic_cas_int(lmod, isize):
    fname = '___numba_atomic_i' + str(isize) + '_cas_hack'
    fnty = ir.FunctionType(ir.IntType(isize),
                           (ir.PointerType(ir.IntType(isize)),
                            ir.IntType(isize),
                            ir.IntType(isize)))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def atomic_cmpxchg(builder, lmod, isize, ptr, cmp, val):
    if nvvm.NVVM().is_nvvm70:
        out = builder.cmpxchg(ptr, cmp, val, 'monotonic', 'monotonic')
        return builder.extract_value(out, 0)
    else:
        return builder.call(declare_atomic_cas_int(lmod, isize),
                            (ptr, cmp, val))

# For atomic intrinsics, "numba_nvvm" prevents LLVM 9 onwards auto-upgrading
# them into atomicrmw instructions that are not recognized by NVVM. It is
# replaced with "nvvm" in llvm_to_ptx later, after the module has been parsed
# and dumped by LLVM.


def declare_atomic_add_float32(lmod):
    fname = 'llvm.numba_nvvm.atomic.load.add.f32.p0f32'
    fnty = ir.FunctionType(ir.FloatType(),
                           (ir.PointerType(ir.FloatType(), 0), ir.FloatType()))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_add_float64(lmod):
    if current_context().device.compute_capability >= (6, 0):
        fname = 'llvm.numba_nvvm.atomic.load.add.f64.p0f64'
    else:
        fname = '___numba_atomic_double_add'
    fnty = ir.FunctionType(ir.DoubleType(),
                           (ir.PointerType(ir.DoubleType()), ir.DoubleType()))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_sub_float32(lmod):
    fname = '___numba_atomic_float_sub'
    fnty = ir.FunctionType(ir.FloatType(),
                           (ir.PointerType(ir.FloatType()), ir.FloatType()))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_sub_float64(lmod):
    fname = '___numba_atomic_double_sub'
    fnty = ir.FunctionType(ir.DoubleType(),
                           (ir.PointerType(ir.DoubleType()), ir.DoubleType()))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_inc_int32(lmod):
    fname = 'llvm.nvvm.atomic.load.inc.32.p0i32'
    fnty = ir.FunctionType(ir.IntType(32),
                           (ir.PointerType(ir.IntType(32)), ir.IntType(32)))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_inc_int64(lmod):
    fname = '___numba_atomic_u64_inc'
    fnty = ir.FunctionType(ir.IntType(64),
                           (ir.PointerType(ir.IntType(64)), ir.IntType(64)))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_dec_int32(lmod):
    fname = 'llvm.nvvm.atomic.load.dec.32.p0i32'
    fnty = ir.FunctionType(ir.IntType(32),
                           (ir.PointerType(ir.IntType(32)), ir.IntType(32)))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_dec_int64(lmod):
    fname = '___numba_atomic_u64_dec'
    fnty = ir.FunctionType(ir.IntType(64),
                           (ir.PointerType(ir.IntType(64)), ir.IntType(64)))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_max_float32(lmod):
    fname = '___numba_atomic_float_max'
    fnty = ir.FunctionType(ir.FloatType(),
                           (ir.PointerType(ir.FloatType()), ir.FloatType()))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_max_float64(lmod):
    fname = '___numba_atomic_double_max'
    fnty = ir.FunctionType(ir.DoubleType(),
                           (ir.PointerType(ir.DoubleType()), ir.DoubleType()))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_min_float32(lmod):
    fname = '___numba_atomic_float_min'
    fnty = ir.FunctionType(ir.FloatType(),
                           (ir.PointerType(ir.FloatType()), ir.FloatType()))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_min_float64(lmod):
    fname = '___numba_atomic_double_min'
    fnty = ir.FunctionType(ir.DoubleType(),
                           (ir.PointerType(ir.DoubleType()), ir.DoubleType()))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_nanmax_float32(lmod):
    fname = '___numba_atomic_float_nanmax'
    fnty = ir.FunctionType(ir.FloatType(),
                           (ir.PointerType(ir.FloatType()), ir.FloatType()))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_nanmax_float64(lmod):
    fname = '___numba_atomic_double_nanmax'
    fnty = ir.FunctionType(ir.DoubleType(),
                           (ir.PointerType(ir.DoubleType()), ir.DoubleType()))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_nanmin_float32(lmod):
    fname = '___numba_atomic_float_nanmin'
    fnty = ir.FunctionType(ir.FloatType(),
                           (ir.PointerType(ir.FloatType()), ir.FloatType()))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_atomic_nanmin_float64(lmod):
    fname = '___numba_atomic_double_nanmin'
    fnty = ir.FunctionType(ir.DoubleType(),
                           (ir.PointerType(ir.DoubleType()), ir.DoubleType()))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_cudaCGGetIntrinsicHandle(lmod):
    fname = 'cudaCGGetIntrinsicHandle'
    fnty = ir.FunctionType(ir.IntType(64),
                           (ir.IntType(32),))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def declare_cudaCGSynchronize(lmod):
    fname = 'cudaCGSynchronize'
    fnty = ir.FunctionType(ir.IntType(32),
                           (ir.IntType(64), ir.IntType(32)))
    return cgutils.get_or_insert_function(lmod, fnty, fname)


def insert_addrspace_conv(lmod, elemtype, addrspace):
    addrspacename = {
        nvvm.ADDRSPACE_SHARED: 'shared',
        nvvm.ADDRSPACE_LOCAL: 'local',
        nvvm.ADDRSPACE_CONSTANT: 'constant',
    }[addrspace]
    tyname = str(elemtype)
    tyname = {'float': 'f32', 'double': 'f64'}.get(tyname, tyname)
    s2g_name_fmt = 'llvm.nvvm.ptr.' + addrspacename + '.to.gen.p0%s.p%d%s'
    s2g_name = s2g_name_fmt % (tyname, addrspace, tyname)
    elem_ptr_ty = ir.PointerType(elemtype)
    elem_ptr_ty_addrspace = ir.PointerType(elemtype, addrspace)
    s2g_fnty = ir.FunctionType(elem_ptr_ty, [elem_ptr_ty_addrspace])
    return cgutils.get_or_insert_function(lmod, s2g_fnty, s2g_name)


def declare_string(builder, value):
    lmod = builder.basic_block.function.module
    cval = cgutils.make_bytearray(value.encode("utf-8") + b"\x00")
    gl = cgutils.add_global_variable(lmod, cval.type, name="_str",
                                     addrspace=nvvm.ADDRSPACE_CONSTANT)
    gl.linkage = 'internal'
    gl.global_constant = True
    gl.initializer = cval

    charty = ir.IntType(8)
    constcharptrty = ir.PointerType(charty, nvvm.ADDRSPACE_CONSTANT)
    charptr = builder.bitcast(gl, constcharptrty)

    conv = insert_addrspace_conv(lmod, charty, nvvm.ADDRSPACE_CONSTANT)
    return builder.call(conv, [charptr])


def declare_vprint(lmod):
    voidptrty = ir.PointerType(ir.IntType(8))
    # NOTE: the second argument to vprintf() points to the variable-length
    # array of arguments (after the format)
    vprintfty = ir.FunctionType(ir.IntType(32), [voidptrty, voidptrty])
    vprintf = cgutils.get_or_insert_function(lmod, vprintfty, "vprintf")
    return vprintf


# -----------------------------------------------------------------------------

SREG_MAPPING = {
    'tid.x': 'llvm.nvvm.read.ptx.sreg.tid.x',
    'tid.y': 'llvm.nvvm.read.ptx.sreg.tid.y',
    'tid.z': 'llvm.nvvm.read.ptx.sreg.tid.z',

    'ntid.x': 'llvm.nvvm.read.ptx.sreg.ntid.x',
    'ntid.y': 'llvm.nvvm.read.ptx.sreg.ntid.y',
    'ntid.z': 'llvm.nvvm.read.ptx.sreg.ntid.z',

    'ctaid.x': 'llvm.nvvm.read.ptx.sreg.ctaid.x',
    'ctaid.y': 'llvm.nvvm.read.ptx.sreg.ctaid.y',
    'ctaid.z': 'llvm.nvvm.read.ptx.sreg.ctaid.z',

    'nctaid.x': 'llvm.nvvm.read.ptx.sreg.nctaid.x',
    'nctaid.y': 'llvm.nvvm.read.ptx.sreg.nctaid.y',
    'nctaid.z': 'llvm.nvvm.read.ptx.sreg.nctaid.z',

    'warpsize': 'llvm.nvvm.read.ptx.sreg.warpsize',
    'laneid': 'llvm.nvvm.read.ptx.sreg.laneid',
}


def call_sreg(builder, name):
    module = builder.module
    fnty = ir.FunctionType(ir.IntType(32), ())
    fn = cgutils.get_or_insert_function(module, fnty, SREG_MAPPING[name])
    return builder.call(fn, ())


class SRegBuilder(object):
    def __init__(self, builder):
        self.builder = builder

    def tid(self, xyz):
        return call_sreg(self.builder, 'tid.%s' % xyz)

    def ctaid(self, xyz):
        return call_sreg(self.builder, 'ctaid.%s' % xyz)

    def ntid(self, xyz):
        return call_sreg(self.builder, 'ntid.%s' % xyz)

    def nctaid(self, xyz):
        return call_sreg(self.builder, 'nctaid.%s' % xyz)

    def getdim(self, xyz):
        tid = self.tid(xyz)
        ntid = self.ntid(xyz)
        nctaid = self.ctaid(xyz)
        res = self.builder.add(self.builder.mul(ntid, nctaid), tid)
        return res


def get_global_id(builder, dim):
    sreg = SRegBuilder(builder)
    it = (sreg.getdim(xyz) for xyz in 'xyz')
    seq = list(itertools.islice(it, None, dim))
    if dim == 1:
        return seq[0]
    else:
        return seq
