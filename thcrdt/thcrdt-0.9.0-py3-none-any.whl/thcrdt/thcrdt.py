__all__ = ['CRDTOk', 'CRDTErr', 'CRDTResult', 'CRDT', 'Counter', '_CRDT_List_Object', '_CRDT_Dict_Object']

import os
import json
from uuid import uuid4
from typing import Any, TypeAlias, Union, Callable

from thresult.result import Ok, Err, wrap_result
from thquickjs.thquickjs import QuickJS


_CRDT_Object: TypeAlias = '_CRDT_Object'
_CRDT_Counter_Object: TypeAlias = '_CRDT_Counter_Object'


class CRDTOk(Ok):
    pass


class CRDTErr(Err):
    pass


CRDTResult: type = CRDTOk[Any] | CRDTErr[str]


class _CRDT_Object:
    '''
    A class to handle distributed conflict-free data type
    '''
    root: _CRDT_Object
    parent: Union['quickjs.Object', _CRDT_Object]
    rendered_ops: list[str]


    def render_op(self, op: tuple) -> str:
        '''
        TODO: Add docstring
        '''
        # print(f'render_op: {op}')
        opcode, operands = op
        rendered_op: str

        # prev_rendered_ops
        prev_rendered_ops = []
        child_value = self
        parent: Union['quickjs.Object', list, dict] = self.parent

        # last_rendered_op
        last_rendered_op: str

        while True:
            if isinstance(parent, list):
                child_key = parent.index(child_value)
            elif isinstance(parent, dict):
                for k, v in parent.items():
                    if v is child_value:
                        child_key = k
                        break
            else:
                break

            prev_rendered_op: str = f'[{child_key!r}]'
            prev_rendered_ops.insert(0, prev_rendered_op)

            child_value = parent
            parent = parent.parent

        #
        # eval
        #
        first_rendered_op: str = 'doc'

        match opcode:
            case 'setitem':
                key, value = operands

                # last_rendered_op
                if isinstance(self, (list, dict)):
                    last_rendered_op = f'[{key!r}] = {value!r}'
                else:
                    raise ValueError(f'Unsupported type {type(self)}')
            case 'delitem':
                # FIXME: refactor
                # key = operands[0]
                key, = operands

                # last_rendered_op
                if isinstance(self, (list, dict)):
                    first_rendered_op = 'delete doc'
                    last_rendered_op = f'[{key!r}]'
                else:
                    raise ValueError(f'Unsupported type {type(self)}')
            case 'dict.delitem':
                # key = operands[0]
                key, = operands

                # last_rendered_op
                if isinstance(self, dict):
                    first_rendered_op = 'delete doc'
                    last_rendered_op = f'[{key!r}]'
                else:
                    raise ValueError(f'Unsupported type {type(self)}')
            case 'list.append':
                # key = operands[0]
                key, = operands
                
                # last_rendered_op
                if isinstance(self, (list, dict)):
                    last_rendered_op = f'.push({key!r})'
                else:
                    raise ValueError(f'Unsupported type {type(self)}')
            case 'list.pop':
                # last_rendered_op
                if isinstance(self, (list,)):
                    last_rendered_op = f'.pop()'
                else:
                    raise ValueError(f'Unsupported type {type(self)}')
            case 'list.shift':
                # last_rendered_op
                if isinstance(self, (list,)):
                    last_rendered_op = f'.shift()'
                else:
                    raise ValueError(f'Unsupported type {type(self)}')
            case 'Counter.increment':
                # v = operands[0]
                v, = operands

                # last_rendered_op
                last_rendered_op = f'.increment({v})'
            case 'Counter.decrement':
                # v = operands[0]
                v, = operands

                # last_rendered_op
                last_rendered_op = f'.decrement({v})'
            case _:  # pragma: no cover
                raise ValueError(f'Unsupported operation {opcode!r}')

        # rendered_op
        rendered_op = first_rendered_op + ''.join(prev_rendered_ops) + last_rendered_op
        # print('rendered_op:', rendered_op)
        return rendered_op


class _CRDT_List(list):
    '''
    A class representing an underlying object for _CRDT_List_Object
    '''
    id: str


    def __init__(self, *args, **kwargs):
        tmp: list = list(*args, **kwargs)
        new_tmp: list = []

        for v in tmp:
            id_: str | None

            try:
                id_ = v.id
            except AttributeError as e:
                id_ = None

            if isinstance(v, list):
                v = _CRDT_List(v)
            elif isinstance(v, dict):
                v = _CRDT_Dict(v)
            
            if id_:
                v.id = id_

            new_tmp.append(v)

        list.__init__(self, new_tmp)


