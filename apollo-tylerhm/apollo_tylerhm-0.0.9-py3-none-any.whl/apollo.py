import sys
from . import arguments, custom_checker, diff_checker, token_checker, epsilon_checker

def check(judge_input, user_output, judge_output, tokenizer = False, epsilon = None, checker = None):
    if (checker != None):
        return custom_checker.check(checker, judge_input, user_output, judge_output)

    with open(user_output) as user_out, open(judge_output) as judge_out:
        if tokenizer:
            res = token_checker.check(user_out, judge_out)
        elif epsilon != None:
            res = epsilon_checker.check(user_out, judge_out, epsilon)
        else:
            res = diff_checker.check(user_out, judge_out)

    return res

def _cli():
    args = arguments.parse()
    res = check(args.input, args.user_output, args.judge_output, args.tok, args.eps, args.checker);

    if (args.verbose):
        print(res.to_string())

    sys.exit(res.verdict.return_code);

