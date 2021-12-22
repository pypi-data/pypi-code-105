from . core import Literal
from collections import defaultdict
import re
# PRECOMPUTE THESE

# REG
r_literal = r'(body|head)_literal\((\d+),(\w+),(\d+),\((.*?)\)\)'
r_direction = r'direction\((\w+),\((.*?)\)'
r_min_clause = r'min_clause\((\d+),(\d+)\)'
r_before = r'before\((\d+),(\d+)\)'

from itertools import permutations
max_vars = 10
args_map = {}
for arity in range(1, 5):
    for xs in permutations(range(max_vars), arity):
        k = ','.join(str(x) for x in xs)
        v = tuple(chr(ord('A') + int(x)) for x in xs)
        if len(v) == 1:
            k += ','
        args_map[k] = v

# @profile
def generate_program(model):
    before     = defaultdict(set)
    min_clause = defaultdict(lambda: 0)
    # directions = defaultdict(lambda: defaultdict(lambda: '?'))
    directions = {}
    rule_id_to_body = defaultdict(set)
    rule_id_to_head_literal = {}

    m = ' '.join(str(atom) for atom in model)
    for (sym, c, p, arity, args) in re.findall(r_literal, m):
        rule_id = int(c)
        args = args_map[args]
        arity = int(arity)
        literal = (p, args, arity)
        if sym == 'head':
            rule_id_to_head_literal[rule_id] = literal
        else:
            rule_id_to_body[rule_id].add(literal)

    for (sym, dirs) in re.findall(r_direction, m):
        dirs = tuple(x for x in dirs.split(',') if x != '')
        directions[sym] = dirs

    for (c1, c2) in re.findall(r_before, m):
        before[int(c1)].add(int(c2))

    for (clause, min_clause_num) in re.findall(r_min_clause, m):
        clause = int(clause)
        min_clause_num = int(min_clause_num)
        min_clause[clause] = max(min_clause[clause], min_clause_num)

    clauses = []
    for rule_id in rule_id_to_head_literal:
        (head_pred, head_args, head_arity) = rule_id_to_head_literal[rule_id]
        # head_modes = tuple(directions[head_pred][i] for i in range(head_arity))
        head_modes = []
        head = Literal(head_pred, head_args, head_modes)

        body = []
        for (body_pred, body_args, body_arity) in rule_id_to_body[rule_id]:
            # body_modes = tuple(directions[body_pred][i] for i in range(body_arity))
            body_modes = []
            body.append(Literal(body_pred, body_args, body_modes))
        clauses.append((head, tuple(body)))
    return (clauses, before, min_clause)