class _CRDT_List_Object(_CRDT_Object, list):
    '''
    TODO: Add docstring
    '''
    def __init__(self, root, parent, *args, **kwargs):
        tmp: list = list(*args, **kwargs)
        new_tmp: list = []

        if root is None:
            root = self
        for v in tmp:
            if isinstance(v, list):
                v = _CRDT_List_Object(root, self, v)
            elif isinstance(v, dict):
                v = _CRDT_Dict_Object(root, self, v)

            new_tmp.append(v)

        list.__init__(self, new_tmp)
        self.root = root
        self.parent = parent
        self.rendered_ops = []


    def __repr__(self) -> str:
        return f'_CRDT_List_Object {list.__repr__(self)}'


    def __setitem__(self, key: Any, value: Any):
        # render op
        op = ('setitem', (key, value))
        rendered_op: str = self.render_op(op)
        self.root.rendered_ops.append(rendered_op)
        list.__setitem__(self, key, value)


    def __delitem__(self, key: Any):
        # render op
        op = ('delitem', (key,))
        rendered_op: str = self.render_op(op)
        self.root.rendered_ops.append(rendered_op)
        
        try:
            list.__delitem__(self, key)
        except IndexError as e:
            pass
        # list.__delitem__(self, key)


    def dumps(self) -> str:
        '''
        Dumps CRDT list to JSON string
        '''
        items = []

        for v in self:
            # value
            v_s: str
                
            if isinstance(v, _CRDT_Counter):
                v_s = f'new Automerge.Counter({int.__repr__(v)})'
            elif isinstance(v, list):
                v_s = v.dumps()
            elif isinstance(v, dict):
                v_s = v.dumps()
            else:
                v_s = json.dumps(v)
            
            items.append(v_s)

        s: str = '[\n' + ',\n'.join(items) + ']'
        return s


    def append(self, item: Any):
        '''
        Inserts item to the end of the CRDT list and removes the item from the list
        '''
        # render op
        op = ('list.append', (item,))
        rendered_op: str = self.render_op(op)
        self.root.rendered_ops.append(rendered_op)

        list.append(self, item)


    def pop(self) -> Any:
        '''
        Returns last item from CRDT list and removes the item from the list
        '''
        # render op
        op = ('list.pop', ())
        rendered_op: str = self.render_op(op)
        self.root.rendered_ops.append(rendered_op)

        v: Any = list.pop(self)
        return v


    def shift(self) -> Any:
        '''
        Returns first item from CRDT list and removes the item from the list
        '''
        # render op
        op = ('list.shift', ())
        rendered_op: str = self.render_op(op)
        self.root.rendered_ops.append(rendered_op)

        v: Any = list.pop(self, 0)
        return v


class _CRDT_Dict(dict):
    '''
    A class representing an underlying object for _CRDT_Dict_Object
    '''
    id: str


    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and (arg := args[0]) and isinstance(arg, dict) and '__type__' in arg and '__value__' in arg:
            if arg['__type__'] == 'Counter':
                self = _CRDT_Counter(arg['__value__'])
            else:  # pragma: no cover
                raise ValueError('Unsupported type/value {arg!r}')
        else:
            self = dict.__new__(cls, *args, **kwargs)

        return self


    def __init__(self, *args, **kwargs):
        tmp: dict = dict(*args, **kwargs)
        new_tmp: dict = {}

        for k, v in tmp.items():
            id_: str | None

            try:
                id_ = v.id
            except AttributeError as e:
                id_ = None

            if isinstance(v, list):
                v = _CRDT_List(v)
            elif isinstance(v, dict):
                v = _CRDT_Dict(v)

            if id_: # pragma: no cover
                v.id = id_

            new_tmp[k] = v

        dict.__init__(self, new_tmp)


class _CRDT_Dict_Object(_CRDT_Object, dict):
    '''
    TODO: Add docstring
    '''
    def __new__(cls, root, parent, *args, **kwargs):
        if len(args) == 1 and (arg := args[0]) and isinstance(arg, dict) and '__type__' in arg and '__value__' in arg:
            if arg['__type__'] == 'Counter':
                self = _CRDT_Counter_Object(root, parent, arg['__value__'])
            else:  # pragma: no cover
                raise ValueError('Unsupported type/value {arg!r}')
        else:
            self = dict.__new__(cls, *args, **kwargs)

        return self


    def __init__(self, root, parent, *args, **kwargs):
        tmp: dict = dict(*args, **kwargs)
        new_tmp: dict = {}

        if root is None:
            root = self

        for k, v in tmp.items():
            if isinstance(v, list):
                v = _CRDT_List_Object(root, self, v)
            elif isinstance(v, dict):
                v = _CRDT_Dict_Object(root, self, v)

            new_tmp[k] = v

        dict.__init__(self, new_tmp)
        self.root = root
        self.parent = parent
        self.rendered_ops = []


    def __repr__(self) -> str:
        return f'_CRDT_Dict_Object {dict.__repr__(self)}'


    def __setitem__(self, key: Any, value: Any):
        # render op
        op = ('setitem', (key, value))
        rendered_op: str = self.render_op(op)
        self.root.rendered_ops.append(rendered_op)
        
        dict.__setitem__(self, key, value)


    def __delitem__(self, key: Any):
        # render op
        op = ('dict.delitem', (key,))
        rendered_op: str = self.render_op(op)
        self.root.rendered_ops.append(rendered_op)
        
        try:
            dict.__delitem__(self, key)
        except KeyError as e:
            pass
        # dict.__delitem__(self, key)


    def dumps(self) -> str:
        '''
        Dumps CRDT dict to JSON string
        '''
        items = []

        for k, v in self.items():
            # key
            k_s: str = json.dumps(k)
            
            # value
            v_s: str
                
            if isinstance(v, _CRDT_Counter):
                v_s = f'new Automerge.Counter({int.__repr__(v)})'
            elif isinstance(v, list):
                v_s = v.dumps()
            elif isinstance(v, dict):
                v_s = v.dumps()
            else:
                v_s = json.dumps(v)
            
            item = (k_s, v_s)
            items.append(item)

        s: str = '{\n' + ',\n'.join(f'{k}: {v}' for k, v in items) + '\n}'
        return s


class _CRDT_Counter(int):
    '''
    A class representing an underlying object for _CRDT_Counter_Object
    '''
    id: str


    def __repr__(self) -> str:
        return f'_CRDT_Counter({int.__repr__(self)})'


    def increment(self, v: int=1):
        self += v


    def decrement(self, v: int=1):
        self -= v


Counter = _CRDT_Counter


class _CRDT_Counter_Object(_CRDT_Object, _CRDT_Counter):
    '''
    A class representing datatype used for concurrent counter
    '''
    def __new__(cls, root, parent, value: int) -> _CRDT_Counter_Object:
        self = Counter.__new__(cls, value)
        return self


    def __init__(self, root, parent, value: int):
        self.root = root
        self.parent = parent
        self.rendered_ops = []


    def __repr__(self) -> str:
        return f'_CRDT_Counter_Object {int.__repr__(self)}'


    def increment(self, v: int=1):
        '''
        Increase counter value
        '''
        # render op
        op = ('Counter.increment', (v,))
        rendered_op: str = self.render_op(op)
        self.root.rendered_ops.append(rendered_op)

        Counter.increment(self, v)


    def decrement(self, v: int=1):
        '''
        Decrease counter value
        '''
        # render op
        op = ('Counter.decrement', (v,))
        rendered_op: str = self.render_op(op)
        self.root.rendered_ops.append(rendered_op)

        Counter.decrement(self, v)


class CRDT:
    '''
    Creates a new CRDT instance.
    '''
    def __init__(self):
        self.qjs = QuickJS()

        # import encoding
        path = os.path.join('/deps', '', 'vendor', 'encoding.js')
        self.qjs.import_js_module(path).unwrap()

        # import automerge
        path = os.path.join('/deps', '', 'vendor', 'automerge.js')
        self.qjs.import_js_module(path).unwrap()

        self.qjs.eval('''
            Automerge.Counter.prototype.toJSON = function() {
                return {
                    __type__: 'Counter',
                    __value__: this.valueOf()
                }
            };
        ''').unwrap()


    @wrap_result(CRDTResult[Any, str])
    def from_(self, o: Any) -> Any:
        '''
        Creates a new CRDT object and populates it with the contents of the passed object
        '''
        r_id = str(uuid4()).lower().replace('-', '_')
        r_var = f'__r_{r_id}'
        
        # o_json: str = json.dumps(o)
        o = _CRDT_Dict_Object(None, None, o)
        o_str: str = o.dumps()

        code = f'''
            var {r_var} = Automerge.from({o_str});
            {r_var}
        '''

        v = self.qjs.eval(code, as_json=True).unwrap()

        # return _CRDT_Dict
        r = _CRDT_Dict(v)
        r.id = r_var
        return r


    @wrap_result(CRDTResult[Any, str])
    def change(self, doc: Any, fn: Callable) -> Any:
        '''
        Modify an CRDT object, returning an updated copy
        '''
        fn_id = id(fn)
        fn_name: str = f'__change_{fn_id}'
        r_id = str(uuid4()).lower().replace('-', '_')
        r_var = f'__r_{r_id}'

        # add callable
        def wrap_fn(qjs_object: Any) -> Any:
            # doc
            doc_json: str = qjs_object.json()
            doc: dict | list = json.loads(doc_json)
            # print('wrap_fn doc:', doc)
            
            # _CRDT_Object
            if isinstance(doc, list): # pragma: no cover
                obj = _CRDT_List_Object(None, qjs_object, doc)
            elif isinstance(doc, dict):
                obj = _CRDT_Dict_Object(None, qjs_object, doc)
            else:  # pragma: no cover
                raise ValueError('Unsupported object type')

            # invoke "native" python function
            r = fn(obj)

            # rendered operations
            rendered_ops = obj.rendered_ops
            # print(f'rendered_ops: {rendered_ops}')

            res = {'obj': r, 'rendered_ops': rendered_ops}
            # print('!res:', res)
            return json.dumps(res)


        self.qjs.add_callable(fn_name, wrap_fn).unwrap()

        # invoke callable from automerge method
        code = f'''
            var {r_var} = Automerge.change({doc.id}, doc => {{
                var r = {fn_name}(doc);
                var {{ obj, rendered_ops }} = JSON.parse(r);

                rendered_ops.map(op => {{
                    eval(op);
                }});
            }});

            {r_var}
        '''

        v = self.qjs.eval(code, as_json=True).unwrap()

        # return _CRDT_Dict
        r = _CRDT_Dict(v)
        r.id = r_var
        return r


    @wrap_result(CRDTResult[Any, str])
    def get_changes(self, root: Any, doc: Any) -> Any:
        '''
        Returns a list of all the changes that were made in the document
        '''
        r_id = str(uuid4()).lower().replace('-', '_')
        r_var = f'__r_{r_id}'
        
        code = f'''
            var {r_var} = Automerge.getChanges({root.id}, {doc.id});
            {r_var}
        '''

        v = self.qjs.eval(code, as_json=True).unwrap()
        
        # convert dict/object to Uint8Array-like array
        v = [list(n.values()) for n in v]

        # return _CRDT_List
        r = _CRDT_List(v)
        r.id = r_var
        return r


    @wrap_result(CRDTResult[Any, str])
    def apply_changes(self, root: Any, doc: Any) -> _CRDT_List:
        '''
        Applies the list of changes to the given document, and returns a new document with those changes applied
        '''
        r_id = str(uuid4()).lower().replace('-', '_')
        r_var = f'__r_{r_id}'
        root_id = str(uuid4()).lower().replace('-', '_')
        root_var = f'__root_{root_id}'
        patch_id = str(uuid4()).lower().replace('-', '_')
        patch_var = f'__patch_{patch_id}'
        doc_json: str = json.dumps(doc)

        code = f'''
            var {r_var} = Automerge.applyChanges(
                {root.id},
                {doc_json}.map(n => Uint8Array.from(n))
            );

            var [{root_var}, {patch_var}] = {r_var};
            {r_var};
        '''

        v = self.qjs.eval(code, as_json=True).unwrap()
        
        # root
        root = _CRDT_Dict(v[0])
        root.id = root_var

        # patch
        patch = _CRDT_List(v[1])
        patch.id = patch_var

        # return _CRDT_List
        r = _CRDT_List([root, patch])
        r.id = r_var
        return r


    @wrap_result(CRDTResult[Any, str])
    def merge(self, a: Any, b: Any) -> Any:
        '''
        Looks for any changes that appear in 'b' but not in 'a',
        and applies them to 'a', returning an updated version of 'a'
        '''
        r_id = str(uuid4()).lower().replace('-', '_')
        r_var = f'__r_{r_id}'
        
        code = f'''
            var {r_var} = Automerge.merge({a.id}, {b.id});
            {r_var}
        '''

        v = self.qjs.eval(code, as_json=True).unwrap()
        
        # return _CRDT_Dict
        r = _CRDT_Dict(v)
        r.id = r_var
        return r


    @wrap_result(CRDTResult[Any, str])
    def clone(self, root: Any) -> Any:
        '''
        Clone CRDT object
        '''
        r_id = str(uuid4()).lower().replace('-', '_')
        r_var = f'__r_{r_id}'
        
        code = f'''
            var {r_var} = Automerge.clone({root.id});
            {r_var}
        '''

        v = self.qjs.eval(code, as_json=True).unwrap()
        
        # return _CRDT_Dict
        r = _CRDT_Dict(v)
        r.id = r_var
        return r